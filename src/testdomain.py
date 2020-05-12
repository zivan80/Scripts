# -*- coding: utf-8 -*-
# @Time    : 2020/5/6 16:13
# @Author  : Zivan
# @Email   : aquarz@163.com
# @File    : testdomain.py
# @Software: PyCharm

#利用dig命令，批量测试dns的速度
from os import popen
from re import compile,match

class DNS_Test:

    def __init__(self):
        self.dns_list = {#dns池
            'dnspod' : '119.29.29.29',
            'alibaba': '223.5.5.5',
            '114'    : '114.114.114.114',
            # 'CNNIC' :   '1.2.4.8',
        }
        self.pattern = compile( #域名检查
            r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
            r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
            r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
            r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$' )

    """取延迟时间,一个dns一个url 测5次，取平均值，返回内容dns ,url, 5次均值"""
    def __query_delay(self, dns, url) :
        #拼接dig命令
        dig_cmd = 'dig @'+ dns +' '+ url

        #用os执行
        count = 0#计数器
        self.score = []#跑分池
        while count < 5:  # 取5次，算平均值
            dig_resp = popen(dig_cmd)
            dig_delay_line = dig_resp.readlines()[-5]  # 取到需要的内容，倒数第5行
            dig_delay = dig_delay_line.split()[3]  # 切字符串，只取数值
            self.score.append(int(dig_delay))
            count += 1

        avg = sum(self.score) / len(self.score)#求平均值
        return dns,url,avg

    def domain_valid(self,domain):#校验域名
        return True if self.pattern.match(domain) else False

    def test_process(self,domain):
        best = {}
        self.__print_line('对:{}进行测试'.format(domain))
        for dns in self.dns_list:
            d,u,delay = self.__query_delay(self.dns_list[dns],domain)
            print('通过{}:{} 测试 {} 5次平均 {} 毫秒'.format(dns, d, u, delay))
            best[dns] = delay#记录一下结果，取最佳dns用
            self.__print_line('5次结果为：{0[0]} ms, {0[1]} ms, {0[2]} ms, {0[3]} ms, {0[4]} ms'.format(self.score))

        best_delay = min(best.values()) #取字典value中最小的延迟
        best_dns = ''.join([k for k,v in best.items() if v == best_delay ])#取字典中最小延迟的dns名称

        print('⭐本次测试最快的DNS为：{}:{} 延迟{}毫秒'.format(best_dns,
                                                 self.dns_list[best_dns],
                                                 best_delay)
              )

    def __print_line(self,msg):
        print('=========%s========' % str(msg))

if __name__ == '__main__':
    test_ob = DNS_Test()
    while True:
        domain = input('域名：')
        if test_ob.domain_valid(domain):
            test_ob.test_process(domain)
            break
        elif domain == "q":
            print('quit Done.')
            break
        else:
            print('域名无效，请重新输入或(q)退出')
