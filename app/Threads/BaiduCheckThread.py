from PyQt5.QtCore import QThread, pyqtSignal


# 检测线程
class BaiduCheckThread(QThread):
    # 定义检测发送的信号
    sigbaiduprocess = pyqtSignal(str,int)
    # 刷新数据
    sigbaidurefresh = pyqtSignal(int)
    # 完成检测
    sigbaiducomplete= pyqtSignal()
    working = True

    def __init__(self, queue_info):
        super(BaiduCheckThread, self).__init__()
        self.queue_info = queue_info
        self.checknum=0

    # 关闭线程
    def __del__(self):
        self.working = False

    # 运行线程
    def run(self):
        while self.working == True:
            if not self.queue_info.empty():
                rq = self.queue_info.get()
                if rq['status'] == 0:
                    #异常情况通知
                    self.sigbaiduprocess.emit(rq['message'],0)
                elif rq['status'] == 1:
                    self.sigbaiduprocess.emit(rq['message'],0)
                elif rq['status'] == 2:
                    self.checknum+=1
                    self.sigbaidurefresh.emit(self.checknum)
                    self.sigbaiduprocess.emit(rq['message'],0)
                elif rq['status']==3:
                    #完成
                    self.sigbaiduprocess.emit(rq['message'], 0)
                    self.sigbaiducomplete.emit()
                    self.working=False
                # 睡眠1秒
                self.sleep(1)
            else:
                self.sleep(1)
