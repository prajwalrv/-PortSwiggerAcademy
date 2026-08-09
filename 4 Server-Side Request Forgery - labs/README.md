
## SSRF - SERVER SIDE REQUEST FORGERY

## What is SSRF
```text
===================================================================================================================
                                WHAT IS SERVER-SIDE REQUEST FORGERY (SSRF)?
===================================================================================================================


                                    Normal Architecture
                                    -------------------


                              You (User/Attacker)
                                      |
                                      | 1. Send Request
                                      |
                                      v
                        +-------------------------------+
                        |                               |
                        |      Web Application          |
                        |                               |
                        +---------------+---------------+
                                        |
                                        |
                     Server has access to systems that
                     users CANNOT access directly.
                                        |
                                        |
             ----------------------------------------------------------
             |                         |                              |
             |                         |                              |
             v                         v                              v

      +----------------+      +------------------+          +------------------+
      | Internal API   |      | Internal Database|          | Mail Service     |
      |                |      |                  |          |                  |
      +----------------+      +------------------+          +------------------+

             |
             |
             +------ Accessible ONLY from the server's network ------+

                    (Private Network / Corporate LAN / VPN)


===========================================================================================================
IMPORTANT
===========================================================================================================

The user DOES NOT have direct access to these internal systems.

To communicate with them, you must:

    ✔ Be inside the corporate network
                 OR
    ✔ Connect through the company's VPN

Therefore,

User
   X-------> Internal API        (Blocked)

User
   X-------> Database            (Blocked)

User
   X-------> Mail Server         (Blocked)

Only the Web Application can talk to them.


===========================================================================================================
Normal Request Flow
===========================================================================================================


User
   |
   | Request Product Details
   |
   v

Web Application
   |
   | Fetch data from Internal API
   |
   v

Internal API
   |
   | Returns Product Data
   |
   v

Web Application
   |
   | Sends Response
   |
   v

User


The application acts as a TRUSTED MIDDLEMAN.


===========================================================================================================
Where SSRF Happens
===========================================================================================================


Suppose the application allows the user to specify a URL.


User Input

https://example.com/image.jpg


        |
        v

Web Application

        |
        | Server fetches the URL
        |
        v

Returns Image


Everything works correctly.



===========================================================================================================
What if the URL is User-Controlled?
===========================================================================================================


Instead of

https://example.com/image.jpg


Attacker sends


http://internal-api.company.local/admin


        |
        v

Web Application

        |
        | Backend trusts the supplied URL
        |
        | Server makes the request
        |
        v

Internal API

        |
        | Returns Secret Data
        |
        v

Web Application

        |
        | Sends Response back
        |
        v

Attacker


The attacker never directly accessed the Internal API.

The WEB APPLICATION did it on the attacker's behalf.


===========================================================================================================
SSRF IN ONE SENTENCE
===========================================================================================================


                     Attacker
                         |
                         |
                         v
               Web Application
                         |
                         |  "Please fetch this URL for me."
                         |
                         v
        +-----------------------------------------+
        | Internal APIs                           |
        | Databases                               |
        | Mail Servers                            |
        | Cloud Metadata Services                 |
        | Third-Party APIs                        |
        +-----------------------------------------+

The vulnerable application becomes a PROXY that fetches resources
the attacker cannot normally reach.


===========================================================================================================
KEY TAKEAWAY
===========================================================================================================

Normal User
      |
      | Can access only
      v
Web Application

Web Application
      |
      | Has access to
      v
+--------------------------------------+
| Internal APIs                        |
| Microservices                        |
| Databases                            |
| Third-Party Services                 |
| Cloud Resources                      |
+--------------------------------------+

SSRF allows an attacker to abuse the Web Application's network access
and make it communicate with systems that the attacker cannot reach directly.

===================================================================================================================
```

## SSRF Vulnerability Types :

## 1. Basic SSRF against the local server :
```text
================================================================================
                         THE CORE SSRF IDEA
================================================================================

┌──────────────┐        ┌──────────────────┐        ┌──────────────────┐
│     YOU      │        │   WEB SERVER     │        │     LOCALHOST    │
│              │        │  Vulnerable App  │        │                  │
│ Burp /       │───────►│                  │───────►│   /admin         │
│ Browser      │        │  stockApi =      │        │   127.0.0.1      │
└──────────────┘        │  localhost/admin  │        └──────────────────┘
                        └──────────────────┘
                              │
                              │
                              │ SSRF
                              │
                              ▼
                     Server accesses the
                     internal resource
                     on your behalf.
================================================================================
```

