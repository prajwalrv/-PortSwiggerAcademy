Lab#1 - Broken Acces Control - Unprotected admin functionality - Predictable location

Target Goal - FInd the admin pannel & delete the user carlos

Manual PenTest via burpsuite :

    1. Setup burpsuite proxy ip : 127.0.0.1 on port : 8080
    2. Now open burpsuite and go to proxies tab to turn on intercept
    3. manipulate homepage url --> /administrator-panel
    4. You will see this wxact get request send it to repeater & click send
    4. you will be loged on to admin page
    5. Now you will see two users delete the user carlos using delete button
        
        URL : GET https://0a7b00ff049c8bc982ba10a200c200a0.web-security-academy.net/adminstrator-panel HTTP/2 

        Response : status code 200 for both admin page access & deleting user carlos.


Concept : Unprotected admin functionality
    At its most basic, vertical privilege escalation arises where an application does not enforce any protection for sensitive functionality. For example, administrative functions might be linked from an administrator's welcome page but not from a user's welcome page. However, a user might be able to access the administrative functions by browsing to the relevant admin URL.

    For example, a website might host sensitive functionality at the following URL: https://insecure-website.com/admin

    This might be accessible by any user, not only administrative users who have a link to the functionality in their user interface. In some cases, the administrative URL might be disclosed in other locations, such as the robots.txt file: https://insecure-website.com/robots.txt

    Even if the URL isn't disclosed anywhere, an attacker may be able to use a wordlist to brute-force the location of the sensitive functionality. 