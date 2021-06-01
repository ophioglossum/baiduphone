from config import database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.pool import QueuePool
#数据库基础类
class DBbase():
    def __init__(self):
        self.engine = create_engine(
            database.DB_HOST,
            poolclass=QueuePool,
            max_overflow=0,  # 超过连接池大小外最多创建的连接
            pool_size=5,  # 连接池大小
            pool_timeout=30,  # 池中没有线程最多等待的时间
            pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
            echo=database.DB_DEBUG,
            echo_pool=database.DB_DEBUG
        )
        # engine是2.2中创建的连接
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = scoped_session(self.DBSession)

    def __del__(self):
        self.session.remove()
        self.engine.dispose()

    #获取一个新的连接池
    def _get_new_session(self):
        # 创建Session类实例
        new_session = scoped_session(self.DBSession)
        return new_session