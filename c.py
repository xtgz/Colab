import os

username = "user" #@param {type:"string"}
password = "root" #@param {type:"string"}

print("Creating User and Setting it up")

# Creation of user
os.system(f"useradd -m {username}")

# Add user to sudo group
os.system(f"adduser {username} sudo")
    
# Set password of user to 'root'
os.system(f"echo '{username}:{password}' | sudo chpasswd")

# Change default shell from sh to bash
os.system("sed -i 's/\/bin\/sh/\/bin\/bash/g' /etc/passwd")

print(f"User created and configured having username `{username}` and password `{password}`")

#@title **RDP**
#@markdown  It takes 4-5 minutes for installation

import os
import subprocess

#@markdown  Visit http://remotedesktop.google.com/headless and copy the command after Authentication

CRP = "\"%PROGRAMFILES(X86)%\\Google\\Chrome Remote Desktop\\CurrentVersion\\remoting_start_host.exe\" --code=\"4/0AfJohXmSIX8fmRMufOVwtVLn37C9J72jB5dKQgTt5y2XZR9lBxJzDVwJMLkLoj2WgRL8MQ\" --redirect-url=\"https://remotedesktop.google.com/_/oauthredirect\" --name=%COMPUTERNAME%" #@param {type:"string"}

#@markdown Enter a Pin (more or equal to 6 digits)
Pin = 123456 #@param {type: "integer"}

#@markdown Autostart Notebook in RDP
Autostart = False #@param {type: "boolean"}


class CRD:
    def __init__(self, user):
        os.system("apt update")
        self.installCRD()
        self.installDesktopEnvironment()
        self.installGoogleChorme()
        self.finish(user)
        print("\nRDP created succesfully move to https://remotedesktop.google.com/access")

    @staticmethod
    def installCRD():
        print("Installing Chrome Remote Desktop")
        subprocess.run(['wget', 'https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb'], stdout=subprocess.PIPE)
        subprocess.run(['dpkg', '--install', 'chrome-remote-desktop_current_amd64.deb'], stdout=subprocess.PIPE)
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'], stdout=subprocess.PIPE)

    @staticmethod
    def installDesktopEnvironment():
        print("Installing Desktop Environment")
        os.system("export DEBIAN_FRONTEND=noninteractive")
        os.system("apt install --assume-yes xfce4 desktop-base xfce4-terminal")
        os.system("bash -c 'echo \"exec /etc/X11/Xsession /usr/bin/xfce4-session\" > /etc/chrome-remote-desktop-session'")
        os.system("apt remove --assume-yes gnome-terminal")
        os.system("apt install --assume-yes xscreensaver")
        os.system("systemctl disable lightdm.service")

    @staticmethod
    def installGoogleChorme():
        print("Installing Google Chrome")
        subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"], stdout=subprocess.PIPE)
        subprocess.run(["dpkg", "--install", "google-chrome-stable_current_amd64.deb"], stdout=subprocess.PIPE)
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'], stdout=subprocess.PIPE)

    @staticmethod
    def finish(user):
        print("Finalizing")
        if Autostart:
            os.makedirs(f"/home/{user}/.config/autostart", exist_ok=True)
            link = "https://colab.research.google.com/github/PradyumnaKrishna/Colab-Hacks/blob/master/Colab%20RDP/Colab%20RDP.ipynb"
            colab_autostart = """[Desktop Entry]
Type=Application
Name=Colab
Exec=sh -c "sensible-browser {}"
Icon=
Comment=Open a predefined notebook at session signin.
X-GNOME-Autostart-enabled=true""".format(link)
            with open(f"/home/{user}/.config/autostart/colab.desktop", "w") as f:
                f.write(colab_autostart)
            os.system(f"chmod +x /home/{user}/.config/autostart/colab.desktop")
            os.system(f"chown {user}:{user} /home/{user}/.config")

        os.system(f"adduser {user} chrome-remote-desktop")
        command = f"{CRP} --pin={Pin}"
        os.system(f"su - {user} -c '{command}'")
        os.system("service chrome-remote-desktop start")
        

        print("Finished Succesfully")


try:
    if CRP == "":
        print("Please enter authcode from the given link")
    elif len(str(Pin)) < 6:
        print("Enter a pin more or equal to 6 digits")
    else:
        CRD(username)
except NameError as e:
    print("'username' variable not found, Create a user first")

%env USE_AUTH_EPHEM=0

#@title **Google Drive Mount**
#@markdown Google Drive can be used as Persistance HDD for files.<br>

#@markdown **Choose a method (GDFuse Recommended)**
mount_method = "GDFuse" #@param ["GDFuse", "Native"]


#@markdown **Options for GDFuse** <br>
#@markdown - Visit https://github.com/astrada/google-drive-ocamlfuse/wiki/Team-Drives
label = "default" #@param {type:"string"}
mount_team_drive = False #@param {type:"boolean"}
force_mount = False #@param {type:"boolean"}

