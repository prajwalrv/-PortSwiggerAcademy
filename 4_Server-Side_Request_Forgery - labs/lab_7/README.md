================================================================================
          THE "PROXY MESSAGE" GAME: BLIND SSRF + SHELLSHOCK
================================================================================

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


## Example flow :

================================================================================
             THE ACTUAL NETWORK FLOW: BLIND SSRF + SHELLSHOCK
================================================================================
```text
 [ YOU ]
    │
    │ 1. Sends request to Public Web App.
    │    Payload says: "Go talk to Internal Service, and pass along 
    │    this malicious Shellshock glitch header."
    ▼
 [ PUBLIC WEB APP ]
    │
    │ 2. Forwards the message blindly. It does not look at the payload.
    │    It just blindly passes your header to the internal system.
    ▼
 [ INTERNAL SERVICE ]
    │
    │ 3. Processes the header. The Shellshock glitch triggers inside its 
    │    system. The vulnerability forces the machine to execute your 
    │    command: "Grab my secret files and send them out to the internet!"
    │
    │ 4. Bypasses the Web App completely! Reaches directly out to the 
    │    internet to connect to your trap server.
    ▼
 [ YOUR PUBLIC SERVER (OOB Trap) ]
    │
    │ 5. Logs the direct connection from the Internal Service.
    │    You look at your screen and see the stolen data printed in your logs.
```