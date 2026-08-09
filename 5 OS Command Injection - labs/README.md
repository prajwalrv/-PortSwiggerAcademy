```text
================================================================================
                         OS COMMAND INJECTION
================================================================================

  WHAT IS OS COMMAND INJECTION?
  ------------------------------

  An application takes user-controlled input and passes it to the
  operating system as part of a command.

  If the application does not properly separate DATA from COMMANDS,
  an attacker may be able to influence which OS command is executed.

================================================================================
                    BASIC OS COMMAND INJECTION FLOW
================================================================================


┌──────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
│      ATTACKER    │      │    WEB APPLICATION   │      │      WEB SERVER      │
│                  │      │                      │      │                      │
│  Sends input     │─────►│  Receives user input │─────►│  Builds an OS        │
│                  │      │                      │      │  command using the   │
│  Example:        │      │  Example feature:    │      │  supplied input      │
│                  │      │                      │      │                      │
│  127.0.0.1       │      │  "Ping this IP"      │      │  OS command executes │
│                  │      │                      │      │                      │
│  + additional    │      │  Input is not        │      │  on the server       │
│    command       │      │  safely separated    │      │                      │
└──────────────────┘      └──────────────────────┘      └──────────┬───────────┘
                                                                   │
                                                                   │
                                                                   ▼
                                                         ┌──────────────────────┐
                                                         │     OPERATING        │
                                                         │       SYSTEM         │
                                                         │                      │
                                                         │  Executes the        │
                                                         │  resulting command   │
                                                         └──────────────────────┘


================================================================================
                         THE CORE IDEA
================================================================================


┌──────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    ATTACKER  │──────►│ WEB APPLICATION │──────►│  OPERATING      │
│              │       │                 │       │    SYSTEM       │
│ User input   │       │ Builds command  │       │                 │
│              │       │ using input     │       │ Executes command│
└──────────────┘       └─────────────────┘       └─────────────────┘
                              │
                              │
                              ▼
                     USER INPUT BECOMES
                     PART OF AN OS COMMAND


================================================================================
                     TYPE 1 — IN-BAND COMMAND INJECTION
================================================================================

  IN-BAND means:

  The command is executed on the server AND the command's output comes
  back through the application's normal HTTP response.


┌──────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
│      ATTACKER    │      │    WEB APPLICATION   │      │      WEB SERVER      │
│                  │      │                      │      │                      │
│  Sends crafted   │─────►│  Takes the supplied  │─────►│  Passes input into   │
│  input           │      │  input and builds    │      │  an OS command       │
│                  │      │  an OS command       │      │                      │
│                  │      │                      │      │  Command executes    │
└──────────────────┘      └──────────────────────┘      └──────────┬───────────┘
                                                                   │
                                                                   │
                                                                   │ Command
                                                                   │ output
                                                                   ▼
                                                        ┌──────────────────────┐
                                                        │   COMMAND OUTPUT     │
                                                        │                      │
                                                        │   Returned to the    │
                                                        │   web application    │
                                                        └──────────┬───────────┘
                                                                   │
                                                                   │ HTTP Response
                                                                   ▼
                                                        ┌──────────────────────┐
                                                        │      ATTACKER        │
                                                        │                      │
                                                        │  Sees the command    │
                                                        │  output directly     │
                                                        │                      │
                                                        │        ✔ OUTPUT      │
                                                        └──────────────────────┘
================================================================================
                     TYPE 2 — BLIND COMMAND INJECTION
================================================================================

  BLIND means:

  The command may execute successfully, but the application's HTTP response
  does NOT contain the command's output.


┌──────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
│      ATTACKER    │      │    WEB APPLICATION   │      │      WEB SERVER      │
│                  │      │                      │      │                      │
│  Sends crafted   │─────►│  Takes user input    │─────►│  Executes the OS     │
│  input           │      │  and executes the    │      │  command             │
│                  │      │  command             │      │                      │
│                  │      │                      │      │  Command executes    │
└──────────────────┘      └──────────────────────┘      └──────────┬───────────┘
                                                                   │
                                                                   │
                                                                   │ Output exists
                                                                   │ internally
                                                                   ▼
                                                         ┌──────────────────────┐
                                                         │    COMMAND OUTPUT    │
                                                         │                      │
                                                         │  NOT included in     │
                                                         │  HTTP response       │
                                                         └──────────────────────┘
                                                                    │
                                                                    │
                                                                    │ No visible
                                                                    │ output
                                                                    ▼
                                                         ┌──────────────────────┐
                                                         │      ATTACKER        │
                                                         │                      │
                                                         │  Cannot directly     │
                                                         │  see command output  │
                                                         │                      │
                                                         │        ❌ OUTPUT     │
                                                         └──────────────────────┘
================================================================================
                     HOW DO WE KNOW BLIND EXECUTION HAPPENED?
================================================================================

                 ┌──────────────────────┐
                 │      ATTACKER        │
                 └──────────┬───────────┘
                            │
                            │ Sends command
                            ▼
                 ┌──────────────────────┐
                 │   WEB APPLICATION    │
                 └──────────┬───────────┘
                            │
                            │ Executes command
                            ▼
                 ┌──────────────────────┐
                 │      WEB SERVER      │
                 │                      │
                 │      OS COMMAND      │
                 └──────────┬───────────┘
                            │
                            │
                            │ No output
                            │ in HTTP response
                            ▼
                 ┌──────────────────────┐
                 │      ATTACKER        │
                 │                      │
                 │  "I don't see the    │
                 │   command output."   │
                 └──────────────────────┘


  In a controlled security lab, execution can instead be inferred from
  an observable side effect, such as:

       command execution
              │
              ▼
       observable change
              │
              ▼
       attacker confirms execution

  The important distinction is that the result is NOT returned directly
  inside the application's HTTP response.

================================================================================
                         IN-BAND vs BLIND
================================================================================


┌──────────────────────────┬──────────────────────────┐
│      IN-BAND             │        BLIND             │
├──────────────────────────┼──────────────────────────┤
│ Command executes         │ Command executes         │
│          │               │          │               │
│          ▼               │          ▼               │
│ Output generated         │ Output generated         │
│          │               │          │               │
│          ▼               │          X               │
│ Output returned          │ Output NOT returned      │
│          │               │                          │
│          ▼               │ Execution must be        │
│ Attacker sees output     │ inferred from another    │
│ directly                 │ observable effect        │
└──────────────────────────┴──────────────────────────┘
================================================================================
```
