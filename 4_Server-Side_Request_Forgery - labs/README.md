
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