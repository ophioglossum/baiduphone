from lib.common import main_dir
#链接的sqlite地址
DB_HOST="sqlite:///"+main_dir.get_main_dir()+"/database/baiduphone.db"
#是否开启调试,False:不开启,True:开启,输入为sys.stdout,字符串'debug':结果行将被打印到标准输出
DB_DEBUG=False
#QT_数据库地址
QT_DB_HOST=main_dir.get_main_dir()+"/database/baiduphone.db"