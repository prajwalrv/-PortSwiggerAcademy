```text
================================================================================
                 THE FLOW: OS COMMAND INJECTION — SIMPLE CASE
================================================================================

┌──────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│      YOU         │     │    WEB APPLICATION   │     │      WEB SERVER      │
│                  │     │                      │     │                      │
│  Open product    │────►│  Stock checker       │────►│  Receives product    │
│  page            │     │                      │     │  and store IDs       │
│                  │     │  storeID = 1         │     │                      │
│  Click           │     │                      │     │  Builds a shell      │
│  "Check Stock"   │     │  Normally trusted    │     │  command using the   │
│                  │     │  user-supplied value │     │  supplied storeID    │
│                  │     │                      │     │                      │
└──────────────────┘     └──────────────────────┘     └──────────┬───────────┘
                                                                 │
                                                                 │
                                                                 │ OS command
                                                                 ▼
                                                    ┌─────────────────────────┐
                                                    │      OPERATING SYSTEM   │
                                                    │                         │
                                                    │  Shell executes the     │
                                                    │  command constructed    │
                                                    │  by the application     │
                                                    └────────────┬────────────┘
                                                                 │
                                                                 │ Command output
                                                                 ▼
                                                    ┌─────────────────────────┐
                                                    │    WEB APPLICATION      │
                                                    │                         │
                                                    │ Returns the raw command │
                                                    │ output in the HTTP      │
                                                    │ response                │
                                                    └────────────┬────────────┘
                                                                 │
                                                                 │ HTTP response
                                                                 ▼
                                                          ┌──────────────┐
                                                          │     YOU      │
                                                          │              │
                                                          │  See output  │
                                                          │  directly    │
                                                          └──────────────┘


================================================================================
                       WHERE THE VULNERABILITY HAPPENS
================================================================================


┌──────────────────┐
│      YOU         │
│                  │
│ Normal value:    │
│ storeID = 1      │
└────────┬─────────┘
         │
         │ Burp modifies parameter
         ▼
┌──────────────────┐
│   MODIFIED INPUT │
│                  │
│ storeID =        │
│ 1|whoami         │
└────────┬─────────┘
         │
         │ Sent to application
         ▼
┌────────────────────────┐
│    WEB APPLICATION     │
│                        │
│ Does not safely        │
│ separate user input    │
│ from the shell command │
└───────────┬────────────┘
            │
            │ Input becomes part
            │ of the command
            ▼
┌────────────────────────┐
│      WEB SERVER        │
│                        │
│ Shell interprets the   │
│ command separator      │
│ and executes the       │
│ injected command       │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│       OS / SHELL       │
│                        │
│ Executes:              │
│                        │
│      whoami            │
└───────────┬────────────┘
            │
            │ Returns current
            │ user name
            ▼
┌────────────────────────┐
│    HTTP RESPONSE       │
│                        │
│ Raw command output     │
│ is returned by the     │
│ application            │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│          YOU           │
│                        │
│ See the current        │
│ operating-system user  │
│                        │
│          ✔             │
└────────────────────────┘
================================================================================
```