## 2. Basic SSRF against the INTERNAL BACK-END :
```text
================================================================================
                THE CORE SSRF IDEA — INTERNAL BACK-END
================================================================================

┌─────────┐       ┌────────────────┐       ┌────────────────────┐
│   YOU   │──────►│  WEB SERVER    │──────►│ 192.168.0.X:8080   │
│         │       │                │       │                    │
│ Burp    │       │ "Fetch this    │       │     /admin         │
│         │       │  URL for me"   │       │                    │
└─────────┘       └────────────────┘       └────────────────────┘
                         │
                         │
                         ▼
                       SSRF

       The vulnerable server becomes your access point
       into the internal network.

================================================================================
                       DISCOVERY FLOW
================================================================================

┌──────────────┐     ┌──────────────────┐     ┌──────────────────────┐
│ stockApi     │────►│ 192.168.0.1:8080 │────►│ Is this the target?  │
│              │     └──────────────────┘     └──────────────────────┘
│ 192.168.0.X  │
│      :8080   │────► 192.168.0.2:8080 ────► Check response
│              │
│ X = 1 → 255  │────► 192.168.0.3:8080 ────► Check response
│              │
│              │────►       ...         │
│              │
│              │────► 192.168.0.5:8080 ────► ADMIN FOUND
└──────────────┘
================================================================================
```

## 3. BLACK LIST BASED INPUT FILTER SSRF
```text
================================================================================
              SSRF FILTER BYPASS — ALTERNATE IP REPRESENTATION
================================================================================


┌──────────────────┐       ┌──────────────────────┐       ┌─────────────────────┐
│       YOU        │       │  SECURITY GUARD /    │       │    PUBLIC WEB APP   │
│                  │       │       FILTER         │       │                     │
│ Want to access   │──────►│ Scans your payload   │──────►│ Receives the        │
│ 127.0.0.1        │       │ for forbidden IPs    │       │ allowed request     │
│                  │       │                      │       │                     │
│ But 127.0.0.1    │       │ "127.0.0.1" ❌       │       │ http://127.1        │
│ is BANNED!       │       │ "localhost" ❌       │       │                     │
│                  │       │                      │       │                     │
│ Disguise it as:  │       │ Not found! ✓         │       │ OS resolves the     │
│                  │       │                      │       │ decimal IP back to  │
│ 2130706433       │       │ "Looks clean!" ✓     │       │ 127.0.0.1           │
│                  │       │                      │       │                     │
│ Payload:         │       └──────────────────────┘       └──────────┬──────────┘
│                  │                                                 │
│ http://          │                                                 │
│ 127.1            │                                                 │
└──────────────────┘                                                 │
                                                                     │
                                                                     │ SSRF
                                                                     │
                                                                     ▼
                                                         ┌─────────────────────┐
                                                         │ INTERNAL SERVICE    │
                                                         │    / LOCALHOST      │
                                                         │                     │
                                                         │    127.0.0.1        │
                                                         │                     │
                                                         │ Receives the        │
                                                         │ connection from     │
                                                         │ the Web App         │
                                                         └─────────────────────┘
================================================================================
```

