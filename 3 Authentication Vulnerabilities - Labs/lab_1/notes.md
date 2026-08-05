Lab#1 Username enumeration via different responses

Analysis :

    +-------------------------------------------+          +-------------------------------------------+
    | PHASE 1: Username Enumeration (Sniper)    |          | PHASE 2: Password Brute-Force (Sniper)    |
    | (Finding the Valid User)                  |          | (Cracking the Password)                   |
    |                                           |          |                                           |
    | [Burp Intruder Configuration]             |          | [Burp Intruder Configuration]             |
    | Attack Type: Sniper                       |    ->    | Attack Type: Sniper                       |
    |                                           |          |                                           |
    | Payload Position:                         |          | Payload Position:                         |
    | username=§§                               |          | password=§§                               |
    | (Password is static: "dummy")             |          | (Username is static: "wiener")            |
    |                                           |          |                                           |
    | Payload List: Candidate Usernames         |          | Payload List: Candidate Passwords         |
    | - carlos                                  |          | - 123456                                  |
    | - wiener                                  |          | - password                                |
    | - admin                                   |          | - blue                                    |
    | ...                                       |          | ...                                       |
    |                                           |          |                                           |
    | [Results Table Analysis]                  |          | [Results Table Analysis]                  |
    | Sort by: Length                           |          | Sort by: Status                           |
    |                                           |          |                                           |
    | Payload   | Length | Status | Response    |          | Payload   | Length | Status | Response    |
    | carlos    | 500    | 200    | "Invalid... |          | 123456    | 500    | 200    | "Incorrect..|
    | wiener    | 505    | 200    | "Incorrect..|    ->    | password  | 500    | 200    | "Incorrect..|
    | admin     | 500    | 200    | "Invalid... |          | blue      | 0      | 302    | (Redirect)  |
    |                                           |          |                                           |
    | >> OBSERVATION: "wiener" has DIFFERENT    |          | >> OBSERVATION: "blue" has STATUS 302     |
    |    Length & Message ("Incorrect password")|          |    (All others are 200 "Incorrect pass")  |
    |                                           |          |                                           |
    | >> RESULT: Valid Username = wiener        |          | >> RESULT: Valid Password = blue          |
    +-------------------------------------------+          +-------------------------------------------+

    +-------------------------------------------+          +-------------------------------------------+
    | FINAL STEP: Solve the Lab                 |          | VISUAL INDICATORS IN BURP                 |
    |                                           |          |                                           |
    | [Browser Login Page]                      |          | [Enumeration Phase]                       |
    | Username: wiener                          |    <-    | - Look for the UNIQUE row in "Length" col.|
    | Password: blue                            |          | - Message changes: "Invalid username"     |
    |                                           |          |   TO "Incorrect password".                |
    | [Click Login]                             |          |                                           |
    |                                           |          | [Brute-Force Phase]                       |
    | >> Redirect to: /my-account               |          | - Look for "Log out" in row res text      |
    | >> Message: "Welcome to your account!"    |          | - String found: "Log out".                | 
    |                                           |          |                                           |
    | >> LAB SOLVED                             |          | >> Success indicated by HTTP Redirect     |
    +-------------------------------------------+          +-------------------------------------------+   