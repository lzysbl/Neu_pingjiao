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
    
def get_task_count(driver):
    try:
        # 等待任务数量元素完全可见
        task_element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.col-lg-4 strong#sum"))
        )
        # 获取该元素的文本内容，并转换为整数
        task_count = int(task_element.text)
        print(f"当前任务数量: {task_count}")
        return task_count
    except Exception as e:
        print(f"获取任务数量失败: {e}")
        # 加载失败时，提示用户手动输入任务数量
        while True:
            try:
                print(f"请手动输入的任务数量: {task_count}")
                task_count = int(input("请输入任务数量: "))
                return task_count
            except ValueError:
                print("输入无效，请输入一个有效的整数。")




def submit_form(class_name, driver):
    try:
        # 等待并点击确认提交按钮
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, class_name))
        )
        driver.execute_script("arguments[0].click();", submit_button)
        print("表单已提交")
        
        # 等待页面加载完成
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a#btn-goBack"))
        )
        print("页面已加载完成")
        time.sleep(10)
        # 点击返回按钮
        back_button = driver.find_element(By.CSS_SELECTOR, "a#btn-goBack")
        driver.execute_script("arguments[0].click();", back_button)
        print("点击了返回按钮")
        time.sleep(5)
    except Exception as e:
        print(f"提交表单失败: {e}")


def click_all_five(driver):
    try:
        # 等待所有单选按钮加载
        rows = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table#evlTable tbody tr'))
        )
        print(f"总行数: {len(rows)}")
        
        # 遍历每一行
        for i, row in enumerate(rows):
            # 获取当前行的所有单选按钮
            radio_buttons_in_row = row.find_elements(By.CSS_SELECTOR, 'td input[type="radio"]')
            # 如果该行至少有两个按钮，点击第二个按钮
            if len(radio_buttons_in_row) > 1:
                driver.execute_script("arguments[0].click();", radio_buttons_in_row[1])  # 点击第二个按钮
                print(f"点击了第 {i+1} 行的第二个按钮")
            else:
                print(f"第 {i+1} 行没有第二个按钮")
        
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
    
    num = get_task_count(driver)
    #开始测评
    for i in range(1,num+1):
        click_element(_test,driver)
        click_all_five(driver)
        time.sleep(1)
        click_element(_put_on,driver)
        time.sleep(1)
        submit_form(_confirm,driver)
        print(f"已完成第{i}个评教")
        
    
    print("评教完成")
    time.sleep(10)
    

#下载驱动
edgedriver=edgedriverdownloader.EdgeDriver()
Start(edgedriver)