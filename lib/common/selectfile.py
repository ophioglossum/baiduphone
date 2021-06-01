from PyQt5.QtWidgets import QFileDialog
#选择文本文件
def selectTxt(self):
    fname, _ = QFileDialog.getOpenFileName(self,'选择TXT文件', '/', "文本(*.txt)")
    return fname

def saveexcelfile(self):
    fname, _ = QFileDialog.getSaveFileName(self, '保存文件', r'/新建文件.xlsx',"Microsoft Excel 文件(*.xlsx)")
    return fname

def savetxtfile(self):
    fname, _ = QFileDialog.getSaveFileName(self, '保存文件', r'/新建文件.txt',"txt 文件(*.txt)")
    return fname