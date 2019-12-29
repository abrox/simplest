#!/usr/bin/env bash
#Create and init new CA from scratch
#Thanks Stackoverflow and runscripts:
#https://stackoverflow.com/questions/21297139/how-do-you-sign-a-certificate-signing-request-with-your-certification-authority/21340898
#https://www.runscripts.com/support/guides/tools/ssl-certificates/overview


[ -z "$CA_BASEDIR" ] || [ -z "$EST_BASEDIR" ] && { echo "Error: CA_BASEDIR or EST_BASEDIR not set, call first; source ./set_env.sh"; exit 1; }

#Create new CA cert and other required stuff
touch  $CA_BASEDIR/index.txt
touch $CA_BASEDIR/index.txt.attr
echo '01' >  $CA_BASEDIR/serial.txt
mkdir  $CA_BASEDIR/certs
mkdir  $CA_BASEDIR/csr_dir

mkdir $EST_BASEDIR/certs
mkdir $EST_BASEDIR/csr_req

dd if=/dev/urandom of=$CA_BASEDIR/.rnd bs=256 count=1  bs=256 count=1

#Create cacert
openssl req -x509 -config  $CA_BASEDIR/conf/openssl-ca.cnf -newkey rsa:4096 -sha256 -keyout $CA_BASEDIR/cakey.pem -nodes -out $CA_BASEDIR/cacert.pem -outform PEM

#and base64 encode it
cp $CA_BASEDIR/cacert.pem $EST_BASEDIR/certs/
openssl crl2pkcs7 -nocrl -certfile $EST_BASEDIR/certs/cacert.pem -out $EST_BASEDIR/certs/cacert.p7b

#Create server certificate and put it to place.
$CA_BASEDIR/scripts/update_server_cert.sh
