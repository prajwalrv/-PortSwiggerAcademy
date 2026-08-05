Lab#6 Method-based access control can be circumvented

Target Goal - FInd the admin pannel & delete the user carlos

Background Knowledge : The X-Original-URL header is a non starndard http request that can be used to overwrite the original request.
- let's say a website implements access control by restricting based on a URL but the app allows the URL to be overwritten using that X-Original-URL reqyest header.
---> this makes it Access Control Vulnrability

Steps to exploit :
    1. Login using given regular user cred
    2. This vulnerability decides on which method (POST, GET, PUT, UPDATE, DELETE) is 
        not havng access control,
        example : an enpoint : POST /admin-roles HTTP/2  --> Access COntrols is implemented with POST method only.
                -----------> GET /admin-roles?username=carlos&action=upgrade HTTP/2
        Host: --> now the same enpoint with GET method without Access Control implementation is vulnerable.
    