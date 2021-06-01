from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from lib.common import main_dir,logrecord

class BaiduKeyWordSearch:
    def __init__(self):
        # 设置chromium可执行文件和chromedriver.exe驱动路径
        self.options = webdriver.ChromeOptions()
        # self.options.binary_location = main_dir.get_main_dir() + '/chromium/chrome.exe'
        self.options.add_experimental_option('excludeSwitches', ['enable-automation']) #开发者模式防止selenium被识别
        self.options.add_argument("--headless") #无头浏览器
        self.options.add_argument("disable-infobars") #不显示控制
        self.options.add_argument("--no-sandbox")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--incognito')  #无痕隐身模式
        self.options.add_argument("disable-cache")  #禁用缓存
        driver_path = main_dir.get_main_dir() + '/chromedriver_win32/chromedriver.exe'
        self.browser = webdriver.Chrome(executable_path=driver_path, chrome_options=self.options)
        self.browser.implicitly_wait(10)  # 隐性等待，最长等10秒

    # 关闭浏览器
    def __del__(self):
        self.browser.close()

    #开始查询关键词
    def run_start(self,keyword):
        self.browser.get("https://www.baidu.com")
        title = WebDriverWait(self.browser, 5).until(EC.title_is(u"百度一下，你就知道"))
        if title:
            baidu_wd = self.browser.find_element_by_id("kw")  # 关键词输入框
            baidu_su = self.browser.find_element_by_id("su")  # 百度搜索按钮
            baidu_wd.send_keys(keyword)
            baidu_su.click()
            # 获取百度快照内容
            kz_list = self.get_all_kz_urls()
            return kz_list

    # 获取快照链接信息
    def get_baidu_kz_url(self):
        try:
            kz_list = []
            baidu_kz = WebDriverWait(self.browser, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.se_st_footer>a.m')))
            for item in baidu_kz:
                href = item.get_attribute('href')
                kz_list.append(href)
            return kz_list
        except Exception as e:
            logrecord.log("获取快照链接信息异常"+e)
            raise Exception("获取百度前指定页面节点异常" + e)


    #获取百度前指定页面节点
    def get_baidu_pages(self,page):
        try:
            baidu_p = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, f"//span[@class='pc' and contains(text(),'{page}')]"))).find_element_by_xpath('..')
            return baidu_p
        except Exception as e:
            logrecord.log("获取百度前指定页面节点异常"+e)
            raise Exception("获取百度前指定页面节点异常"+e)

    #获取百度前10页所有快照链接
    def get_all_kz_urls(self):
        kz_list=[]
        try:
            #获取第一页内容
            kz_temp=self.get_baidu_kz_url()
            kz_list=kz_list+kz_temp
            for page in range(2, 11, 1):
                sleep(3)
                page_el = self.get_baidu_pages(page)
                if page_el:
                    page_el.click()
                    kz_temp = self.get_baidu_kz_url()
                    kz_list=kz_list+kz_temp
            return kz_list
        except Exception as e:
            logrecord.log("百度调用异常" + e)
        finally:
            return kz_list