#written by zivan on 2024.5.7
#referens:https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-create-dns-record
#为了方便给cdn域名批量添加测试好的A记录
#用ipinfo.io检测出IP所在地和ASN号添加到备注中
#测试好proxyIP后，一行一个写入proxyip.txt内，执行脚本自动添加至cf的A记录中
#cloudns.org的域名要做双向解析才能生效，所以在cf中增加了a记录后，可以用变通方法使用
#加后缀 cdn.yourname.cloudns.org.cdn.cloudflare.net 就可以实时解析到地址了，反正只是为了解析用

import requests
import json
import time

EMAIL = 'cf邮箱'
AUTH_KEY = 'dashboard的全局API'
ZONE_ID = '域名的zone_id'
DOMAIN = '子域名'

headers = {
    'Content-Type': 'application/json',
    'X-Auth-Email': EMAIL,
    'X-Auth-Key': AUTH_KEY,
}

def read_ips(file):
    with open(file, "r") as f:
        ip_list = f.readlines()
    return ip_list


def get_ip_info(ip):
    headers = {
        'User-Agent': 'curl/8.4.0',
    }
    response = requests.get('https://ipinfo.io/{}'.format(ip.strip()), headers=headers)
    data = response.json()
    return data


def add_dns_record(comment, ip):
    url = f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records'
    data = {
        "content": ip.strip(),
        "name": DOMAIN,
        "proxied": False,
        "type": "A",
        "comment": comment,
        "ttl": 1,#auto=1
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


def main():
    ips = read_ips("proxyip.txt")

    for ip in ips:
        ip_info = get_ip_info(ip)
        comment = ip_info['org'].split(',')[0] + '@' + ip_info['country'] + ',' + ip_info['city'] + ' Commit By Script'

        response_data = add_dns_record(comment, ip)
        if response_data['success']:
            print('Added record for IP Address: {} successfully'.format(ip))
        else:
            print('Adding record for IP Address: {} failed. Response: {}'.format(ip, response_data))
        time.sleep(3)


if __name__ == "__main__":
    main()
