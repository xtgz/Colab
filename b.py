#@title **Create User**
import os
username = "akuhnet" #@param {type:"string"}
password = "123456" #@param {type:"string"}

print("Creating User and Setting it up")

# Creat user
os.system(f"useradd -m {username}")

# Add user to sudo group
os.system(f"adduser {username} sudo")
    
# Set password user to 'root'
os.system(f"echo '{username}:{password}' | sudo chpasswd")

# Change default shell from sh to bash
os.system("sed -i 's/\/bin\/sh/\/bin\/bash/g' /etc/passwd")

print("User Created and Configured")
     

#@title **Google Drive Mount**

from google.colab import drive
drive.mount('/content/drive')
     

#@title **Start RDP**
#@markdown UPDATE
#@markdown Connect with RDP
#@markdown [Ngrok Auth Token](https://dashboard.ngrok.com/get-started/your-authtoken)
#@markdown Other Free VPS
#@markdown [akuh.net](https://www.akuh.net/)
./xfce4.sh
