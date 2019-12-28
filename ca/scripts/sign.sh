#!/usr/bin/env bash

#Sign csr and base64 encode newly created certificate.
#Argumnets in: csr name.
[ -z "$CA_BASEDIR" ] || [ -z "$EST_BASEDIR" ] && { echo "Error: CA_BASEDIR or EST_BASEDIR not set, call first; source ./set_env.sh"; exit 1; }

#Sign request...
openssl ca  -batch -config $CA_BASEDIR/conf/openssl-ca.cnf -policy signing_policy -extensions signing_req -out $EST_BASEDIR/csr_req/$1.pem -infiles $EST_BASEDIR/csr_req/$1.csr

#base64 encode it
openssl crl2pkcs7 -nocrl -certfile $EST_BASEDIR/csr_req/$1.pem -out $EST_BASEDIR/csr_req/$1.p7b
#Remove pem file, other files deleted by est server itself
rm $EST_BASEDIR/csr_req/$1.pem
