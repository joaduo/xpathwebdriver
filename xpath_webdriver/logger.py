'''
Copyright (c) 2014, Juju Inc.
Copyright (c) 2011-2013, Joaquin G. Duo
'''
import rel_imp; rel_imp.init()
import logging
from .ColorStreamHandler import ColorStreamHandler

def log_test(msg, *args):
    if args:
        msg = msg % args
    try:
        print(msg)
    except IOError as e:
        if e.errno == 32:
            # Ignore broken pipe, close program
            logging.debug('Ignoring broken pipe')
            raise SystemExit
        # Forward error
        raise


class Logger(object):
    default_level = logging.INFO
    handler_level = logging.DEBUG
    default_fmt = '%(levelname)s %(asctime)s: %(message)s'
    default_datefmt = '%H:%M:%S'

    def __init__(self, name=None, output=None, level=None, color=False):
        if not level:
            level = self.default_level
        if not output:
            if not name:
                output = logging.getLogger()
            else:
                output = logging.getLogger(name)
        self.output = output
        self.color = color
        if not logging.root.handlers:
            self._config_handler()
            self.set_fmt()
            self.setLevel(level)

    def _config_handler(self):
        if not self.output.handlers:
            if self.color:
                hdlr = ColorStreamHandler()
            else:
                hdlr = logging.StreamHandler()
            hdlr.setLevel(self.handler_level)
            self.output.addHandler(hdlr)

    def set_fmt(self, fmt=None, datefmt=None):
        datefmt = datefmt or self.default_datefmt
        fmt = fmt or self.default_fmt
        hdlr = self.output.handlers[0]
        fmt = logging.Formatter(fmt=fmt,
                                datefmt=datefmt
                                )
        hdlr.setFormatter(fmt)

    def set_pre_post(self, pre='', post=''):
        if pre:
            pre = '[%s] ' % pre.strip()
        self.set_fmt(fmt=pre + self.default_fmt + post)

    def _log(self, method, msg, args):
        getattr(self.output, method)(msg, *args)

    def critical(self, msg, *args):
        self._log('critical', msg, args)

    def error(self, msg, *args):
        self._log('error', msg, args)

    def warning(self, msg, *args):
        self._log('warning', msg, args)

    def info(self, msg, *args):
        self._log('info', msg, args)

    def debug(self, msg, *args):
        self._log('debug', msg, args)

    def exception(self, msg, *args):
        self._log('exception', msg, args)

    def c(self, msg, *args):
        self.critical(msg, *args)

    def e(self, msg, *args):
        self.error(msg, *args)

    def exc(self, msg, *args):
        self.exception(msg, *args)

    def w(self, msg, *args):
        self.warning(msg, *args)

    def i(self, msg, *args):
        self.info(msg, *args)

    def d(self, msg, *args):
        self.debug(msg, *args)

    def verbose(self, msg):
        self.output.debug(str(msg))

    def v(self, msg, *args):
        self.debug(msg, *args)

    def printFilePath(self, file_path, line=None, error=False):
        if error:
            out = self.e
        else:
            out = self.d
        if not line:
            line = 1
        msg = '  File "%s", line %d\n' % (file_path, line)
        out(msg)

    def setLevel(self, level):
        if hasattr(self.output, 'setLevel'):
            self.output.setLevel(level)
        else:
            self.w('Cannot set logging level')

    def __call__(self, msg):
        self.info(msg)


def smoke_test_module():
    ''' Simple self-contained test for the module '''
    logger = Logger('a.logger')
    logger.setLevel(logging.DEBUG)
    logger.set_pre_post(pre='A.Prefix ')
    # logger.set_fmt('')
    logger.critical('critical')
    logger.debug('debug')
    logger.error('error')
    logger.info('info')
    logger.warning('warning')
    logger('Call')

if __name__ == '__main__':
    smoke_test_module()
