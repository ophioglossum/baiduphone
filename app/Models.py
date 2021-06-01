from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,Text,REAL
Base = declarative_base()
#关键词手机号表
class Phones(Base):
    __tablename__ = 'phones'

    # 指定id映射到id字段; id字段为整型，为主键
    id = Column(Integer, primary_key=True)
    phone = Column(Text, nullable=False)
    keyword = Column(Text, nullable=False)
    source_url=Column(Text, nullable=False)
    kz_url=Column(Text, nullable=False)
    create_time = Column(Integer, nullable=False)

#短信发送记录
class PhoneSmsLogs(Base):
    __tablename__ = 'phone_sms_logs'

    # 指定id映射到id字段; id字段为整型，为主键
    id = Column(Integer, primary_key=True)
    phone = Column(Text, nullable=False)
    keyword = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    batchno = Column(Text, nullable=True)
    respcode=Column(Text, nullable=True)
    respdesc=Column(Text, nullable=True)
    logid=Column(Text, nullable=True)
    create_time = Column(Integer, nullable=False)