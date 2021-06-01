# -*- coding: utf-8 -*-
__author__ = '郭松'
import sys,multiprocessing
from app.Controllers.mainController import mainController
from PyQt5.QtWidgets import QApplication,QDialog
if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    # 显示主界面
    main_controller = mainController()
    main_controller.show()
    sys.exit(app.exec_())