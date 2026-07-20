Lab#5 URL-based access control can be circumvented

Target Goal - FInd the admin pannel & delete the user carlos

Background Knowledge : The X-Original-URL header is a non starndard http request that can be used to overwrite the original request.
- let's say a website implements access control by restricting based on a URL but the app allows the URL to be overwritten using that X-Original-URL reqyest header.
---> this makes it Access Control Vulnrability

