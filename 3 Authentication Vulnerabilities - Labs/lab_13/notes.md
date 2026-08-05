Lab#13 Broken brute-force protection, multiple credentials per request

==============================================================
 LAB: Broken Brute-Force Protection
 Multiple Credentials Per Request (ASCII Diagram)
==============================================================

          +----------------------+
          |   Open the Lab       |
          +----------+-----------+
                     |
                     v
          +----------------------+
          | Start Burp Suite     |
          | (Proxy ON)           |
          +----------+-----------+
                     |
                     v
          +----------------------+
          | Login Page           |
          | Username: carlos     |
          | Password: anything   |
          +----------+-----------+
                     |
                     v
          +----------------------+
          | Capture Request      |
          | POST /login          |
          +----------+-----------+
                     |
                     v
          +----------------------+
          | Send to Repeater     |
          +----------+-----------+
                     |
                     v
     +-----------------------------------------+
     | Original JSON                           |
     |                                         |
     | {                                       |
     |   "username":"carlos",                  |
     |   "password":"password123"              |
     | }                                       |
     +------------------+----------------------+
                        |
                        | Replace password string
                        | with an array
                        v
     +-----------------------------------------+
     | Modified JSON                           |
     |                                         |
     | {                                       |
     |   "username":"carlos",                  |
     |   "password":[                          |
     |      "123456",                          |
     |      "password",                        |
     |      "qwerty",                          |
     |      "letmein",                         |
     |      "..."                              |
     |   ]                                     |
     | }                                       |
     +------------------+----------------------+
                        |
                        v
          +----------------------+
          | Click Send           |
          +----------+-----------+
                     |
                     v
          +----------------------+
          | Response: HTTP 302   |
          | Redirect Found       |
          +----------+-----------+
                     |
                     v
          +----------------------+
          | Right Click          |
          | Show Response        |
          | in Browser           |
          +----------+-----------+
                     |
                     v
          +----------------------+
          | Copy Generated URL   |
          +----------+-----------+
                     |
                     v
          +----------------------+
          | Open URL             |
          | in Browser           |
          +----------+-----------+
                     |
                     v
          +----------------------+
          | Logged in as Carlos  |
          +----------+-----------+
                     |
                     v
          +----------------------+
          | Click My Account     |
          +----------+-----------+
                     |
                     v
          +----------------------+
          |      LAB SOLVED      |
          +----------------------+

==============================================================
Flow Summary
==============================================================

Capture Request
      │
      ▼
Send to Repeater
      │
      ▼
Replace password with array
      │
      ▼
Send Request
      │
      ▼
Receive HTTP 302
      │
      ▼
Show Response in Browser
      │
      ▼
Open Generated URL
      │
      ▼
Logged in as Carlos
      │
      ▼
My Account → Lab Solved
==============================================================