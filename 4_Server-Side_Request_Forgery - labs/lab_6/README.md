================================================================================
          THE "HIDE AND SEEK" GAME: WHY BLIND SSRF IS HIDDEN
================================================================================

 NORMAL REQUEST (The Server Speaks To You)
 ┌──────────────┐     1. "Give me secret_file.txt"   ┌───────────────┐
 │   Attacker   │ ─────────────────────────────────► │ Target Server │
 │    (You)     │ ◄───────────────────────────────── │               │
 └──────────────┘     2. "Here is the file: [Data]"  └───────────────┘
                      (You see the result instantly on your screen)


 BLIND SSRF (The Server Plays "Hide and Seek")
 No matter what evil request you send, the server hides the result from you.
 It acts like a stone wall, always giving you the exact same blank response.

 Request A: "Fetch file://etc/passwd" (Attack)
 Request B: "Fetch http://localhost:80" (Port Scan)
 Request C: "Fetch http://google.com" (Normal URL)

 ┌──────────────┐             Any Request            ┌───────────────┐
 │   Attacker   │ ─────────────────────────────────► │ Target Server │
 │    (You)     │ ◄───────────────────────────────── │               │
 └──────────────┘     "Error: Cannot load image"     └───────────────┘
                      (Always the same blank screen)

 You have NO IDEA if the server actually read the file, scanned the port, 
 or just ignored you completely. The evidence is hidden inside the server.

================================================================================
             HOW THE OUT-OF-BAND (OOB) TRAP BREAKS THE GAME
================================================================================
 Since the server refuses to talk to you, you trick it into talking to someone 
 else standing outside the hiding spot—your OOB trap server.

 ┌──────────────┐  1. "Go fetch this URL:            ┌───────────────┐
 │   Attacker   │      http://my-oob-trap.com"       │ Target Server │
 │    (You)     │ ─────────────────────────────────► │  (Vulnerable) │
 └──────────────┘                                    └───────────────┘
        │                                                    │
        │                                                    │ 2. Silently walks
        │                                                    │    out the back
        │                                                    │    door to fetch
        │                                                    ▼    the URL...
        │                                            ┌───────────────┐
        │          3. "I found you!"                 │ Your OOB Trap │
        └◄────────────────────────────────────────── │ (Heard the    │
               The trap alerts you:                  │ server step   │
               "Target just connected to me!"        │ on the twig)  │
                                                     └───────────────┘

 The target server still gives your browser the same unhelpful error message.
 But it loses the game because your OOB Trap caught it moving in the background.

## Example flow : 
================================================================================
          THE ACTUAL NETWORK FLOW: STANDARD OOB SSRF (INTERNAL TARGET)
================================================================================

 [ YOU ]
    │
    │ 1. Sends a request to the Public Web App.
    │    Payload says: "Go talk to Internal Service, but pass along 
    │    my external domain link (http://your-public-server.com) inside 
    │    the request headers/parameters."
    ▼
 [ PUBLIC WEB APP ]
    │
    │ 2. Blindly routes your message into the private network.
    │    It acts like a delivery driver, dropping off your payload 
    │    directly to the internal machine.
    ▼
 [ INTERNAL SERVICE ]
    │
    │ 3. Processes the incoming request from the Web App. 
    │    It looks at the data you injected and thinks: "Oh, I am supposed 
    │    to load an image/file from http://your-public-server.com."
    │
    │ 4. The Internal Service opens a connection and reaches directly 
    │    out to the internet to fetch that file from your server.
    ▼
 [ YOUR PUBLIC SERVER (OOB Trap) ]
    │
    │ 5. Logs the direct connection coming from the Internal Service's IP!
    │    You check your dashboard and see the hit.
