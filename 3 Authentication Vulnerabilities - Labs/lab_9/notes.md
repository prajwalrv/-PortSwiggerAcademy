Lab#9 Brute-forcing a stay-logged-in cookie

==============================================
LAB: BRUTE-FORCING A STAY-LOGGED-IN COOKIE
==============================================

[ GOAL ]
--------
Gain access to Carlos's My Account page by brute-forcing
his stay-logged-in cookie.


[ WHAT YOU KNOW ]
----------------
- Your username: wiener
- Your password: peter
- Victim username: carlos
- Candidate passwords: use the provided list


[ IMPORTANT IDEA ]
-----------------
The cookie is built like this:

  username + ":" + MD5(password)

Then it is Base64 encoded.

Example:
  wiener:51dc30ddc473d43a6011e9ebba6ca770

So the pattern is:

  base64( username + ":" + md5(password) )


[ STEP-BY-STEP GUIDE ]
---------------------

1) LOGIN AS YOURSELF
--------------------
- Log in with:
  - Username: wiener
  - Password: peter
- Select the option: Stay logged in

2) INSPECT THE COOKIE
---------------------
- Open the request in Burp
- Go to the cookie value
- Check the stay-logged-in cookie
- Decode it in the Inspector panel

3) CONFIRM THE FORMAT
----------------------
- Notice that the decoded value looks like:
  wiener:hash
- The hash is likely an MD5 hash of the password
- Test this by hashing your password with MD5
- If it matches, you have confirmed the logic

4) LOG OUT
----------
- Sign out of your account
- Keep the request available for Burp Intruder

5) SEND TO BURP INTRUDER
------------------------
- In the request:
  - GET /my-account?id=wiener
- Highlight the stay-logged-in cookie
- Send it to Intruder

6) SET UP PAYLOAD POSITION
---------------------------
- Burp will automatically place the cookie as a payload position
- Add your own password as a single test payload

7) ADD PAYLOAD PROCESSING RULES
--------------------------------
Apply these rules in this exact order:

  [1] Hash: MD5
  [2] Add prefix: wiener:
  [3] Encode: Base64-encode

This will turn your password into a valid cookie value.

8) VERIFY THE TEST
------------------
- Start the attack
- Check whether the response contains:
  Update email
- If it does, your payload processing is working correctly

9) BRUTE-FORCE CARLOS
---------------------
Now change the attack to target Carlos:

- Remove your password from the payload list
- Replace it with the list of candidate passwords
- Change the URL parameter:
  - id=wiener  ->  id=carlos
- Change the prefix rule to:
  - carlos:

10) START THE ATTACK
--------------------
- Run the attack again
- Watch the responses carefully

11) LOOK FOR SUCCESS
---------------------
The correct cookie will produce a response containing:

  Update email

That means the cookie is valid for Carlos's account.


[ SUCCESS CONDITION ]
---------------------
When one response contains "Update email",
you have successfully brute-forced Carlos's cookie.


[ FINAL RESULT ]
----------------
You will gain access to Carlos's My Account page.
