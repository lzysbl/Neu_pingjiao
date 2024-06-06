import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import edgedriverdownloader
import xlsxwriter
import random

#评教网站
url_pinjiao = "http://210.30.204.138/school/neusoft"

def click_element(class_name,driver):
    try:
        # 查找具有 class="weui-desktop-sub-menu__item" 的 li 元素
        wait = WebDriverWait(driver, 30)
        li_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, class_name)))

        # 使用 JavaScript 点击元素
        driver.execute_script("arguments[0].click();", li_element)
        # 切换到新打开的窗口
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
    except Exception as e:
        print(f"打开链接失败: {e}")
        return None

def submit_form(class_name,driver):
    try:
        # 等待并点击确认提交按钮
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,class_name))
        )
        driver.execute_script("arguments[0].click();", submit_button)
        print("表单已提交")
    except Exception as e:
        print(f"提交表单失败: {e}")

def click_all_five(driver):
    try:
        # 等待所有单选按钮加载
        radio_buttons = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table#evlTable tbody tr td input[type="radio"]'))
        )
        print(f"单选按钮总数: {len(radio_buttons)}")

        # 遍历所有单选按钮，每找到7个就点击第二个
        for i in range(len(radio_buttons)):
            if i % 7 == 1:  # 每7个按钮点击一次，即点击第2个
                driver.execute_script("arguments[0].click();", radio_buttons[i])
                print(f"点击了第 {i+1} 个单选按钮")
                
    except Exception as e:
        print(f"点击评分失败: {e}")

def set_search_box_value(class_name,value,driver):
    try:
        # 等待搜索框元素出现
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, class_name)))

        # 清空搜索框
        search_box.clear()
        # 输入内容
        search_box.send_keys(value)
        # 获取搜索框的值
        search_value = search_box.get_attribute("value")
        print(f"搜索框的值为: {search_value}")
        return search_value
    except Exception as e:
        print(f"获取搜索框值失败: {e}")
        return None
    
    
def Start(driver):
    
    #输入学号密码
    user = input("请输入学号:")
    passward = input("请输入密码:")
    #输入评教次数
    num = int(input("请输入评教次数:"))
    # 初始化 EdgeDriver 对象
    service = webdriver.EdgeService(driver.driver_path)
    # 设置 Edge 选项
    options = webdriver.EdgeOptions()
    # 设置为无头模式
    #options.add_argument("--headless")
    # 禁用 GPU 加速
    options.add_argument("--disable-gpu")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # 使用 Edge 浏览器驱动
    driver = webdriver.Edge(service=service, options=options)
    
    
    #类名
    _user = 'input#un.login_box_input.person'
    _passward = 'input#pd.login_box_input.lock'
    _click_login =    "input#index_login_btn.login_box_landing_btn"
    _test = 'a.btn.btn-outline.btn-primary.btn-xs'#开始测评

    _put_on ="a#btn-saveResult.btn.btn-primary.btn-outline"#提交
    _confirm = "button.confirm"

    
    # 打开评教网页
    driver.get(url_pinjiao)
    #输入学号和密码
    set_search_box_value(_user,user,driver)
    print("已输入学号")
    set_search_box_value(_passward,passward,driver)
    print("已输入密码")
    #点击登录
    click_element(_click_login,driver)
    #开始测评
    for i in range(1,num):
        click_element(_test,driver)
        click_all_five(driver)
        time.sleep(1)
        click_element(_put_on,driver)
        time.sleep(1)
        submit_form(_confirm,driver)
        print(f"已完成第{i}个评教")
        time.sleep(25)
    
    print("评教完成")
    time.sleep(20)
    

#下载驱动
edgedriver=edgedriverdownloader.EdgeDriver()
Start(edgedriver)