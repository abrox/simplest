# simplest
Simple Python EST server + CA for learning purpose.
As You notice it's not protect private keys etc. So You should **not** use this as as real EST + CA.

EST server URI path begins with"https://www.example.com/.well-known/est".  Each EST operation is indicated by a path-suffix that indicates the intended operations.Following operations and URIs are supported:

|Operation |Operation path   |Details|
|----------|-----------------|-------|
|Distribution of CA Certificates| /cacerts |[RFC7030 section 4.1](https://tools.ietf.org/html/rfc7030#section-4.1)|
|Enrollment of clients|/simpleenroll| [RFC7030 section 4.2](https://tools.ietf.org/html/rfc7030#section-4.2)|
|Re-enrollment of clients|/simplereenroll |[RFC7030 section 4.2.2](https://tools.ietf.org/html/rfc7030#section-4.2.2)|   


## Motivation
- Study [RFC7030][51b5b8ee] and understand how EST works.
- Try to understand more about CA's and certificates.
- Do something fun and usefull with Python

## Configuration and setup
First update configuration files from ca/conf directory. Source set_env.sh script to set setup required environment variables.
 **Note!** with new shell You must always first source  set_env script  before call any other scripts or run server.  

``` bash
juki@JumppaHuitti:~/workspace/simplest/ca/scripts$ source ./set_env.sh
CA_BASEDIR is /home/juki/workspace/simplest/ca and EST_BASEDIR: /home/juki/workspace/simplest/server

```
Next call create_ca.sh  script to create CA+ server certificate for
EST server.
```bash
juki@JumppaHuitti:~/workspace/simplest$ ./ca/scripts/create_ca.sh
1+0 records in
1+0 records out
256 bytes copied, 0,000183138 s, 1,4 MB/s
Generating a RSA private key
..........................................................++++
.....................................................................................................++++
writing new private key to '/home/juki/workspace/simplest/ca/cakey.pem'
-----
Generating a RSA private key
................................................................................................................+++++
...........................................................................+++++
writing new private key to '/home/juki/workspace/simplest/server/certs/serverkey.pem'
-----
Using configuration from /home/juki/workspace/simplest/ca/conf/openssl-ca.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
countryName           :PRINTABLE:'FI'
stateOrProvinceName   :ASN.1 12:'Uusimaa'
localityName          :ASN.1 12:'Vantaa'
organizationName      :ASN.1 12:'Juksutin'
commonName            :ASN.1 12:'127.0.0.1'
Certificate is to be certified until Jan  9 11:18:27 2020 GMT (10 days)

Write out database with 1 new entries
Data Base Updated
```
## Running server
To see availble options, run  python3 server.py -h. CA file, server cert and private key should be by default in correct place after run create_ca.sh script.

```bash
juki@JumppaHuitti:~/workspace/simplest/server$ python3 server.py -h
usage: server.py [-h] -p PORT [-u USER] [[EST-Python Client][f9e00641]-ca CAFILE] [-c CERT] [-k KEY]
                 [-cm {0,1,2}]


optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Server port (default: None)
  -u USER, --user USER  Login crendentials username:password (default: None)
  -ca CAFILE, --cafile CAFILE
                        Ca certificate (default: ./certs/cacert.pem)
  -c CERT, --cert CERT  server certificate (default: ./certs/servercert.pem)
  -k KEY, --key KEY     Certificate private key (default:
                        ./certs/serverkey.pem)
  -cm {0,1,2}, --certmode {0,1,2}
                        Certicate mode 0=CERT_NONE 1=CERT_OPTIONAL
                        2=CERT_REQUIRED (default: 1)
```
Following example should work almost out of box with [EST-Python client][f9e00641] and also with Curl scripts from [EST Testserver site][bfda9873].



```bash
juki@JumppaHuitti:~/workspace/simplest/server$ python3  server.py -p 4443 -u estuser:estpwd
```
This require client certicate addition to username and password.
```bash
juki@JumppaHuitti:~/workspace/simplest/server$ python3  server.py -p 4443 -u estuser:estpwd -cm 2
```
## Client examples
Enroll and re-enroll with [EST-Python Client][f9e00641]

```python
import est.client

ta= 'cacert.pem'
host = 'localhost'
port = 4443

implicit_trust_anchor_cert_path = ta

client = est.client.Client(host, port, implicit_trust_anchor_cert_path)

print("get cacerts")
# Get EST server CA certs.
ca_certs = client.cacerts()
print("get cacerts done ")

username = 'estuser'
password = 'estpwd'

client.set_basic_auth(username, password)

# Create CSR and get private key used to sign the CSR.
common_name = '127.0.0.1'
country = 'US'
state = 'Massachusetts'
city = 'Boston'
organization = 'Cisco Systems'
organizational_unit = 'ENG'
email_address = 'test@cisco.com'
priv, csr = client.create_csr(common_name, country, state, city,
                                     organization, organizational_unit,
                                     email_address)
print("Save private key...")
f = open("key.pem", "w")
f.write( priv.decode("utf-8") )

print("Enroll start..")
client_cert = client.simpleenroll(csr)

print("enroll done")
f = open("cert.pem", "w")
f.write( client_cert )
```
Re-enroll
```python
import est.client

ta= 'cacert.pem'
host = 'localhost'
port = 4443

implicit_trust_anchor_cert_path = ta

client = est.client.Client(host, port, implicit_trust_anchor_cert_path)

username = 'estuser'
password = 'estpwd'

client.set_basic_auth(username, password)

# Create CSR and get private key used to sign the CSR.
common_name = '127.0.0.1'
country = 'US'
state = 'Massachusetts'
city = 'Boston'
organization = 'Cisco Systems'
organizational_unit = 'ENG'
email_address = 'test@cisco.com'
priv, csr = client.create_csr(common_name, country, state, city,
                                     organization, organizational_unit,
                                     email_address)


print("REenroll start...")
# Re-Enroll: Renew cert.  The previous cert/key can be passed for auth if needed.
client_cert_new = client.simplereenroll(csr,cert =('./cert.pem','./key.pem'))
#following works when cert mode is CERT_OPTIONAL or CERT_NONE
#client_cert_new = client.simplereenroll(csr)
print("reenroll done")
f = open("cert.pem", "w")
f.write(client_cert_new)

print("Save new private key...")
f = open("key.pem", "w")
f.write(priv.decode("utf-8"))
```
  [f9e00641]: https://github.com/laurentluce/est-client-python "EST-Python Client"
  [51b5b8ee]: https://tools.ietf.org/html/rfc7030 "RFC7030"
  [bfda9873]: http://www.testrfc7030.com/ "EST Testserver site"
