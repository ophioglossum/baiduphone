from PyQt5.QtCore import QThread,pyqtSignal
from app.Services.DbService import DbService
from lib.common import logrecord
from openpyxl import Workbook
import traceback
#导出线程
class ExportThread(QThread):
    #定义找到结果后需要发送的信号
    sigexport = pyqtSignal()
    def __init__(self,fname):
        super(ExportThread,self).__init__()
        #初始化
        self.fname = fname

    #关闭线程
    def __del__(self):
        pass

    #运行线程
    def run(self):
        self.import_excel_file()

    def import_excel_file(self):
        pageindex = 1
        pagesize = 1000
        flag = True
        dbservice = DbService()
        book = Workbook()
        sheet = book.active
        sheet.append(['手机号','关键词','来源','创建时间'])
        try:
            while flag:
                res = dbservice.get_export_data(pagesize=pagesize, pageindex=pageindex)
                if (res):
                    for i, row in enumerate(res):
                        # logrecord.log(row)
                        # logrecord.log(type(row))
                        sheet.append(list(row))
                else:
                    flag = False
                pageindex += 1
            book.save(self.fname)
        except Exception:
            traceback.print_exc()
        finally:
            self.sigexport.emit()