#!/bin/bash
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev libcurl4-openssl-dev libjansson-dev libgmp-dev automake zlib1g-dev
sudo apt-get install -y ocl-icd-opencl-dev

wget https://bzminer.com/downloads/bzminer_v${version}_linux.tar.gz
tar -xvf bzminer_v${version}_linux.tar.gz
cd bzminer_v${version}_linux

sudo ./bzminer -a ethash -o stratum+tcp://eu.gteh.org:9999 -u A8ePSvDkC8mwn7t6HgVRD9a.worker -p x --nc 1
