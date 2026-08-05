Lab#3 - Broken Acces Control - Parameter-based access control methods

    This lab has an admin panel at /admin, which identifies administrators using a 'forgeable cookie'.

    -> Solve the lab by accessing the admin panel and using it to delete the user carlos.

    -> You can log in to your own account using the following credentials: wiener:peter

Analysis : 



Target Goal - FInd the admin pannel & delete the user carlos

Manual PenTest via burpsuite :

    1. Setup burpsuite proxy ip : 127.0.0.1 on port : 8080
    2. Now open burpsuite and go to proxies tab to turn on intercept
    3. For this lab they have given a cred to login, While login highlight that particular login request and chek its response where it sets two cookies :
        
        - set-cookie: Admin=false
        - set-cookie: session=___session_token__
        
        use it and login to that account.
        URL : GET https://0a7b00ff049c8bc982ba10a200c200a0.web-security-academy.net/admin-ku7xaw HTTP/2 

    4. After logged in open the inspect tab and go storage 
        --> Set cookies - 
                Admin=false --> Admin=true
       refresh the page and click myaccount.

    5. now delete usr carlos

    Response : status code 200 for both admin page access & deleting user carlos.

Concept : Parameter-based access control methods

    Some applications determine the user's access rights or role at login, and then store this information in a user-controllable location. This could be:

        A hidden field.
        A cookie.
        A preset query string parameter.

    The application makes access control decisions based on the submitted value. For example:
    https://insecure-website.com/login/home.jsp?admin=true
    https://insecure-website.com/login/home.jsp?role=1

    This approach is insecure because a user can modify the value and access functionality they're not authorized to, such as administrative functions.


wiener:peter