## ====================================================================
##                    SSRF REMEDIATION
## ====================================================================

## 1. Validate User Input
----------------------
```txt
Never trust user-supplied URLs.

        User URL
           |
           v
      Validate URL
           |
     Valid / Reject

--------------------------------------------------------------------
```

## 2. Use an Allowlist
-------------------
```text
Allow requests only to trusted domains.

✔ api.company.com
✔ payment.company.com

✖ localhost
✖ 127.0.0.1
✖ Private IPs

--------------------------------------------------------------------
```

## 3. Block Internal Resources
---------------------------
```text
Prevent access to:

✔ localhost
✔ 127.0.0.1
✔ 10.x.x.x
✔ 172.16.x.x - 172.31.x.x
✔ 192.168.x.x
✔ Cloud Metadata (169.254.169.254)

--------------------------------------------------------------------
```

## 4. Restrict Outbound Requests
-----------------------------
```text
Allow Server
      |
      +-----> Trusted APIs

Block everything else using firewall rules.

--------------------------------------------------------------------
```

## 5. Disable Unnecessary Protocols
--------------------------------
```text
Allow:
✔ HTTP
✔ HTTPS

Block:
✖ file://
✖ ftp://
✖ gopher://

--------------------------------------------------------------------
```

## 6. Log & Monitor
----------------
```text
Monitor outbound requests for:

• Internal IP access
• Unusual destinations
• Suspicious request patterns

====================================================================
```
