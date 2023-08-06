class LogReporter(object):
    def __init__(self, *args, **kwargs):
        super().__init__()
        logger = kwargs.get("logger")
        self.log = logger.log
        self.warning = logger.warning
        self.error = logger.error
        self.debug = logger.debug
        self.info = logger.info