## 5. SSRF WITH WHITELIST + URL PARSER + DOUBLE DECODING
```text
================================================================================
       THE FLOW: SSRF WITH WHITELIST + URL PARSER + DOUBLE DECODING
================================================================================


┌──────────────────┐     ┌────────────────────┐     ┌──────────────────────┐
│       YOU        │     │  WHITELIST FILTER  │     │    PUBLIC WEB APP    │
│                  │     │                    │     │                      │
│ Want to reach:   │────►│ Checks the         │────►│ Receives the URL     │
│                  │     │ hostname against   │     │ after it passes the  │
│ localhost/admin  │     │ the trusted list   │     │ whitelist            │
│                  │     │                    │     │                      │
│ Direct attempt:  │     │ localhost ❌       │     │ Backend parses and   │
│ 127.0.0.1        │     │ 127.0.0.1 ❌       │     │ decodes the URL      │
│                  │     │                    │     │ again                │
│ Rejected ❌      │     │ Need a trusted     │     │                      │
│                  │     │ hostname visible   │     │ %2523 → %23 → #      │
│ Then discover:   │     │ to the validator   │     │                      │
│                  │     │                    │     │ URL is interpreted   │
│ username@        │     │ stock.weliketoshop │     │ differently from     │
│ trusted-host     │     │ .net = ✔ Allowed   │     │ the whitelist        │
└──────────────────┘     └────────────────────┘     └──────────┬───────────┘
                                                               │
                                                               │
                                                               │ SSRF
                                                               ▼
                                                    ┌────────────────────────┐
                                                    │    INTERNAL SERVICE    │
                                                    │                        │
                                                    │       localhost        │
                                                    │                        │
                                                    │         /admin         │
                                                    │                        │
                                                    │ /admin/delete?         │
                                                    │ username=carlos        │
                                                    └────────────┬───────────┘
                                                                 │
                                                                 ▼
                                                          ┌─────────────┐
                                                          │   CARLOS    │
                                                          │   DELETED   │
                                                          │      ✔      │
                                                          └─────────────┘


================================================================================
                              PAYLOAD EVOLUTION
================================================================================

┌──────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│ Direct Target    │────►│ Parser Discovery │────►│ Double Encoding     │
│                  │     │                  │     │                     │
│ localhost/admin  │     │ username@        │     │ # → %23 → %2523     │
│                  │     │ trusted-host     │     │                     │
│ ❌ Blocked       │     │                  │     │ Validator sees      │
│                  │     │ ✔ Accepted       │     │ trusted hostname    │
└──────────────────┘     └──────────────────┘     └──────────┬──────────┘
                                                             │
                                                             ▼
                                                  ┌─────────────────────────┐
                                                  │     FINAL PAYLOAD       │
                                                  │                         │
                                                  │ http://localhost:80     │
                                                  │ %2523@stock.            │
                                                  │ weliketoshop.net/       │
                                                  │ admin/delete?           │
                                                  │ username=carlos         │
                                                  └────────────┬────────────┘
                                                               │
                                                               ▼
                                                    ┌─────────────────────┐
                                                    │    WHITELIST        │
                                                    │                     │
                                                    │ Trusted hostname ✔  │
                                                    │                     │
                                                    │ Request allowed     │
                                                    └──────────┬──────────┘
                                                               │
                                                               ▼
                                                    ┌─────────────────────┐
                                                    │      WEB APP        │
                                                    │                     │
                                                    │ Double decoding     │
                                                    │                     │
                                                    │ %2523 → %23 → #     │
                                                    └──────────┬──────────┘
                                                               │
                                                               │ Server-side
                                                               │ request
                                                               ▼
                                                    ┌─────────────────────┐
                                                    │      LOCALHOST      │
                                                    │                     │
                                                    │ /admin/delete       │
                                                    │ ?username=carlos    │
                                                    └─────────────────────┘
================================================================================
```

## 4. SSRF BYPASS VIA OPEN REDIRECTION VULNERABILITY

```text
================================================================================
          THE FLOW: SSRF BYPASS VIA OPEN REDIRECTION VULNERABILITY
================================================================================


┌──────────────────┐     ┌────────────────────┐     ┌─────────────────────────┐
│       YOU        │     │  SECURITY GUARD /  │     │      PUBLIC WEB APP     │
│                  │     │       FILTER       │     │    OPEN REDIRECTOR      │
│ Want to reach:   │────►│                    │────►│                         │
│                  │     │ Checks the FIRST   │     │ Receives the allowed    │
│ 192.168.0.1      │     │ destination URL    │     │ redirect request        │
│                  │     │                    │     │                         │
│ Direct access    │     │ "Does it point to  │     │ Redirect parameter:     │
│ is blocked ❌    │     │  our trusted site?"│     │                         │
│                  │     │                    │     │ ?url=http://            │
│ Instead use the  │     │ target.com ✔       │     │ 192.168.0.1             │
│ trusted site's   │     │                    │     │                         │
│ redirector       │     │ "Looks safe!" ✔    │     │ Server processes the    │
│                  │     │                    │     │ redirect instruction    │
└──────────────────┘     └────────────────────┘     └────────────┬────────────┘
                                                                 │
                                                                 │ 302 Redirect
                                                                 │
                                                                 │ New request
                                                                 ▼
                                                    ┌─────────────────────────┐
                                                    │     INTERNAL SERVICE    │
                                                    │                         │
                                                    │      192.168.0.1        │
                                                    │                         │
                                                    │   Internal resource     │
                                                    │                         │
                                                    │        ✔ REACHED        │
                                                    └─────────────────────────┘

================================================================================
                              WHAT HAPPENED?
================================================================================

┌──────────────────┐     ┌──────────────────┐     ┌─────────────────────────┐
│ Direct Target    │────►│      FILTER      │────►│        BLOCKED           │
│                  │     │                  │     │                         │
│ 192.168.0.1      │     │ Internal IP ❌   │     │        ❌                │
└──────────────────┘     └──────────────────┘     └─────────────────────────┘


Instead:


┌──────────────────┐     ┌──────────────────┐     ┌─────────────────────────┐
│      YOU         │────►│      FILTER      │────►│    TRUSTED REDIRECTOR   │
│                  │     │                  │     │                         │
│ target.com       │     │ target.com ✔     │     │ ?url=192.168.0.1        │
│                  │     │                  │     │                         │
│ Looks trusted    │     │ ALLOWED ✔        │     │        │                │
└──────────────────┘     └──────────────────┘     └────────┼────────────────┘
                                                           │
                                                           │ 302
                                                           ▼
                                                  ┌─────────────────────┐
                                                  │   192.168.0.1       │
                                                  │                     │
                                                  │ INTERNAL TARGET     │
                                                  └─────────────────────┘
================================================================================
```

