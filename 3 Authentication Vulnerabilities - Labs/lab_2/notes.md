Lab#2 2FA simple bypass

Target Goal : 

    +-----------------------------------------------------------------------+
    | LAB SCENARIO: 2FA Bypass via Brute-Force                              |
    +-----------------------------------------------------------------------+
    |                                                                       |
    | [ OBJECTIVE ]                                                         |
    | This lab's two-factor authentication can be bypassed.                 |
    | You have already obtained a valid username and password,              |
    | but do NOT have access to the user's 2FA verification code.           |
    |                                                                       |
    | GOAL: Access Carlos's account page to solve the lab.                  |
    |                                                                       |
    +-----------------------------------------------------------------------+
    |                                                                       |
    | [ CREDENTIALS PROVIDED ]                                              |
    |                                                                       |
    | YOUR ACCOUNT (Attacker):                                              |
    | Username: wiener                                                      |
    | Password: peter                                                       |
    |                                                                       |
    | VICTIM ACCOUNT (Target):                                              |
    | Username: carlos                                                      |
    | Password: montoya                                                     |
    |                                                                       |
    +-----------------------------------------------------------------------+
    |                                                                       |
    | [ THE CHALLENGE ]                                                     |
    |                                                                       |
    | 1. You know the victim's password ('montoya').                        |
    | 2. You are blocked by the 2FA verification screen.                    |
    | 3. You do not have the valid 2FA code sent to the victim.             |
    |                                                                       |
    | >> TASK: Bypass the 2FA check and log in as 'carlos'.                 |
    |                                                                       |
    +-----------------------------------------------------------------------+   

Exploit steps :

    +-----------------------------------------------------------------------+
    | LAB INSTRUCTIONS: 2FA Simple Bypass                                   |
    +-----------------------------------------------------------------------+
    |                                                                       |
    | [ STEP 1: Investigate Your Own Account ]                              |
    | 1. Log in to your own account.                                        |
    |    Credentials: wiener:peter                                          |
    | 2. Check email for 2FA code, enter it, and log in.                    |
    | 3. Go to your account page and note the URL:                          |
    |    >> /my-account?id=wiener                                           |
    | 4. Log out of your account.                                           |
    |                                                                       |
    | [ STEP 2: Exploit the Victim's Account ]                              |
    | 1. Log in using the victim's credentials.                             |
    |    Credentials: carlos:montoya                                        |
    | 2. You are prompted for the 2FA verification code (which you lack).   |
    | 3. DO NOT enter a code. Instead, manually change the URL in the       |
    |    browser address bar from:                                          |
    |    >> /login2                                                         |
    |    TO:                                                                |
    |    >> /my-account?id=carlos                                           |
    | 4. Press Enter. The page loads.                                       |
    |                                                                       |
    | >> RESULT: Lab Solved (Access to Carlos's account gained).            |
    |                                                                       |
    +-----------------------------------------------------------------------+   

Flaw Background :

    +-----------------------------------------------------------------------+
    | FLAW ANALYSIS: 2FA Enforcement Failure                                |
    +-----------------------------------------------------------------------+
    |                                                                       |
    | [ THE CORE ISSUE ]                                                    |
    | The server fails to verify that the Second Factor (OTP) was           |
    | successfully completed before granting access to protected pages.     |
    |                                                                       |
    | >> It treats the Password Check as the ONLY real gate.                |
    | >> It treats the OTP Page as a voluntary step, not a requirement.     |
    |                                                                       |
    +-----------------------------------------------------------------------+
    |                                                                       |
    | [ WHY IT HAPPENS: The Logic Gap ]                                     |
    |                                                                       |
    | 1. User submits Password -> Server validates -> Session Created.      |
    |    (Session Status: "Logged In")                                      |
    |                                                                       |
    | 2. Server redirects to /login2 (OTP Page).                            |
    |    (BUT: Server does NOT mark session as "2FA Pending")               |
    |                                                                       |
    | 3. Server expects user to voluntarily enter code.                     |
    |    (NO server-side flag prevents skipping this step)                  |
    |                                                                       |
    | >> RESULT: The session is already valid for /my-account.              |
    |                                                                       |
    +-----------------------------------------------------------------------+
    |                                                                       |
    | [ HOW THE BYPASS WORKS ]                                              |
    |                                                                       |
    | SCENARIO A: Manual URL Change                                         |
    | - User is at: /login2 (Waiting for code)                              |
    | - User types: /my-account                                             |
    | - Server checks: "Is session valid?" -> YES.                          |
    | - Server grants access. (Ignores missing OTP).                        |
    |                                                                       |
    | SCENARIO B: Dropping the Request                                      |
    | - User submits Password.                                              |
    | - User intercepts and DROPS the OTP request.                          |
    | - User requests /my-account directly.                                 |
    | - Server checks: "Is session valid?" -> YES.                          |
    | - Server grants access.                                               |
    |                                                                       |
    | >> REASON: The server never checked:                                  |
    |    "if (session.2FA_verified == false) { DENY }"                      |
    |                                                                       |
    +-----------------------------------------------------------------------+
    |                                                                       |
    | [ THE CONCLUSION ]                                                    |
    |                                                                       |
    | The 2FA page was merely a CLIENT-SIDE HURDLE.                         |
    | It was not a SERVER-SIDE GATE.                                        |
    |                                                                       |
    | >> Fix: Server must track state: "Password OK" -> "OTP Pending"       |
    |    -> "Fully Verified". Access denied until final state reached.      |
    |                                                                       |
    +-----------------------------------------------------------------------+   