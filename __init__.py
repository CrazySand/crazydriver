"""
谷歌浏览器及相关驱动下载地址:
https://googlechromelabs.github.io/chrome-for-testing/

每次调用该库, 会创建一个 chrome_data 目录, 用于存储浏览器的用户数据
如果不存在则会自动创建, 存在则会读取
"""

from .core import CrazyDriver
from selenium.webdriver.common.by import By

__all__ = [
    'CrazyDriver', 
    'By'
]