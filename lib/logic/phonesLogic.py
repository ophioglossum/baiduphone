import asyncio, aiohttp, re
from lib.common import logrecord
from pyquery import PyQuery as pq

async def fetch_async(url):
    try:
        async with aiohttp.ClientSession() as session:  # 协程嵌套，只需要处理最外层协程即可fetch_async
            async with session.get(url) as resp:
                return {'html':await resp.text('gbk', 'ignore'),'url':url}  # 因为这里使用到了await关键字，实现异步，所有他上面的函数体需要声明为异步async

    except Exception as e:
        return ''

# 百度快照下载处理
def baidukz_download(urls,*args, **kwargs):
    tasks = []
    for url in urls:
        tasks.append(fetch_async(url))
    event_loop = asyncio.get_event_loop()
    results = event_loop.run_until_complete(asyncio.gather(*tasks))
    # event_loop.close()
    for ritem in results:
        yield ritem


# 正则规则获取手机号
def getPhones(html,re_match):
    # 手机号正则,"1"代表数字1开头，"[3|4|5|7|8]"代表第2位是3/4/5/7/8中任一个，"\d"代表0~9的数字，"{9}"代表按前面的规则取9次
    pattern_mob = re.compile(re_match['re'])
    # 用正则匹配html文件中的内容，匹配结果放在变量result中，结果是list形式，如果匹配到两个就这样['13699999999', '17399999999']
    result = pattern_mob.findall(html)
    new_result=[]
    # 处理替换正则
    if re_match['sub']!="":
        for item in result:
            new_result.append(re.sub(re_match['sub'], "", item))
    else:
        new_result=result
    # 返回匹配结果
    return new_result

#批量正则规则查询手机号
def getReMatchPhones(html):
    re_list=[
        {'re': '1[3|4|5|6|7|8|9]\d{9}<', 'sub': '<'},
        {'re': '>1[3|4|5|6|7|8|9]\d{9}', 'sub': '>'},
        {'re': '1[3|4|5|6|7|8|9]\d{1}-\d{4}-\d{4}', 'sub': '-'},
        {'re': '1[3|4|5|6|7|8|9]\d{1} \d{4} \d{4}', 'sub': ' '},
        {'re': ' 1[3|4|5|6|7|8|9]\d{9} ', 'sub': ' '},
        {'re': '热线：1[3|4|5|6|7|8|9]\d{9}', 'sub': '热线：'},
        {'re': '热线:1[3|4|5|6|7|8|9]\d{9}', 'sub': '热线:'},
        {'re': '手机：1[3|4|5|6|7|8|9]\d{9}', 'sub': '手机：'},
        {'re': '手机:1[3|4|5|6|7|8|9]\d{9}', 'sub': '手机:'},
        {'re': '电话：1[3|4|5|6|7|8|9]\d{9}', 'sub': '电话：'},
        {'re': '电话:1[3|4|5|6|7|8|9]\d{9}', 'sub': '电话:'},
        {'re': 'TEL：1[3|4|5|6|7|8|9]\d{9}', 'sub': 'TEL：'},
        {'re': 'TEL:1[3|4|5|6|7|8|9]\d{9}', 'sub': 'TEL:'},
        {'re': 'tel：1[3|4|5|6|7|8|9]\d{9}', 'sub': 'tel：'},
        {'re': 'tel:1[3|4|5|6|7|8|9]\d{9}', 'sub': 'tel:'},
    ]
    phones_list=[]
    for item in re_list:
        res=getPhones(html,item)
        # print(res)
        phones_list=phones_list+res

    #手机号去重复
    new_phones_list=list(set(phones_list))
    #维持数据顺序一致
    new_phones_list.sort(key=phones_list.index)
    return new_phones_list

# 获取快照中来源地址
def getSourceDomain(html):
    try:
        doc=pq(html)
        source_url=doc('#bd_snap_note>a').attr('href')
        return source_url
    except Exception as e:
        return ''

# 获取手机号入口
def run(urls):
    logrecord.log(f'检索的快照页为:{urls}')
    phones_list=[]
    res = baidukz_download(urls)
    for item in res:
        if 'html' in item:
            html = item['html']
            phones_temp = getReMatchPhones(html)
            source_url = getSourceDomain(html)
            if not source_url:
                source_url = item['url']
            kz_url = item['url']
            phones_list.append({'phones': phones_temp, 'source_url': source_url, 'kz_url': kz_url})
    return phones_list