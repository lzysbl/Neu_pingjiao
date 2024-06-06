
import os
import platform
import subprocess
import requests
import zipfile
class EdgeDriver:
    def __init__(self):
        print("初始化")
        self.edge_version = None #初始化edge版本
        self.version = None #初始化平台版本
        self.driver_path = "msedgedriver.exe" #初始化驱动路径
        self.platform = None #初始化平台
        if os.path.exists(self.driver_path) is False:
            self.get_edge_version()
            self.get_platform_architecture()
            self.down_load()
        print("初始化成功")
    #获取edge浏览器版本
    def get_edge_version(self):
            try:
                result = subprocess.run(["reg", "query", "HKEY_CURRENT_USER\\Software\\Microsoft\\Edge\\BLBeacon", "/v", "version"], capture_output=True, text=True)
                self.edge_version = result.stdout.split("version    REG_SZ    ")[1].strip()
                return self.edge_version
            except Exception as e:
                return None
    #获取平台版本
    def get_platform_architecture(self):
            arch = platform.architecture()[0]
            if arch == '32bit':
                self.version = 'win32'
                return 'win32'
            elif arch == '64bit':
                self.version = 'win64'
                return 'win64'
            else:
                return 'Unknown'
    #
    def down_load(self):
        
        release_url = f"https://msedgedriver.azureedge.net/{self.edge_version}/edgedriver_{self.version}.zip"
        #下载驱动
        # 发送 GET 请求并获取文件内容
        print ("开始下载")
        response = requests.get(release_url)

        # 检查响应状态码是否为 200 (表示成功)
        if response.status_code == 200:
            # 指定本地文件路径
            local_file_path = 'msedgedriver.zip'
            # 以二进制写入方式打开本地文件，并将响应内容写入文件中
            with open(local_file_path, 'wb') as f:
                f.write(response.content)
        print("下载完成")
        #解压缩
        with zipfile.ZipFile("msedgedriver.zip", 'r') as zip_ref:
            zip_ref.extractall()
        #删除压缩包
        os.remove("msedgedriver.zip")
        #设置驱动路径
        self.driver_path = os.path.abspath("msedgedriver.exe")


