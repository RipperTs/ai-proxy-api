import logging
from logging.handlers import TimedRotatingFileHandler
import os


def get_log_handler():
    # 获取当前脚本所在的目录路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    if not os.path.exists(os.path.join(parent_dir, 'logs')):
        os.makedirs(os.path.join(parent_dir, 'logs'))

    log_file_path = os.path.join(parent_dir, 'logs', 'app.log')
    handler = TimedRotatingFileHandler(filename=log_file_path, when='midnight', interval=1, backupCount=7)
    handler.setLevel(logging.WARNING)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s")
    handler.setFormatter(formatter)
    return handler


def register_log_handler():
    logger = logging.getLogger()
    logger.addHandler(get_log_handler())
