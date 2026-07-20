Lab#4 User role can be modified in user profile

Target Goal - FInd the admin pannel & delete the user carlos

Stepps to script :

    1. Login with giver user creds.
    2. Change the role_id of the user to 2
    3. Access admin panel, & delete user carlos.

Analysis : https://insecure-website.com/myaccount?id=123 
           --------> https://insecure-website.com/myaccount?id=124 --> [IDOR - Insecure Direct Object Reference] Vulnerability

Concept : Horizontal privilege escalation

    Horizontal privilege escalation occurs if a user is able to gain access to resources belonging to another user, instead of their own resources of that type. For example, if an employee can access the records of other employees as well as their own, then this is horizontal privilege escalation.

    Horizontal privilege escalation attacks may use similar types of exploit methods to vertical privilege escalation. For example, a user might access their own account page using the following URL:
    https://insecure-website.com/myaccount?id=123

    If an attacker modifies the id parameter value to that of another user, they might gain access to another user's account page, and the associated data and functions.
    Note

    This is an example of an insecure direct object reference (IDOR) vulnerability. This type of vulnerability arises where user-controller parameter values are used to access resources or functions directly.

    In some applications, the exploitable parameter does not have a predictable value. For example, instead of an incrementing number, an application might use globally unique identifiers (GUIDs) to identify users. This may prevent an attacker from guessing or predicting another user's identifier. However, the GUIDs belonging to other users might be disclosed elsewhere in the application where users are referenced, such as user messages or reviews.