import os
import subprocess


class Drive():
    creds = {}
    mountpoint = ""
    deps = False
    
    debug = False

    def __init__(self, mountpoint="/content/drives", debug=False):
        os.makedirs(mountpoint, exist_ok=True)
        self.mountpoint = mountpoint
        self.debug = debug

    def _mount_gdfuse(self, mount_dir):
        os.makedirs(mount_dir, exist_ok=True)

        subprocess.run(
            ['google-drive-ocamlfuse',
             '-o',
             'allow_other',
             '-label',
             label,
             mount_dir,
            ]
        )

        print(f"Drive Mounted at {mount_dir}. If you get input/output error, then `team_drive_id` might be wrong or not accessible.")

    def _unmount_gdfuse(self, mount_dir):
        subprocess.run(
            ['fusermount',
             '-u',
             mount_dir,
            ]
        )
        os.rmdir(mount_dir)

    def auth(self):
        from google.colab import auth
        from oauth2client.client import GoogleCredentials

        auth.authenticate_user()
        
        creds = GoogleCredentials.get_application_default()
        self.creds = {
            "id": creds.client_id,
            "secret": creds.client_secret
        }

    def gdfuse(self, label, mound_team_drive=False, force_mount=False):
        import getpass

        if not self.creds:
            self.auth()

        if not self.deps:
            print("Installing google-drive-ocamlfuse")
            subprocess.run(['apt', 'install', 'software-properties-common python-software-properties module-init-tools', '-y'])
            subprocess.run(['add-apt-repository', 'ppa:alessandro-strada/ppa', '-y'])
            subprocess.run(['apt', 'update'])
            subprocess.run(['apt', 'install', '--assume-yes', 'google-drive-ocamlfuse'])
            self.deps = True

        base_dir = '/root/.gdfuse'
        config_dir = f'{base_dir}/{label}'
        mount_dir = f"{self.mountpoint}/{label}"

        if force_mount and os.path.exists(mount_dir):
            self._unmount_gdfuse(mount_dir)
        elif os.path.exists(mount_dir):
            print("Drive already mounted")
            return

        if not os.path.exists(config_dir) or force_mount:
            print(f"Please, open the following URL in a web browser: https://accounts.google.com/o/oauth2/auth?client_id={self.creds['id']}&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive&response_type=code&access_type=offline&approval_prompt=force")
            vcode = getpass.getpass("Enter the Auth Code: ")

            subprocess.run(
              ['google-drive-ocamlfuse',
                '-headless',
                '-id',
                self.creds['id'],
                '-secret',
                self.creds['secret'],
                '-label',
                label,
              ],
                text=True,
                input=vcode
            )

        if mount_team_drive:
            team_drive_id = input("Enter Team Drive ID: ")

            subprocess.run(
                ['sed',
                 '-i',
                 f's/team_drive_id=.*$/team_drive_id={team_drive_id}/g',
                 f'{config_dir}/config'
                ]
            )
        else:
            subprocess.run(
                ['sed',
                 '-i',
                 f's/team_drive_id=.*$/team_drive_id=/g',
                 f'{config_dir}/config'
                ]
            )

        self._mount_gdfuse(mount_dir)


    def native(self):
        from google.colab import drive
        mount_dir = f"{self.mountpoint}/Native"
        drive.mount(mount_dir)

if 'drive' not in globals():
    try:
        drive = Drive(f"/home/{username}/drives")
    except NameError:
        drive = Drive('/content/drives')

if mount_method == "Native":
    drive.native()
if mount_method == "GDFuse":
    drive.gdfuse(label, mount_team_drive, force_mount)

#@title **SSH**

! pip install colab_ssh --upgrade &> /dev/null

#@markdown Choose a method (Agro Recommended)
ssh_method = "Ngrok" #@param ["Agro", "Ngrok"]


#@markdown Copy authtoken from https://dashboard.ngrok.com/auth (only for ngrok)
ngrokRegion = "ap" #@param ["us", "eu", "ap", "au", "sa", "jp", "in"]

def runAgro():
    from colab_ssh import launch_ssh_cloudflared
    launch_ssh_cloudflared(password=password)

def runNgrok():
    from colab_ssh import launch_ssh
    from IPython.display import clear_output

    import getpass
    ngrokToken = getpass.getpass("Enter the ngrokToken: ")

    launch_ssh(ngrokToken, password, region=ngrokRegion)
    clear_output()

    print("ssh", user, end='@')
    ! curl -s http://localhost:4040/api/tunnels | python3 -c \
            "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'][6:].replace(':', ' -p '))"

try:
    user = username
    password = password
except NameError:
    print("No user found, using username and password as 'root'")
    user='root'
    password='root'


if ssh_method == "Agro":
    runAgro()
if ssh_method == "Ngrok":
    runNgrok()

