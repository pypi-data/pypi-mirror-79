from rsm.utils.misc import get_module_location
from platform import system
import logging.config
import functools
import logging


RSM_MODULE_LOCATION = get_module_location('rsm')[0]


DEFAULT_LOGGING_CONFIG_FOLDER = "/conf/"
DEFAULT_LOGGING_CONFIG_FILENAME = "logging.conf"

LOGGING_CONFIG_PATH = []

# This is pretty much only for development purposes.
if system() == "Windows":
    for path in [RSM_MODULE_LOCATION, DEFAULT_LOGGING_CONFIG_FOLDER]:
        LOGGING_CONFIG_PATH.append(path.replace('/', '\\'))
    LOGGING_CONFIG_PATH.append(DEFAULT_LOGGING_CONFIG_FILENAME)
    LOGGING_CONFIG_ABS_PATH = "".join(i for i in LOGGING_CONFIG_PATH)
else:
    LOGGING_CONFIG_ABS_PATH = RSM_MODULE_LOCATION + DEFAULT_LOGGING_CONFIG_FOLDER + DEFAULT_LOGGING_CONFIG_FILENAME


class LogHandler:
    def __init__(self, logger=__name__):
        logging.config.fileConfig(
            LOGGING_CONFIG_ABS_PATH,
            disable_existing_loggers=False)
        self.logger = logging.getLogger(logger)

    def debug(self, msg):

        return self.logger.debug(msg)

    def info(self, msg):
        return self.logger.info(msg)

    def warning(self, msg):
        return self.logger.warning(msg)

    def error(self, msg):
        return self.logger.error(msg)

    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            try:
                self.logger.debug(
                    "{0} - {1} - {2}".format(fn.__name__, args, kwargs))
                result = fn(*args, **kwargs)
                self.logger.debug(result)
                return result
            except Exception as ex:
                self.logger.error("Exception {0}".format(ex))
                raise ex

        return decorated
