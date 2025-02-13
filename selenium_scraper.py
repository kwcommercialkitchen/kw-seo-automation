from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 配置 Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 隐藏浏览器窗口（可选）
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

service = Service("C:\\Users\\61401\\PycharmProjects\\PythonProject\\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

try:
    # 打开 Nisbets 登录页面
    driver.get("https://www.nisbets.com.au/login")
    wait = WebDriverWait(driver, 15)

    # 等待并输入账号和密码
    username_input = wait.until(EC.presence_of_element_located((By.ID, "j_username")))
    username_input.send_keys("admin@kwonline.com.au")
    password_input = driver.find_element(By.ID, "j_password")
    password_input.send_keys("12345qwert")
    driver.find_element(By.NAME, "login").click()

    # 确认是否登录成功
    time.sleep(5)
    if "My Account" in driver.page_source:
        print("登录成功！")
    else:
        print("登录失败，请检查账号和密码。")

except Exception as e:
    print(f"发生错误：{e}")

finally:
    driver.quit()
