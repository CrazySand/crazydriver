### ChromeDriver

- **Linux（Snap Chromium）**：默认使用 `/snap/bin/chromium.chromedriver` 与 `/snap/bin/chromium`，无需手动下载
- **Windows**：将 `chromedriver.exe` 放到当前项目目录下

> Windows / x86 手动下载：https://googlechromelabs.github.io/chrome-for-testing/

### chrome_data 目录

用于存储浏览器的用户数据。行为如下：
- 目录不存在时：自动创建
- 目录已存在时：读取并使用现有数据