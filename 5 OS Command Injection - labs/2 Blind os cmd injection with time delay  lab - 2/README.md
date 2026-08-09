```text
================================================================================
          THE FLOW: BLIND OS COMMAND INJECTION VIA TIME DELAY
================================================================================

┌──────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│      YOU         │     │    WEB APPLICATION   │     │      WEB SERVER      │
│                  │     │                      │     │                      │
│ Open Feedback    │────►│ Feedback function    │────►│ Receives feedback    │
│ page             │     │                      │     │ submission           │
│                  │     │ email parameter      │     │                      │
│ Capture request  │     │ normally contains    │     │ Application builds   │
│ in Burp Suite    │     │ an email address     │     │ a shell command      │
│                  │     │                      │     │ using user input     │
│ Modify email:    │     │ No safe separation   │     │                      │
│                  │     │ between input and    │     │ Command executes     │
│ & sleep 10 #     │     │ shell command        │     │ on the server        │
│                  │     │                      │     │                      │
└──────────────────┘     └──────────────────────┘     └──────────┬───────────┘
                                                                 │
                                                                 │
                                                                 │ Injected
                                                                 │ command
                                                                 ▼
                                                    ┌─────────────────────────┐
                                                    │       OS / SHELL        │
                                                    │                         │
                                                    │ Executes the injected   │
                                                    │ command                 │
                                                    │                         │
                                                    │ sleep 10                │
                                                    │                         │
                                                    │ Takes approximately     │
                                                    │ 10 seconds              │
                                                    └────────────┬────────────┘
                                                                 │
                                                                 │ Command output
                                                                 │ is NOT returned
                                                                 ▼
                                                    ┌─────────────────────────┐
                                                    │    WEB APPLICATION      │
                                                    │                         │
                                                    │ Returns its normal      │
                                                    │ HTTP response           │
                                                    │                         │
                                                    │ No command output       │
                                                    │ visible to attacker     │
                                                    └────────────┬────────────┘
                                                                 │
                                                                 │ HTTP response
                                                                 │ after delay
                                                                 ▼
                                                          ┌──────────────┐
                                                          │     YOU      │
                                                          │              │
                                                          │ Response     │
                                                          │ arrives ~10s │
                                                          │ later        │
                                                          │              │
                                                          │     ✔        │
                                                          └──────────────┘

================================================================================
                           CORE IDEA
================================================================================

       YOU
        │
        │ Inject command that causes delay
        ▼
   WEB APPLICATION
        │
        │ Executes command
        ▼
     OS / SHELL
        │
        │ Delays execution
        ▼
   WEB APPLICATION
        │
        │ No command output
        │ but response is delayed
        ▼
      YOU


              COMMAND OUTPUT = HIDDEN
              EXECUTION EFFECT = VISIBLE
================================================================================
```