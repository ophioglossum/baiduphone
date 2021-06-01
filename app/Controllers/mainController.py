from ui.mainUi import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from app.Services.DbService import DbService
from config import database, app
from lib.common import check_api_back_sign,logrecord,multiprocessing_call
import tldextract, re
from lib.common.selectfile import saveexcelfile
from multiprocessing import Manager
from lib.logic import baiduLogic
from app.Threads.BaiduCheckThread import BaiduCheckThread
from app.Threads.ExportThread import ExportThread

class mainController(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainController, self).__init__(parent)
        self.setupUi(self)
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(database.QT_DB_HOST)
        self.dbConn = self.db.open()
        if not self.dbConn:
            resQB = QMessageBox.critical(None, ('无法连接数据库'), ("无法建立到数据库的连接,请联系管理员"), QMessageBox.Cancel)
            if (resQB == QMessageBox.Cancel):
                # 直接退出
                quit()
        # 主页模块内容
        self.tw_main.setColumnCount(4)
        self.tw_main.setRowCount(100)
        # 禁止任何操作
        self.tw_main.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 不显示列序号
        self.tw_main.verticalHeader().setVisible(False)
        # 行自适应
        self.tw_main.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        self.tw_main.setHorizontalHeaderLabels(["手机号","关键词","来源","创建时间"])
        # 初始化禁用上一页按钮
        self.pb_main_previous_page.setEnabled(False)
        # 刷新一次
        self.refresh_main_db()
        # 刷新
        self.pb_main_refresh.clicked.connect(self.refresh_main_db)
        # 首页
        self.pb_main_first_page.clicked.connect(self.first_main_page)
        # 上一页
        self.pb_main_previous_page.clicked.connect(self.previous_main_page)
        # 下一页
        self.pb_main_next_page.clicked.connect(self.next_main_page)
        # 转到指定页面
        self.pb_main_query.clicked.connect(self.go_main_page)
        # 清空手机号
        self.pb_db_clear.clicked.connect(self.phone_db_clear)
        # 清空关键词
        self.pb_clear_keywords.clicked.connect(self.keywords_clear)
        # 运行
        self.pb_main_run.clicked.connect(self.run_baidu)
        # 导出为excel
        # self.pb_main_export.hide()
        self.pb_main_export.clicked.connect(self.main_export_excel)

    # 分页查询方法
    def __main_recordQuery(self, limitIndex):
        # 清空内容但不含表头
        self.tw_main.clearContents()
        dbservice = DbService()
        res = dbservice.record_query(limitIndex)
        for i, row in enumerate(res):
            for j, col in enumerate(row):
                if j == 0:
                    checkbox = QTableWidgetItem(str(col))
                    checkbox.setCheckState(Qt.Unchecked)
                    self.tw_main.setItem(i, j, checkbox)
                    self.tw_main.item(i, j).setTextAlignment(Qt.AlignCenter)
                else:
                    self.tw_main.setItem(i, j, QTableWidgetItem(str(col)))
                    self.tw_main.item(i, j).setTextAlignment(Qt.AlignCenter)
            # changemainbtn = QPushButton("修改")
            # changemainbtn.clicked.connect(self.change_main_clicked)
            # self.tw_main.setCellWidget(i, 4, changemainbtn)

    # 刷新数据库
    def refresh_main_db(self):
        dbservice = DbService()
        res_count = dbservice.get_phones_count()
        self.lb_main_db_total.setText(str(res_count))
        self.go_main_page()

    # 首页
    def first_main_page(self):
        self.__main_recordQuery(1)
        self.sb_main_currentpage.setValue(1)
        self.pb_main_previous_page.setEnabled(False)

    # 上一页
    def previous_main_page(self):
        currentpage = self.sb_main_currentpage.value()
        previouspage = currentpage - 1
        if (previouspage > 1):
            self.__main_recordQuery(previouspage)
            self.sb_main_currentpage.setValue(previouspage)
        elif (previouspage == 1):
            self.__main_recordQuery(previouspage)
            self.sb_main_currentpage.setValue(previouspage)
            self.pb_main_previous_page.setEnabled(False)
        elif (previouspage < 1):
            self.pb_main_previous_page.setEnabled(False)

    # 下一页
    def next_main_page(self):
        currentpage = self.sb_main_currentpage.value()
        nextpage = currentpage + 1
        self.__main_recordQuery(nextpage)
        self.sb_main_currentpage.setValue(nextpage)
        self.pb_main_previous_page.setEnabled(True)

    # 跳转到指定页
    def go_main_page(self):
        currentpage = self.sb_main_currentpage.value()
        if (currentpage > 1):
            self.__main_recordQuery(currentpage)
            self.sb_main_currentpage.setValue(currentpage)
            self.pb_main_previous_page.setEnabled(True)
        elif (currentpage == 1):
            self.__main_recordQuery(currentpage)
            self.sb_main_currentpage.setValue(currentpage)
            self.pb_main_previous_page.setEnabled(False)
        elif (currentpage < 1):
            self.pb_main_previous_page.setEnabled(False)

    # 清空手机号
    def phone_db_clear(self):
        dbservice = DbService()
        dbservice.clear_tables()
        self.refresh_main_db()

    # 清空关键词
    def keywords_clear(self):
        self.pte_keywords.clear()

    # 去重复和去空字符
    def __getKeyWordsList(self):
        keywords_list = []
        keywords = self.pte_keywords.toPlainText()
        keywords_temp = keywords.split('\n')
        for item in keywords_temp:
            if item != '':
                keywords_list.append(item)
        new_keywords_list=list(set(keywords_list))
        #保持顺序一致
        new_keywords_list.sort(key=keywords_list.index)
        return new_keywords_list

    # 运行
    def run_baidu(self):
        if self.pb_main_run.isEnabled():
            keywords_list=self.__getKeyWordsList()
            if not keywords_list:
                # 百度token校验失败
                box = QMessageBox(QMessageBox.Warning, self.tr("提示"), self.tr("请输入关键词!"), QMessageBox.NoButton, self)
                yr_btn = box.addButton(self.tr("是"), QMessageBox.YesRole)
                box.exec_()
                if box.clickedButton() == yr_btn:
                    return
            self.pb_main_run.setEnabled(False)
            self.pb_main_run.setText("运行中...")
            # 设置进度条
            self.pbar_main.setMinimum(0)
            self.pbar_main.setValue(0)
            self.pbar_main.setMaximum(len(keywords_list))

            self.queue_info = Manager().Queue()
            self.p_baidu = multiprocessing_call.run(func_callback=baiduLogic.run, queue_info=self.queue_info,
                                                    keywords=keywords_list)
            # 检测信息
            self.baidu_check_Thread = BaiduCheckThread(queue_info=self.queue_info)
            self.baidu_check_Thread.sigbaiduprocess.connect(self.baidu_check_callback)
            self.baidu_check_Thread.sigbaidurefresh.connect(self.baidu_check_progress_callback)
            self.baidu_check_Thread.sigbaiducomplete.connect(self.badiu_check_complete_callback)
            self.baidu_check_Thread.start()


    # message 消息
    # snum 显示的毫秒,0表示不过期
    def baidu_check_callback(self,message, snum):
        self.sb_main.showMessage(message, snum)

    # 进度条
    def baidu_check_progress_callback(self,checknum):
        self.refresh_main_db()
        self.pbar_main.setValue(int(checknum))

    def badiu_check_complete_callback(self):
        self.pb_main_run.setEnabled(True)
        self.pb_main_run.setText("运行")

    # 数据tab页导出为excel
    def main_export_excel(self):
        fname = saveexcelfile(self)
        if (fname != ''):
            self.pb_main_export.setEnabled(False)
            self.pb_main_export.setText("正在导出..")
            self.exportthread = ExportThread(fname)
            self.exportthread.sigexport.connect(self.export_finish)
            self.exportthread.start()

    # 导出完成
    def export_finish(self):
        self.sb_main.showMessage("导出成功!", 5000)
        self.pb_main_export.setEnabled(True)
        self.pb_main_export.setText("导出")


