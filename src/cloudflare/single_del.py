#written by zivan 2024.5.7
#referens:
#https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-list-dns-records
#https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-delete-dns-record
#给cf一个域名加多个A记录进行负载，有的IP挂了，还要登后台删除太麻烦，所以搞个脚本，删除指定IP的A记录
#先获取zoneid下所有记录，然后匹配和输入IP相同的域名，并提交删除

import requests
import sys
import argparse

EMAIL = 'cf的邮箱'
AUTH_KEY = '全局API'
ZONE_ID = '域名zone_id'

def get_dns_records():
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Email': EMAIL,
        'X-Auth-Key': AUTH_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()['result']

def delete_dns_record(record_id):
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{record_id}"
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Email': EMAIL,
        'X-Auth-Key': AUTH_KEY
    }
    response = requests.delete(url, headers=headers)
    return response.json()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', metavar='[IP地址]',help='要删除的ip地址')
    parser.add_argument('-list', action='store_true', help='列出所有DNS记录')

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    if args.list:
        dns_records = get_dns_records()
        for record in dns_records:
            print(f"{record['name']} : {record['content']}")
    elif args.ip:
        ip_address = args.ip
        dns_records = get_dns_records()
        matched_records = [record for record in dns_records if record['content'] == ip_address]
        if matched_records:
            for record in matched_records:
                delete_result = delete_dns_record(record['id'])
                if delete_result['success']:
                    print(f"成功删除DNS记录 {record['name']},IP:{ip_address}, id是 {record['id']}")
                else:
                    print(f"删除DNS记录失败 {record['name']},IP:{ip_address}, id是 {record['id']}，错误内容为：{delete_result['errors']}")
        else:
            print(f"错误: 没有找到与 {ip_address} 匹配的DNS记录")
