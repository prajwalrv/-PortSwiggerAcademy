Lab#1 - Broken Acces Control - Unprotected admin functionality

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