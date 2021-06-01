from sqlalchemy import func
from app.Models import Phones,PhoneSmsLogs
from app.DBbase import DBbase
from sqlalchemy import case, column
from lib.common import logrecord
import time

# 数据服务
class DbService(DBbase):
    def __init__(self):
        super(DbService, self).__init__()

    def __del__(self):
        super(DbService, self).__del__()

    # 获取Phones表总条数
    def get_phones_count(self):
        res_count = self.session.query(Phones).count()
        return res_count

    # 清空表
    def clear_tables(self):
        self.session.query(Phones).delete()
        self.session.execute('update sqlite_sequence set seq=0 where name=:table',
                             params={"table": Phones.__tablename__})
        self.session.commit()

    # 查询记录表
    def record_query(self, limitIndex):
        pagecount = 100
        limitnum = (limitIndex - 1) * pagecount
        res = self.session.query(Phones).with_entities(
            Phones.phone,
            Phones.keyword,
            Phones.source_url,
            func.datetime(Phones.create_time, 'unixepoch',
                          'localtime').label('create_time_zh')).order_by(
            Phones.id).limit(pagecount).offset(limitnum).all()
        return res

    # 批量写入手机号
    def set_phones_to_db(self,phones,source_url,kz_url,keyword):
        phones_list = phones
        db_phones_list=[]
        #域名去重复
        no_repeat_phones_list = list(set(phones_list))
        # 保持顺序一致
        no_repeat_phones_list.sort(key=phones_list.index)

        #判断有多少存在数据库中
        if len(no_repeat_phones_list)>0:
            res_phones = self.session.query(Phones).filter(Phones.phone.in_(no_repeat_phones_list)).all()
            for dbitem in res_phones:
                db_phones_list.append(dbitem.phone)
            logrecord.log(f"重复手机号:{str(db_phones_list)},不记录到数据库")

        #求出数据库没有的值
        no_db_list_phones=list(set(no_repeat_phones_list).difference(set(db_phones_list)))
        insert_data=[]
        for item in no_db_list_phones:
            insert_data.append({"phone": str(item),"keyword":str(keyword),"source_url":str(source_url),"kz_url":str(kz_url),"create_time":int(time.time())})

        if len(insert_data)>0:
            logrecord.log(f"新手机号:{str(no_db_list_phones)},记录到数据库中")
            try:
                self.session.execute(Phones.__table__.insert(),insert_data)
                self.session.commit()
            except Exception as e:
                logrecord.log(f"数据库异常:{str(e)}")
                self.session.rollback()


    # 查询需要导出的数据
    def get_export_data(self, pagesize, pageindex):
        export_phones = self.session.query(Phones).with_entities(Phones.phone, Phones.keyword,Phones.source_url,func.datetime(Phones.create_time, 'unixepoch',
                          'localtime').label('create_time_zh'))
        res = export_phones.order_by(Phones.id).limit(pagesize).offset(
            (pageindex - 1) * pagesize).all()
        return res

    # 通过关键词获取手机号关键词信息
    def get_all_by_keywords(self,keywords):
        res = self.session.query(Phones).with_entities(Phones.phone, Phones.keyword).filter(Phones.keyword.in_(keywords)).order_by(
            Phones.id).all()
        return res

    # 获取数据库中所有关键词
    def get_all_keywords(self):
        res = self.session.query(Phones).with_entities(Phones.keyword).distinct(Phones.keyword).order_by(
            Phones.id).all()
        list_data = []
        for item in res:
            list_data.append(item.keyword)
        return list_data

    # 查询短信发送记录表
    def record_sms_log_query(self, limitIndex):
        pagecount = 500
        limitnum = (limitIndex - 1) * pagecount
        res = self.session.query(PhoneSmsLogs).with_entities(
            PhoneSmsLogs.phone,
            PhoneSmsLogs.keyword,
            PhoneSmsLogs.content,
            PhoneSmsLogs.respcode,
            PhoneSmsLogs.respdesc,
            func.datetime(PhoneSmsLogs.create_time, 'unixepoch',
                          'localtime').label('create_time_zh')).order_by(
            PhoneSmsLogs.id).limit(pagecount).offset(limitnum).all()
        return res

    # 获取短信发送记录表总条数
    def get_phone_sms_log_count(self):
        res_count = self.session.query(PhoneSmsLogs).count()
        return res_count

    # 情况短信消息发送记录
    def clear_phone_sms_log_table(self):
        self.session.query(PhoneSmsLogs).delete()
        self.session.execute('update sqlite_sequence set seq=0 where name=:table',
                             params={"table": PhoneSmsLogs.__tablename__})
        self.session.commit()

    # 查询手机号短信发送记录需要导出的数据
    def get_export_phone_sms_logs_data(self, pagesize, pageindex):
        export_phone_sms_logs = self.session.query(PhoneSmsLogs).with_entities(
            PhoneSmsLogs.phone,
            PhoneSmsLogs.keyword,
            PhoneSmsLogs.content,
            PhoneSmsLogs.respcode,
            PhoneSmsLogs.respdesc,
            func.datetime(PhoneSmsLogs.create_time, 'unixepoch',
                          'localtime').label('create_time_zh'))
        res = export_phone_sms_logs.order_by(PhoneSmsLogs.id).limit(pagesize).offset(
            (pageindex - 1) * pagesize).all()
        return res

    # 写入短信发送记录
    def insert_phone_sms_logs(self,phone,keyword,content,batchno,respcode,respdesc,logid):
        try:
            logrecord.log(f"短信发送记录添加到数据库中")
            self.session.add(PhoneSmsLogs(phone=phone,keyword=keyword,content=content,batchno=batchno,respcode=respcode,respdesc=respdesc,logid=logid,create_time=int(time.time())))
            self.session.commit()
        except Exception as e:
            logrecord.log(f"短信发送记录添加到数据库异常:{str(e)}")
            self.session.rollback()

