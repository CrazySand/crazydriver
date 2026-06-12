"""基于 Selenium 的 Chromium 浏览器驱动封装。"""

import os
import sys
from pathlib import Path
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

PARENT_DIR: Path = Path(__file__).parent.resolve()

CHROME_DATA_DIR: Path = PARENT_DIR / 'chrome_data'
CHROME_DATA_DIR.mkdir(parents=True, exist_ok=True)

# 按平台选择 ChromeDriver 与浏览器可执行文件
if sys.platform == 'win32':
    CHROMEDRIVER_DEFAULT_PATH = PARENT_DIR / 'chromedriver.exe'
    DEFAULT_BROWSER_BINARY = None
elif sys.platform == 'darwin':
    CHROMEDRIVER_DEFAULT_PATH = PARENT_DIR / 'chromedriver'
    DEFAULT_BROWSER_BINARY = None
else:
    CHROMEDRIVER_DEFAULT_PATH = Path('/snap/bin/chromium.chromedriver')
    DEFAULT_BROWSER_BINARY = '/snap/bin/chromium'


class CrazyDriver(webdriver.Chrome):

    def __init__(self, headless: bool = False) -> None:
        """初始化 Chromium 浏览器驱动。

        Args:
            headless: 是否以无头模式启动，不显示浏览器窗口。
        """
        service = Service(
            executable_path=str(CHROMEDRIVER_DEFAULT_PATH),
            log_output=os.devnull,
        )

        options = Options()
        if DEFAULT_BROWSER_BINARY:
            options.binary_location = DEFAULT_BROWSER_BINARY
        options.add_experimental_option(
            'excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_argument(rf'--user-data-dir={CHROME_DATA_DIR}')
        if headless:
            options.add_argument('--headless')

        super().__init__(options=options, service=service)

        from ._stealth_min_js import code
        self.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': code
        })

    def explicit_wait(self, by: str, value: str, seconds: int = 9999) -> WebElement:
        """显式等待单个元素出现并返回。

        Args:
            by: 定位方式，如 ``By.XPATH``。
            value: 定位表达式。
            seconds: 最长等待秒数。

        Returns:
            WebElement: 匹配到的元素。
        """
        WebDriverWait(self, seconds).until(
            EC.presence_of_element_located((by, value)))
        return self.find_element(by, value)

    def explicit_waits(self, by: str, value: str, seconds: int = 9999) -> list[WebElement]:
        """显式等待多个元素出现并返回。

        Args:
            by: 定位方式，如 ``By.XPATH``。
            value: 定位表达式。
            seconds: 最长等待秒数。

        Returns:
            list[WebElement]: 匹配到的元素列表。
        """
        WebDriverWait(self, seconds).until(
            EC.presence_of_all_elements_located((by, value)))
        return self.find_elements(by, value)

    def update_window_handle(self) -> None:
        """切换到最新打开的浏览器窗口。"""
        self.switch_to.window(self.window_handles[-1])

    def scroll_to_bottom(self, scroll_delay_factor: float = 0.5) -> None:
        """模拟滚动至页面底部，用于触发懒加载内容。

        Args:
            scroll_delay_factor: 滚动延迟因子，值越大滚动越慢，建议范围 ``[0.1, 1.0]``。
        """
        get_height = 'return document.body.scrollHeight'
        height = 0
        new_height = self.execute_script(get_height)
        while height < new_height:
            for i in range(height, new_height, random.randint(800, 1000)):
                self.execute_script(f'window.scrollTo(0, {i})')
                time.sleep(random.random() * scroll_delay_factor)
            height = new_height
            new_height = self.execute_script(get_height)
