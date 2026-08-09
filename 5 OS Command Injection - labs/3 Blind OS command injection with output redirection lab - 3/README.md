================================================================================
          THE FLOW: BLIND OS COMMAND INJECTION VIA OUTPUT REDIRECTION
================================================================================

┌──────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│      YOU         │     │    WEB APPLICATION   │     │      WEB SERVER      │
│                  │     │                      │     │                      │
│ Open Feedback    │────►│ Feedback function    │────►│ Receives your        │
│ page             │     │                      │     │ submitted details    │
│                  │     │ email parameter      │     │                      │
│ Capture request  │     │ is used inside a     │     │ Builds / executes    │
│ in Burp Suite    │     │ shell command        │     │ an OS command        │
│                  │     │                      │     │                      │
│ Inject:          │     │ Command injection    │     │ Command executes     │
│                  │     │ is possible          │     │ on the server        │
│ ||whoami >       │     │                      │     │                      │
│ /var/www/images/ │     │ Output normally      │     │                      │
│ output.txt||     │     │ isn't returned       │     │                      │
└──────────────────┘     └──────────────────────┘     └──────────┬───────────┘
                                                                 │
                                                                 │
                                                                 │ whoami
                                                                 ▼
                                                    ┌─────────────────────────┐
                                                    │       OS / SHELL        │
                                                    │                         │
                                                    │ Executes:               │
                                                    │                         │
                                                    │       whoami            │
                                                    │                         │
                                                    │ Output is redirected    │
                                                    │ into:                   │
                                                    │                         │
                                                    │ /var/www/images/        │
                                                    │ output.txt              │
                                                    └────────────┬────────────┘
                                                                 │
                                                                 │ Writes output
                                                                 ▼
                                                    ┌─────────────────────────┐
                                                    │   WRITABLE DIRECTORY    │
                                                    │                         │
                                                    │   /var/www/images/      │
                                                    │                         │
                                                    │       output.txt        │
                                                    │                         │
                                                    │   Contains the result   │
                                                    │   of whoami             │
                                                    └────────────┬────────────┘
                                                                 │
                                                                 │
                                                                 │ Second request
                                                                 │ retrieves file
                                                                 ▼
                                                    ┌─────────────────────────┐
                                                    │    IMAGE / FILE URL     │
                                                    │                         │
                                                    │ filename=output.txt     │
                                                    │                         │
                                                    │ Application serves the  │
                                                    │ contents of the file    │
                                                    └────────────┬────────────┘
                                                                 │
                                                                 │ HTTP response
                                                                 ▼
                                                          ┌──────────────┐
                                                          │     YOU      │
                                                          │              │
                                                          │ Receive the  │
                                                          │ output of    │
                                                          │ whoami       │
                                                          │              │
                                                          │      ✔       │
                                                          └──────────────┘
================================================================================