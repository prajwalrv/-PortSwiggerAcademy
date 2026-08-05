Lab#3 Password reset broken logic

Target Goal : 
    +-----------------------------------------------------------------------+
    | LAB SCENARIO: Vulnerable Password Reset                               |
    +-----------------------------------------------------------------------+
    |                                                                       |
    | [ OBJECTIVE ]                                                         |
    | This lab's password reset functionality is vulnerable.                |
    | To solve the lab, reset Carlos's password, then log in                |
    | and access his "My account" page.                                     |
    |                                                                       |
    +-----------------------------------------------------------------------+
    |                                                                       |
    | [ CREDENTIALS PROVIDED ]                                              |
    |                                                                       |
    | YOUR ACCOUNT (Attacker):                                              |
    | Username: wiener                                                      |
    | Password: peter                                                       |
    |                                                                       |
    | VICTIM ACCOUNT (Target):                                              |
    | Username: carlos                                                      |
    | (Password is unknown and must be reset)                               |
    |                                                                       |
    +-----------------------------------------------------------------------+
    |                                                                       |
    | [ THE CHALLENGE ]                                                     |
    |                                                                       |
    | 1. You have valid credentials for your own account ('wiener').        |
    | 2. You know the victim's username ('carlos') but not their password.  |
    | 3. The password reset mechanism contains a security flaw.             |
    |                                                                       |
    | >> TASK: Exploit the vulnerability to take over 'carlos' account.     |
    |                                                                       |
    +-----------------------------------------------------------------------+   

Exploit steps :

    +-----------------------------------------------------------------------+
    | LAB INSTRUCTIONS: Password Reset Token Validation Flaw                |
    +-----------------------------------------------------------------------+
    |                                                                       |
    | [ STEP 1: Analyze Normal Flow ]                                       |
    | 1. Click "Forgot your password?" and enter YOUR username.             |
    | 2. Open the Email client, click the reset link, and set a password.   |
    | 3. In Burp Proxy > HTTP history, study the reset requests.            |
    |    - Observe: Token is in the URL query parameter.                    |
    |    - Observe: POST request contains 'username' as hidden input.       |
    | 4. Send the POST /forgot-password request to Burp Repeater.           |
    |                                                                       |
    | [ STEP 2: Verify the Vulnerability ]                                  |
    | 1. In Burp Repeater, DELETE the 'temp-forgot-password-token' value:   |
    |    - Remove it from the URL query string.                             |
    |    - Remove it from the request body.                                 |
    | 2. Send the request.                                                  |
    |    >> RESULT: Password reset STILL succeeds.                          |
    |    >> CONFIRMATION: The server is NOT validating the token.           |
    |                                                                       |
    | [ STEP 3: Exploit the Flaw (Account Takeover) ]                       |
    | 1. In the browser, request a NEW password reset (to get a fresh req). |
    | 2. Send the new POST request to Burp Repeater.                        |
    | 3. Modify the request:                                                |
    |    - DELETE the 'temp-forgot-password-token' (URL & Body).            |
    |    - CHANGE the 'username' parameter to: carlos                       |
    |    - SET the 'password' parameter to: [YourChosenPassword]            |
    | 4. Send the request.                                                  |
    |                                                                       |
    | [ STEP 4: Solve the Lab ]                                             |
    | 1. Log in to Carlos's account using the new password.                 |
    | 2. Click "My account".                                                |
    |    >> RESULT: Lab Solved.                                             |
    |                                                                       |
    +-----------------------------------------------------------------------+   