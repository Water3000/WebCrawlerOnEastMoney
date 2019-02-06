import single
import urllib
import re
from stock import Stock
import datetime
import os
from collections import OrderedDict
import json

now = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')[:10]
need_update = not os.path.isfile('data/'+now+'.json')
#### 更新当日数据 ####
if need_update:
    print('准备更新今日数据...')
    whole_stacks_url = 'http://quote.eastmoney.com/stocklist.html'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)"}
    request = urllib.request.Request(url=whole_stacks_url, headers=headers)
    response = urllib.request.urlopen(request)
    whole_content = response.read().decode('gbk')
    # 上海股票
    # 获取全部数据
    pattern = re.compile(
        '<div class="sltit"><a name="sh"/>上海股票</div>[\s\S]*<div class="sltit"><a name="sz"/>深圳股票</div>')
    content = re.findall(pattern, str(whole_content))
    pattern = re.compile('">(.*?)</a></li>')
    nameNcode = re.findall(pattern, content[0])
    pattern = re.compile('[(](.*?)[)]')
    orig_codes = re.findall(pattern, content[0])
    pattern = re.compile('href="(.*?)"')
    orig_links = re.findall(pattern, content[0])
    # 筛选
    codes = []
    links = []
    for num in range(len(orig_codes)):
        if str(orig_codes[num])[0] == '6':
            codes.append(orig_codes[num])
            links.append(orig_links[num])
    print('开始获取股票数据,请稍候...')
    # 访问并获取行业板块和市净率
    stocks = OrderedDict()
    cnt = 0
    for link in links:
        cnt += 1
        print('正在获取', cnt, '/', len(codes), '只股票的数据...')
        B, N, J = single.collect_single_info(link)
        stock = Stock(N, B, J)
        if stock.bankuai in stocks:
            stocks[stock.bankuai].append(stock.__dict__)
        else:
            stocks[stock.bankuai] = [stock.__dict__]
    print('=====今日数据获取完成,进行存储...=====')
    json_str = json.dumps(stocks)
    with open('data/'+now+'.json','w') as json_file:
        json_file.write(json_str)
    print('=====存储完成,请开始使用.=====')
else:
    print('数据已经最新,请开始使用.')
print()
#### 进入使用 ####
date = input('请输入想要查看的日期:(日期格式: 2019-01-10 ;或直接输入 日 查看今天信息)')
if date == '日':
    file_name = 'data/'+now+'.json'
else:
    file_name = 'data/'+date+'.json'
#从本地json读取数据
date_stocks = {}
with open(file_name, 'r') as file:
    line = file.readline()
    json_data = json.loads(line)
for key in json_data:
    for obj_dict in json_data[key]:
        stk = Stock()
        stk.__dict__ = obj_dict
        if stk.bankuai in date_stocks:
            date_stocks[stk.bankuai].append(stk)
        else:
            date_stocks[stk.bankuai] = [stk]
print()
print()
print("所有行业板块分类如下:(其中 - 代表网站信息缺失,原因可能是股票退市或者未上市等,具体原因需手动进入网站查看.)")
print(date_stocks.keys())
bk = input('请输入想要查看的行业板块(或输入 退出 后退出程序.):')
while bk!='退出':
    print('=======================================')
    if bk in date_stocks.keys():
        date_stocks[bk].sort(key=Stock.SJL)
        for one in date_stocks[bk]:
            one.output()
        print('*按照递增顺序排列.*')
    else:
        print("无此行业!")
    print('=======================================')
    print()
    print("所有行业板块分类如下:(其中 - 代表网站信息缺失,原因可能是股票退市或者未上市等,具体原因需手动进入网站查看.)")
    print(date_stocks.keys())
    bk = input('*请继续输入想要查看的行业板块(或输入 退出 后退出程序.):')
print('已退出!')



# single_url = 'http://quote.eastmoney.com/sh600163.html'  # 目标网址
# B, N, J = single.collect_single_info(single_url)
# single_stock = Stock(N, B, J)
# single_stock.output()
