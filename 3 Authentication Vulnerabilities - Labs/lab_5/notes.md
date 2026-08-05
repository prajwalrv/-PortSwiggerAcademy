Lab# Username enumeration via response timing

========================================================================================
             LAB SOLUTION FLOW: USERNAME ENUMERATION VIA RESPONSE TIMING
========================================================================================

   +--------------------------+

   |   1. Capture Request     | <--- Submit invalid credentials on /login page
   +--------------------------+      with a proxy tool to intercept the POST request.
                 |
                 v
   +--------------------------+

   |  2. Analyze Protection   | <--- Multiple attempts may trigger an IP-based block.
   +--------------------------+
                 |
                 v
   +--------------------------+

   |  3. Add Spoofing Header  | <--- Inject "X-Forwarded-For" into the HTTP header.
   +--------------------------+      (Used to test bypass of IP-based restrictions)
                 |
                 v
   +------------------------------------------------------------------------------------+

   | 4. Setup Attack 1 (Enumerate Username)                                             |
   |                                                                                    |
   |    [Header: X-Forwarded-For] -----------> Incremental numbers (to rotate IPs)      |
   |    [Parameter: Username] ---------------> List of candidate usernames              |
   |    [Parameter: Password] ---------------> Fixed long string (to amplify timing)    |
   +------------------------------------------------------------------------------------+
                 |
                 v
   +--------------------------+

   |   5. Run Username Scan   | <--- Execute the automated request sequence.
   +--------------------------+
                 |
                 v
   +--------------------------+      Analyze the duration between "Response received" 

   | 6. Check Response Times  | <--- and "Response completed".
   +--------------------------+      A valid username may show a longer processing time.
                 |
                 v
          [ Valid Username Found ]
                 |
                 v
   +------------------------------------------------------------------------------------+

   | 7. Setup Attack 2 (Brute-force Password)                                            |
   |                                                                                    |
   |    [Header: X-Forwarded-For] -----------> Incremental numbers                      |
   |    [Parameter: Username] ---------------> Fixed (The identified valid username)     |
   |    [Parameter: Password] ---------------> List of candidate passwords              |
   +------------------------------------------------------------------------------------+
                 |
                 v
   +--------------------------+

   |   8. Run Password Scan   | <--- Execute the second automated sequence.
   +--------------------------+
                 |
                 v
   +--------------------------+

   | 9. Identify HTTP 302     | <--- Look for a redirection status code indicating
   +--------------------------+      a successful login.
                 |
                 v
          [ Password Found ]
                 |
                 v
   +--------------------------+

   |   10. Access Account     | <--- Use the discovered credentials to log in.
   +--------------------------+      Status: LAB SOLVED
========================================================================================
