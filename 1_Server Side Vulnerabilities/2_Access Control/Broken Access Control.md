===================================================================== BROKEN ACCESS CONTROL
AGENDA : 
	--> What is Access Control Vulerabilities.
	--> How do you find these vulnerabilities.
	--> How do you exploit it.
	
==> What is Broken Access Control Vulerabilities :
CONCEPT : This vulnerbility arises when users can act outside their intended permissions. This typically leads to :
		-> Sensitive information disclosure, 
		-> Unauthorized access, modification or destruction of data.
	
	-> Access Contro : it determines whether the user is allowed to carry out the action that they are attempting to perform.

		ex : user alice wants to perform banking transaction, ehrn you perform that banking transaction the session token 
		     gets passed to the application & the app backend checks which user id is this session token aassigned to once
		     the user id idententifiess it checks access control rules in the database that have been applied to specif 
		     user id, if the user has the access transaction completes, if not transaction will be failed.
		     
	-> Types of Access Control :
		
		1. Vertical Access Control : it is a security rule that ensures users can only access features appropriate for their
		                             specific job role or rank.
						
			Example : Think of it like a building with different floor levels:
				-> Regular users are only allowed on the ground floor to do basic tasks. 
				-> Administrators have a key to the upper floors to manage the building.

		2. Horizontal Access Control : it enables different users to access similar resources types.
			
			Example : Bob and Adam both have same privilege in the application which is that they
				  are regular users. now Bob should be able to access his data & should not be
				  able to access Adam's data & vice-versa.
				  
		3. Context-dependent Access Control : it restricts access to functionality & resources based on
				  the state of the application or the user's interaction with it to prevent 
				  users performing actions in wrong order.
				  
			Example : In a multistep process for deleting users, the first step is to click on the 
				  delete button, when yo do that its pops and asks yo for the confirmation to
				  delete that user, if you click yes --> this initiates another request to del
				  that specific user & deletes the user.
				  
	-> Types of Brokrn Access Control Vulnerability :
	
		1. Horizontal privilege escalation : it occurs when an attacker gains access to resources belonging
				  to another user of the same privilege level.
				  
			Example : https://vulnerablle-website.com/idor/myccountuser?id=123 -> Bob[Attacker]
				  ----> https://vulnerablle-website.com/idor/myccountuser?id=124  -> Alice 
				  [now actually Bob is having Alice's account & its's data access]
				  
		2. Verticle privilege escalation : it occurs when an attacker gain access to resources belonging to
				  another user of the higher hireacrchy level with higher privilege level.
				  
			Exaample : https://vulnerablle-website.com/idor/myccountuser?regularuser=true -> [Bob] -> regular user
				   ----> https://vulnerablle-website.com/idor/myccountuser?admn=true  -> Admin 
				   [now actually Bob is having Admin account & its's root permission access]
				   
		3. Vulnerability in Multi-Step Process : it occurs when access control rules are implemented on some of the steps
				   
			Example : Orderly chained requests ---> /confirm  ->   /delete   ->  deleted user
				   [bypass] step 1 /confirm - [because this endpint is implemented with strict access controls.]
				   ---> hop on /delete --> deleted user ['/delete' endpoint is vulnerable now]
				   [Because developer though that all user will for the ordered chain so he kept acess control 
				    settings only to '/confirm' not '/delete' wich become vulnerable]
				    
	-> Common Access Control Vulnerability Exploit Way : [VVIP]
	
		1. Bypassing access control checks by modifying parameters in the URL or HTML page.
		2. Accessing the API with missing access controls on the POST, PUT, & DELETE requests.
		3. Manipulating metadate, such as replying or taampering with JSON web tokens [JWT] or a cookie.
		4. Exploiting CORS misconfiguation that allow API access from unauthorized / untrusted origins.
		5. Force browsing to authenticated pages as an unauthenticated user.
