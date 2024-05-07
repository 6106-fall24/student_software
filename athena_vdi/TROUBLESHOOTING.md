# Troubleshooting Athena VDI FAQ

## I cannot connect to my virtual desktop?

## I connected to my virtual desktop and I am getting prompted to an Ubuntu login page with one account called viewadmin or I am already logged in as viewadmin?

## I connected to my virtual desktop and I am getting prompted to an Ubuntu login page with my two accounts one is my kerb, but when clicking on it, it prompts me to enter a password?


1. If you are connected to the virtual desktop, click on connections tabs or three dots at the upper right of the screen.
2. Choose Logoff Desktop.
3. Close the client and launch it again.
4. Before you connect to the 6-106 virtual desktop, right click on the 6-106 icon or click on the three dots on the icon.
5. Choose Restart Desktop.
6. Try to connect now.
7. Once you connect follow 1.4 in [README](README.md) to disable power saving in the vm, this is the likely reason you are getting locked out
8. If you still can’t connect, please make a private post to Piazza and title it [Athena VDI Connectivity Issue] under the infrastructure folder and explain your problem.

# I am constantly getting locked out of my virtual desktop, why is that?

You might have power saving enabled inside you Ubuntu VM in which case follow 1.4 in [README](README.md) to disable it.

# I logged into my virtual desktop and I got an error message that my home directory is almost exceeding its quota, why is that?

Your home directory is your AFS locker on Athena. You have access to 2GB of storage there. It might be previous work folders that you have created when using Athena clusters through Athena Dialup, Athena Physical Clusters, or Athena Virtual Desktops for other classes or personal use. We recommend that you scan through your home directory and see what could be taking up a lot of space and delete them. 

You can check how much space a given directory is taking up by running: `du -hs /path/to/directory`

If none of your personal directories are taking up a lot of space, usually the following directories increase in size the longer you use the virtual desktop: `~/.mozilla`, `~/.config/Code`

You can also use this helper tool provided by Athena to help you investigate: http://kb.mit.edu/confluence/pages/viewpage.action?pageId=3907266 . However, it doesn’t work very well through Athena VDI, so you might need to run it through Athena Dialup.

# Executions involving clang-6106 (e.g. compilations) are taking a long time, why is that?

The first time you use clang-6106 in a session might take a long time (could take a minute or two) since the compilation is using the compiler that is saved on the class locker. First time to read big files on AFS is slow. However, subsequent reads during the same sessions will be fast because the compiler files are unchanged and are now loaded to your virtual machine.

# I am getting "Permission Denied" issues on my home directory? Why and how can I fix it?

Access to the home directory is managed by AFS and Kerberos. When you login the first time, AFS tickets are generated that let you access your files. These tickets typically expire after a day. If you keep your VM running for long, you might run into Permission Denied issue. A simple fix for this is to run the command `renew` in your working terminal. This will prompt you for you password and generate new tickets for you. 

If you are interested further, you can run the command `tokens` and it will show you your current tickets and when they expire. 