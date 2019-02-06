import urllib.request
import re
def collect_single_info(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)"}  # 伪装浏览器请求报头
    request = urllib.request.Request(url=url, headers=headers)  # 请求服务器
    response = urllib.request.urlopen(request)  # 服务器应答
    content = response.read().decode('gbk')  # 以一定的编码方式查看源码
    pattern = re.compile('<title>[\s\S]*</title>')
    sentence = re.findall(pattern, str(content))
    pattern = re.compile('>(.*?)[(]')
    name = re.findall(pattern, sentence[0])
    name[0]='《' + name[0] + '》'
    pattern = re.compile('<td>市净率：<[\s\S]*></td>')
    body = re.findall(pattern, str(content))
    pattern = re.compile('>(.*?)<')
    stock_total = re.findall(pattern, body[0])  # 匹配>和<之间的所有信息
    stock_last = stock_total[:]
    info = name + stock_last[:2]
    if not (info[2]=='' and info[2]=='-'):
        scalar = str(info[2])
    else:
        scalar = '无信息'
    info[1] += scalar
    Name = info[0]
    ShiJingLv = info[1]
    pattern = re.compile('<td class="text-indent0" style="text-align: center;">[\s\S]*</td>')
    line = re.findall(pattern, str(content))
    pattern = re.compile('>(.*?)<')
    bk = re.findall(pattern, line[0])
    BanKuai = bk[17]

    return BanKuai, Name, ShiJingLv


