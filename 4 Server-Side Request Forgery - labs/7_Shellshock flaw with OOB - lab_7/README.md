

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