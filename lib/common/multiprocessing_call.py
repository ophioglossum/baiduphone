from multiprocessing import Process

#进程启动
def run(func_callback,*args, **kwargs):
    p = Process(target=func_callback, args=args, kwargs=kwargs)
    p.start()
    return p