# -*- coding: utf-8 -*-
# @Time    : 2020/5/12 13:14
# @Author  : Zivan
# @Email   : aquarz@163.com
# @File    : nslk.py
# @Software: PyCharm
# 简单批处理操作
# nslookup 为macos系統的版本
# 查看不同dns解析结果

from os import popen
import re


class Nslookup():

    def __init__(self):
        self.dns_pool = {
            '114': '114.114.114.114',
            'ali': '223.5.5.5',
            'smartdns': '192.168.3.252',
            'dnspod': '119.29.29.29',
            'google': '8.8.8.8',
            'CNNIC': '1.2.4.8',
            'cloudflare': '1.1.1.1',
            '运营商': '221.179.155.177'
        }
        self.pattern = re.compile(  # 域名检查
            r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
            r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
            r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
            r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$')

    def domain_valid(self, domain):  # 校验域名
        return True if self.pattern.match(domain) else False

    def __print_line(self, msg):  # 分隔符
        print('=========%s========' % str(msg))

    def __action(self, domain, dns):  # 单dns,单域名,返回为列表，单条或多条
        cmd = 'nslookup ' + domain + ' ' + dns

        try:
            answer = popen(cmd)
            answer = answer.read()
            # 可能存在多条结果，用findall匹配多条记录
            answer = re.findall(r'Address: (.*)', answer)
        except:
            pass

        return answer

    def que(self, domain):
        for dns in self.dns_pool:
            A_answer_lst = self.__action(domain, self.dns_pool[dns])
            self.__print_line(dns)
            for i in A_answer_lst:
                print('{}解析到的地址为：{}'.format(dns, i))


if __name__ == '__main__':
    test_ob = Nslookup()
    while True:
        domain = input('域名：')
        if test_ob.domain_valid(domain):
            test_ob.que(domain)
            break
        elif domain == "q":
            print('quit Done.')
            break
        else:
            print('域名无效，请重新输入或(q)退出')
