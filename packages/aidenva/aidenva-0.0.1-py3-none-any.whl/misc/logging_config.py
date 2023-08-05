import logging.config
import yaml
import os
import sys

RUNTIME_DEFAULT_PROFILE = 'default'
DEFAULT_CONFIG_PATH = 'conf'
LOGGING_FILE = 'logging-%s.yml'

class DSLogConfig:
    def __init__(self, profile, conf_path):
        if profile is None :
            self.profile = RUNTIME_DEFAULT_PROFILE
        else:
            self.profile = profile

        if conf_path is None:
            log_path = os.path.join(DEFAULT_CONFIG_PATH, (LOGGING_FILE % self.profile))
        else :
            log_path = os.path.join(conf_path, (LOGGING_FILE % self.profile))

        print('log configuraion file path : %s'%log_path)

        with open(log_path, 'r') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        sys.stdout = StreamToLogger(logging.getLogger('stdout'), logging.INFO)
        sys.stderr = StreamToLogger(logging.getLogger('stderr'), logging.ERROR)


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


