```text
================================================================================
       THE FLOW: BLIND OS COMMAND INJECTION VIA OUT-OF-BAND INTERACTION
================================================================================

┌──────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│      YOU         │     │    WEB APPLICATION   │     │      WEB SERVER      │
│                  │     │                      │     │                      │
│ Open Feedback    │────►│ Feedback function    │────►│ Receives the         │
│ page             │     │                      │     │ submitted email      │
│                  │     │ User input is used   │     │ parameter            │
│ Capture request  │     │ inside a shell       │     │                      │
│ in Burp Suite    │     │ command              │     │ Command executes     │
│                  │     │                      │     │ asynchronously       │
│ Modify email:    │     │ No command output    │     │                      │
│                  │     │ is returned          │     │                      │
│ x||nslookup +    │     │                      │     │                      │
│ collaborator     │     │ HTTP response is     │     │                      │
│ subdomain||      │     │ unaffected           │     │                      │
└──────────────────┘     └──────────────────────┘     └──────────┬───────────┘
                                                                 │
                                                                 │
                                                                 │ OS command
                                                                 ▼
                                                    ┌─────────────────────────┐
                                                    │       OS / SHELL        │
                                                    │                         │
                                                    │ Executes:               │
                                                    │                         │
                                                    │ nslookup                │
                                                    │ x.<COLLABORATOR>        │
                                                    │                         │
                                                    │ The server attempts a   │
                                                    │ DNS lookup              │
                                                    └────────────┬────────────┘
                                                                 │
                                                                 │ DNS query
                                                                 ▼
                                                    ┌─────────────────────────┐
                                                    │   BURP COLLABORATOR     │
                                                    │                         │
                                                    │ Receives the DNS        │
                                                    │ interaction             │
                                                    │                         │
                                                    │        ✔ HIT            │
                                                    └─────────────────────────┘

================================================================================
                         WHAT THE SCREENSHOT SHOWS
================================================================================


┌────────────────────────────┐
│       COLLABORATOR         │
│         POLLING            │
│                            │
│  #   Time       Type       │
│  ────────────────────────  │
│  1   01:17:43   DNS        │
│  2   01:17:43   DNS        │
│  3   01:18:56   DNS  ←     │
│  4   01:18:56   DNS        │
└────────────────────────────┘
================================================================================
```