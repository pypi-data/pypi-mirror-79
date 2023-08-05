import platform
from threading import Thread

import math
import nerdvision
import time
from nerdvision import settings
from nerdvision.BreakpointService import BreakpointService
from nerdvision.ClientRegistration import ClientRegistration


class NerdVision(object):
    def __init__(self, client_service=None, set_trace=True, serverless=False):
        self.logger = nerdvision.configure_logger(serverless=serverless)
        self.registration = client_service
        self.session_id = None
        self.grpc_service = None
        self.breakpoint_service = BreakpointService(set_trace=set_trace)
        self.thread = Thread(target=self.connect, name="NerdVision Main Thread")
        # Python 2.7 does not take 'daemon' as constructor argument
        self.thread.setDaemon(True)
        self.is_shutdown = False
        self.grpc_backoff_multiplier = settings.get_setting('grpc_backoff_multiplier')
        self.grpc_max_backoff = settings.get_setting('grpc_backoff_max')
        self.client_reg_max_backoff = settings.get_setting('client_registration_backoff_max')
        self.client_reg_backoff_multiplier = settings.get_setting('client_registration_backoff_multiplier')
        self.serverless = serverless

    def start(self):
        self.logger.info("--------------------------------------------------------------------------------------")
        self.logger.info("nerd.vision - Copyright (C) Intergral GmbH. All Rights Reserved")
        self.logger.info("%-16s: %s", "Version", nerdvision.__version__)
        self.logger.info("%-16s: %s", "Git-Commit-ID", nerdvision.__props__['__Git_Commit_Id__'])
        self.logger.info("%-16s: %s", "Git-Commit-Time", nerdvision.__props__['__Git_Commit_Time__'])
        self.logger.info("%-16s: %s (%s)", "OS", ClientRegistration.run_with_catch('os name', platform.system),
                         ClientRegistration.run_with_catch('os arch', platform.machine))
        self.logger.info("%-16s: %s [%s]", "Python", platform.python_version(), platform.python_implementation())
        self.logger.info("%-16s: %s", "Start Time", time.strftime('%a %b %d T%H:%M:%S %Z %Y'))
        self.logger.info("--------------------------------------------------------------------------------------")
        if not self.serverless:
            self.thread.start()
        else:
            self.connect()

    def connect(self):
        if not self.serverless:
            from grpc import RpcError
            from nerdvision.GRPCService import GRPCService
            if self.session_id is None:
                self.session_id = self.get_session_id()

            if self.grpc_service is None:
                self.grpc_service = GRPCService(self.session_id)

            try:
                self.grpc_service.connect(self.breakpoint_received)
                if not self.is_shutdown:
                    self.reconnect()
            except RpcError:
                if not self.is_shutdown:
                    self.logger.exception("Something went wrong with grpc connection")
                    self.reconnect()
        else:
            json = self.registration.send_client_registration()
            if json is not None:
                if 'breakpoints' in json and 'session' in json:
                    self.session_id = json['session']
                    self.breakpoint_service.process_request_serverless(json['breakpoints'], json['session'])

    def breakpoint_received(self, response):
        self.logger.debug("Received breakpoint request from service message_id: %s", response.message_id)
        self.breakpoint_service.process_request(response, self.session_id)

    def stop(self):
        self.is_shutdown = True
        self.logger.info("Stopping NerdVision")
        if self.grpc_service is not None:
            self.grpc_service.stop()
        if self.thread.is_alive():
            self.thread.join()
        self.logger.info("NerdVision shutdown")

    def get_session_id(self):
        count = 0
        while self.session_id is None:
            count = count + 1
            try:
                session_id = self.registration.run_and_get_session_id()
                if session_id is not None:
                    return session_id

            except Exception:
                self.logger.exception("Error loading session id")

            delay = self.calculate_backoff_time(count, self.client_reg_max_backoff, self.client_reg_backoff_multiplier)
            self.logger.error("Unable to load session id for agent.")
            self.logger.info("Attempting again in %d seconds", delay)
            time.sleep(delay)

        return self.session_id

    def reconnect(self):
        from grpc import RpcError
        count = 0
        while True:
            count = count + 1
            delay = NerdVision.calculate_backoff_time(count, self.grpc_max_backoff, self.grpc_backoff_multiplier)
            self.logger.info("Attempting to reconnect in %d seconds", delay)
            time.sleep(delay)
            try:
                self.grpc_service.connect(self.breakpoint_received)
                break
            except RpcError:
                if settings.is_grpc_debug_enabled():
                    self.logger.exception("Something went wrong with grpc connection")
                self.logger.warning("Could not connect client")

    @staticmethod
    def calculate_backoff_time(attempt, max_delay_in_seconds, multiplier):
        delay_in_seconds = (math.pow(2.0, attempt) - 1.0) * 0.5
        return round(min(delay_in_seconds * multiplier, max_delay_in_seconds))
