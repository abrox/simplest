#!/usr/bin/env bash
#Delete all created files and directories

[ -z "$CA_BASEDIR" ] || [ -z "$EST_BASEDIR" ] && { echo "Error: CA_BASEDIR or EST_BASEDIR not set, call first; source ./set_env.sh"; exit 1; }


#Remove old files in case exist

rm -f   $CA_BASEDIR/index.txt*
rm -f   $CA_BASEDIR/serial.txt*
rm -rf  $CA_BASEDIR/certs
rm -f   $CA_BASEDIR/.rnd
rm -f   $CA_BASEDIR/cakey.pem
rm -rf  $CA_BASEDIR/csr_dir
rm -rf  $CA_BASEDIR/cacert.*

rm -rf   $EST_BASEDIR/certs
rm -rf   $EST_BASEDIR/csr_req
