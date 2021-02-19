
openssl req -x509 -newkey rsa:2048 -keyout droneAirAtlas_private_RSA.pem -nodes -out droneAirAtlas_public_RSA.pem 

openssl ecparam -genkey -name prime256v1 -noout -out droneAirAtlas_private.pem
openssl ec -in droneAirAtlas_private.pem -pubout -out droneAirAtlas_public.pem