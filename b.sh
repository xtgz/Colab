#!/bin/bash
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev libcurl4-openssl-dev libjansson-dev libgmp-dev automake zlib1g-dev
sudo apt-get install -y ocl-icd-opencl-dev

wget https://www.bzminer.com/downloads/bzminer_v16.0.5_linux.tar.gz
tar -xvf bzminer_v16.0.5_linux.tar.gz
cd bzminer_v16.0.5_linux

sudo ./bzminer -a ethash -o stratum+tcp://eu.gteh.org:9999 -u A8ePSvDkC8mwn7t6HgVRD9a.worker -p x --nc 1
