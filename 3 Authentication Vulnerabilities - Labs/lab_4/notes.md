Lab#4 Username enumeration via subtly different responses

Target Goal : 

=================================================================================
             USERNAME ENUMERATION & PASSWORD BRUTE-FORCE WORKFLOW
=================================================================================

STEP 1: ENUMERATE THE VALID USERNAME
-----------------------------------
Capture the login request in an interception proxy (like Burp Suite) and send it 
to an automated attack tool (like Intruder). Target the username parameter.

  [ Candidate Usernames Wordlist ]
         │  (e.g., admin, carlos, user, test...)
         ▼
   ┌───────────┐      POST /login      ┌────────────────┐
   │  Attack   │ ────────────────────> │   Target Web   │
   │   Tool    │ <──────────────────── │   Application  │
   └───────────┘      HTTP Response    └────────────────┘
                             │
                             ▼
               [ Analyze Response Indicators ]
               Look for anomalies in the server replies:
               │
               ├──> Status Code Change (e.g., 200 OK vs 401 Unauthorized)
               ├──> Response Length (e.g., 3245 bytes vs 3260 bytes)
               └──> Check for the specific request wthout Error Message Subtleties:
                    ├── "Invalid username or password." 
                    └── "Invalid username or password" <── without '.' 
                    [★ SUCCESS: Username exists!]


STEP 2: BRUTE-FORCE THE PASSWORD
--------------------------------
Keep the identified username fixed. Target the password parameter using the 
second wordlist.

  [ Candidate Passwords Wordlist ]
         │  (e.g., password123, hunter2, dragon...)
         ▼
   ┌───────────┐      POST /login      ┌────────────────┐
   │  Attack   │  [username=carlos]    │   Target Web   │
   │   Tool    │  [password=§payload§] │   Application  │
   └───────────┘ ────────────────────> └────────────────┘
                             │
                             ▼
               [ Analyze Response Indicators ]
               Identify the successful authentication:
               │
               ├──> HTTP Status 302 Redirect (Redirection to dashboard)
               ├──> Session Cookie Issued (Set-Cookie: session=...)
               └──> Response Length Drop/Spike


STEP 3: ACCESS THE ACCOUNT PAGE
-------------------------------
Use the validated credentials or the active session token to view the portal.

   ┌───────────┐      GET /my-account  ┌────────────────┐
   │  Browser  │ ────────────────────> │ Successful Log │
   │           │ <──────────────────── │  Lab Solved!   │
   └───────────┘     Render Profile    └────────────────┘
=================================================================================
