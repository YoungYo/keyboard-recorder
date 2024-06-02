import logging
from logging.handlers import TimedRotatingFileHandler
import os

# 创建logger对象
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_file_path = "/tmp/keyboard-recorder/"
# 判断日志文件夹是否存在，不存在则创建
if not os.path.exists(log_file_path):
    os.makedirs(log_file_path)
# 创建一个TimedRotatingFileHandler，每天生成一个新的日志文件
handler = TimedRotatingFileHandler(log_file_path + "log.txt", when="midnight", interval=1, backupCount=30000)
handler.setLevel(logging.INFO)

# 设置日志格式
formatter = logging.Formatter('%(asctime)s\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

# 将handler添加到logger对象中
logger.addHandler(handler)
