# used to convert dict to breakpoint type for serverless
class Breakpoint(object):
    def __init__(self, dictionary):
        self.breakpoint_id = None
        self.workspace_id = None
        self.line_no = None
        self.rel_path = None
        self.src_type = None
        self.condition = None
        self.fire_count = None
        self.type = None
        self.state = None,
        self.id = None,
        self.created = None,
        self.metadata = {}
        self.named_watchers = []
        self.args = {}
        for k, v in dictionary.items():
            setattr(self, k, v)
