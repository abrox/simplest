#!/usr/bin/env bash
#Update EST server cert
[ -z "$CA_BASEDIR" ] || [ -z "$EST_BASEDIR" ] && { echo "Error: CA_BASEDIR or EST_BASEDIR not set, call first; source ./set_env.sh"; exit 1; }
#Create certificate signing request...
openssl req -new -config $CA_BASEDIR/conf/est_server_cert.cnf  -newkey rsa:2048 -sha256 -nodes -keyout $EST_BASEDIR/certs/serverkey.pem -out $CA_BASEDIR/csr_dir/servercert.csr -outform PEM
#And sign it
openssl ca  -batch -config $CA_BASEDIR/conf/openssl-ca.cnf -policy signing_policy -extensions signing_req -out $EST_BASEDIR/certs/servercert.pem -infiles $CA_BASEDIR/csr_dir/servercert.csr
#remove csr
rm $CA_BASEDIR/csr_dir/servercert.csr
