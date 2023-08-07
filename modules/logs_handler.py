import logging
from datetime import datetime
import dearpygui.dearpygui as dpg


class LogsHandler(logging.Handler):
    def emit(self, log: logging.LogRecord):
        asctime = datetime.fromtimestamp(log.created)
        asctime = asctime.strftime('%d.%m.%Y %H:%M')
    
        dpg.set_value('error_field_reg', f'{dpg.get_value("error_field_reg")}'
                                         f'[{log.filename}:{log.lineno}][{asctime} | {log.levelname}]: {log.msg}\n')