## 6. BLIND OUT OF BAND SSRF
```text
================================================================================
          THE ACTUAL NETWORK FLOW: STANDARD OOB SSRF (INTERNAL TARGET)
================================================================================


┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│        YOU           │     │    PUBLIC WEB APP    │     │   INTERNAL SERVICE   │
│                      │     │                      │     │                      │
│ Send a request to    │────►│ Receives your        │────►│ Receives the request │
│ the public web app   │     │ attacker-controlled  │     │ from the web app     │
│                      │     │ payload              │     │                      │
│ Payload contains:    │     │                      │     │ Processes the data   │
│                      │     │ Acts as the bridge   │     │ you injected         │
│ http://your-public-  │     │ into the internal    │     │                      │
│ server.com           │     │ network              │     │ "I need to fetch     │
│                      │     │                      │     │  this external URL"  │
│ "Make the internal   │     │ Server-side request  │     │                      │
│ service process      │     │                      │     │ Opens its own        │
│ this URL"            │     │                      │     │ outbound connection  │
└──────────────────────┘     └──────────────────────┘     └──────────┬───────────┘
                                                                     │
                                                                     │
                                                                     │ Outbound
                                                                     │ request
                                                                     ▼
                                                        ┌──────────────────────────┐
                                                        │ YOUR PUBLIC SERVER       │
                                                        │                          │
                                                        │     OOB TRAP             │
                                                        │                          │
                                                        │ Receives connection      │
                                                        │ from the Internal        │
                                                        │ Service                  │
                                                        │                          │
                                                        │ Logs:                    │
                                                        │                          │
                                                        │ "Someone connected!"     │
                                                        │                          │
                                                        │ Source = Internal IP     │
                                                        └──────────────────────────┘
================================================================================
                         WHY IT IS CALLED "BLIND" SSRF
================================================================================

        NORMAL SSRF

        YOU ───► WEB APP ───► INTERNAL TARGET
                         │
                         └── Response comes back to you


        BLIND / OOB SSRF

        YOU ───► WEB APP ───► INTERNAL SERVICE ───► YOUR SERVER
                                                        │
                                                        ▼
                                                   "I GOT A HIT!"


        You may NOT see the internal response directly.

        Instead, you confirm that the internal system made
        a connection by observing the callback to your server.
================================================================================
```
## 7. SHELLSHOCK FLAW WITH BLIND OUT OF BAND SSRF
================================================================================
          THE "PROXY MESSAGE" GAME: BLIND SSRF + SHELLSHOCK
================================================================================
```text
 STEP 1: Handing the sealed letter to the middleman (Blind SSRF)
 ┌──────────────┐     1. "Take this letter to the     ┌───────────────────────┐
 │   Attacker   │         internal classroom"         │  Vulnerable Server    │
 │    (You)     │ ──────────────────────────────────► │  (The Principal)      │
 └──────────────┘                                     └───────────────────────┘
                                                                  │
                                                                  │ 2. Delivers the
                                                                  │    letter inside
                                                                  ▼
                                                      ┌───────────────────────┐
                                                      │  Internal Computer    │
                                                      │  (The Glitchy Robot)  │
                                                      └───────────────────────┘


 STEP 2: The Glitchy Robot reads the secret phrase and triggers (Shellshock)
 The letter says: "Glitch Code! Run this command: Check your own username 
                   and send it to http://my-trap.com"

 ┌───────────────────────┐
 │  Internal Computer    │ ─── 3. Robot breaks down, reads its username,
 └───────────────────────┘        and runs the system command.
             │
             │ 4. Sneaks over to the window and
             │    sends a signal to the internet...
             ▼
 ┌───────────────────────┐
 │     Your OOB Trap     │ ─── 5. "I see the message!" ───► [ You see it ]
 │   (Across the Street) │        Log shows: "Incoming ping from 'Admin'!"
 └───────────────────────┘
```