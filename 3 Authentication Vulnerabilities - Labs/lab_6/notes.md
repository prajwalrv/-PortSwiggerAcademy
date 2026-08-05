Lab#6 Broken brute-force protection, IP block

========================================================================================
             LAB SOLUTION FLOW: BROKEN BRUTE-FORCE PROTECTION (IP BLOCK)
========================================================================================

   +--------------------------+

   |   1. Capture Request     | <--- Intercept the POST /login request using Burp.
   +--------------------------+
                 |
                 v
   +--------------------------+

   |  2. Configure Intruder   | <--- Send request to Intruder. 
   +--------------------------+      Select Pitchfork attack type.
                 |
                 v
   +--------------------------+

   |  3. Set Resource Pool    | <--- Set Maximum concurrent requests to 1.
   +--------------------------+      (Forces strict, one-by-one sequential order)
                 |
                 v
   +------------------------------------------------------------------------------------+

   | 4. Setup Payload 1 (Username List)                                                 |
   |                                                                                    |
   |    Alternate your own valid username with the victim's username:                   |
   |    [wiener -> carlos -> wiener -> carlos -> wiener -> carlos ...]                  |
   +------------------------------------------------------------------------------------+
                 |
                 v
   +------------------------------------------------------------------------------------+

   | 5. Setup Payload 2 (Password List)                                                 |
   |                                                                                    |
   |    Align your valid password with your username, followed by a candidate password: |
   |    [peter  -> pass1  -> peter  -> pass2  -> peter  -> pass3  ...]                  |
   +------------------------------------------------------------------------------------+
                 |
                 v
   +--------------------------+

   |    6. Launch Attack      | <--- Start sequence. The successful 'wiener' logins 
   +--------------------------+      reset the IP block counter before 3 failed attempts.
                 |
                 v
   +--------------------------+

   | 7. Filter & Sort Results | <--- Hide HTTP 200 responses.
   +--------------------------+      Sort remaining entries by username.
                 |
                 v
          [ Look for HTTP 302 ] <--- Find the single 302 redirection status for 'carlos'.
                 |
                 v
          [ Password Found ]
                 |
                 v
   +--------------------------+

   |  8. Access Carlos' Lab   | <--- Log in using Carlos' credentials.
   +--------------------------+      Status: LAB SOLVED
========================================================================================
