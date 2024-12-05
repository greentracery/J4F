
import traceback as tr
import logging
import os


class LogWriter():
    
    logs_dir = 'logs'
    
    def __init__(self, logname):
        logger = logging.getLogger(logname)
        logger.setLevel(logging.INFO)
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
        log_handler = logging.FileHandler(os.path.join(self.logs_dir, f"{logname}.log"), mode='w')
        log_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        log_handler.setFormatter(log_formatter)
        logger.addHandler(log_handler)
        self.logger = logger

    def log_error(self, e, trace_error: bool = False):
        """ Отправляем ошибку (error) в лог """
        self.logger.error(e)
        if trace_error:
            e_trace = self.exception_trace(e)
            msg = f"See also: file {e_trace.filename}, line {e_trace.lineno}, string `{e_trace.line}`"
            self.logger.error(msg)
    
    def log_warning(self, msg):
        """ Отправляем ошибку (warning) в лог """
        self.logger.warning(msg)
    
    def log_info(self, msg):
        """ Отправляем сообщение в лог """
        self.logger.info(msg)
        
    def exception_trace(self, e):
        """ Трассировка исключения """
        e_trace = tr.TracebackException(exc_type =type(e),exc_traceback = e.__traceback__ , exc_value =e).stack[-1]
        return e_trace

