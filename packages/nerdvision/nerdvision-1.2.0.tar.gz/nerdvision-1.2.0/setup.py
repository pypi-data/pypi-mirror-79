#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'nerdvision',
        version = '1.2.0',
        description = 'The python nerd.vision agent, allowing real time debugging, any environment, any cloud.',
        long_description = 'To use this please view the docs at https://docs.nerd.vision/python/configuration/',
        author = '',
        author_email = '',
        license = 'https://www.nerd.vision/legal/agent-license',
        url = 'https://nerd.vision',
        scripts = [],
        packages = [
            'nerdvision',
            'nerdvision.settings',
            'nerdvision.models'
        ],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'certifi==2019.9.11',
            'chardet==3.0.4',
            'grpcio~=1.23',
            'grpcio-tools~=1.23',
            'idna==2.8',
            'nerdvision-grpc-api==1.0.0',
            'protobuf~=3.9',
            'psutil==5.6.3',
            'requests==2.22.0',
            'six==1.12.0',
            'urllib3==1.25.6'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
    )
