from lib.common import logrecord,list_to_children
from lib.logic import phonesLogic
from app.Services.DbService import DbService
from app.Services.BaiduKeyWordSearch import BaiduKeyWordSearch
#百度关键词处理处理
def run(*args, **kwargs):
    queue_info = kwargs['queue_info']
    queue_info.put({'status': 1, 'message': '正在整理数据,这可能会花费些许时间,请不要关闭程序并赖心等待...'})  # 刷新数据表
    keywords= kwargs['keywords']
    dbService=DbService()
    baiduSearch=BaiduKeyWordSearch()
    for item in keywords:
        queue_info.put({'status': 1, 'message': f'正在查询关键词【{item}】,请稍等...'})  # 刷新数据表
        kz_list_urls=baiduSearch.run_start(item)
        phones_list=phonesLogic.run(kz_list_urls)
        for iphone_item in phones_list:
            phones=iphone_item['phones']
            source_url = iphone_item['source_url']
            kz_url = iphone_item['kz_url']
            keyword = item
            no_repeat_result_list_children = list_to_children.list_of_groups(phones, 900)
            for rhones in no_repeat_result_list_children:
                dbService.set_phones_to_db(phones=rhones,source_url=source_url,kz_url=kz_url,keyword=keyword)
        queue_info.put({'status': 2, 'message': ''})  # 刷新数据表
    queue_info.put({'status': 3, 'message': '检测完成!'})  # 刷新数据表