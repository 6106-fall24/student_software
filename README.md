# 6.106 Student Software

Welcome to 6.106! This document will direct you through how to get setup with a VM and all the software you will need to use during the class.

## Part 1: VM Setup

The following section will guide you in setting up a local VM for running all course software. Recommended setup differs depending on your OS:

### macOS

For Macbooks, we recommend creating and running an Ubuntu machine with [OrbStack](https://orbstack.dev/).

1. Download OrbStack by running the following command.

   ```
   brew install orbstack
   ```

   You may have to install [brew](https://brew.sh/) if it does not exist on your machine.

2. Create a VM for the class named `6106` as follows:

   ```
   orb create -a amd64 ubuntu:mantic 6106
   ```

   It is important for much of the course software that your VM is AMD-based as opposed to ARM-based.

3. SSH into your VM by running:

   ```
   ssh orb
   ```

4. Install Git:

   ```
   sudo apt-get update
   sudo apt-get install git
   ```

You should find that the root directory of your macOS is mapped to `/mnt/mac` in the OrbStack VM. Visit this [link](https://docs.orbstack.dev/machines/file-sharing) for more details.

### Windows

For Windows computers, we recommend running an Ubuntu distribution through Windows Subsystem for Linux (WSL).

1. Download WSL by running the following command:

   ```
   wsl --install --distribution Ubuntu
   ```

   If you have previously installed WSL, run the following command to update your VM to what we will be using in this class:

   ```
   wsl --set-default-version 2
   wsl --set-default Ubuntu-20.04
   ```

2. After installing, create a username and password as prompted.

3. Enter the WSL shell by running:

   ```
   wsl
   ```

The `C:` directory of your Windows machine is mapped to `/mnt/c/`.

### Linux

If you are working on a Linux machine, most of the course software should be natively compatible.

Do note however that the course infrastructure is designed for Ubuntu 23.10. You may run into less issues, therefore, by developing on a VM with tools such as KVM or VMWare.

## Part 2: Configure Your 6.106 VM

Within your Ubuntu machine,

### Configure GitHub credentials

1.  Create an SSH key

    ```
    ssh-keygen -t ed25519 -C "your_email@example.com"
    ```

    Press **Enter** to accept the default file location, and enter a passphrase when prompted (or leave it empty).

2.  Copy the pub key

    ```
    pbcopy < ~/.ssh/id_ed25519.pub
    ```

3.  Navigate to `Settings > SSH and GPG keys` on GitHub and click `New SSH Key`. Paste the pub key into the `Key` field and `Add SSH Key`.

4.  Verify your SSH connection

    ```
    ssh -T git@github.com
    ```

    You should see the following message

    ```
    Hi <user>! You've successfully authenticated, but GitHub does not provide shell access.
    ```

Note: For users who already have SSH credentials on their local MacBooks, OrbStack forwards your SSH agent to the VM. In this case there is no need to create a new SSH key - it should already exist at the standard directory within the VM. Furthermore, if your local SSH key is already registered on GitHub, there is no need to add it a second time.

### Install the 6.106 software

1.  Clone this repo:

    ```
    git clone git@github.com:MIT-6-106/student_software.git
    ```

2.  Inside the same terminal, after cloning the repository, run:

    ```
    cd student_software
    ./install.sh
    ```

3.  (Optional) Configure git to use your favorite editor. For example, to use vim:

    ```
    git config --global core.editor vim
    ```

4.  Close your terminals and open a new one for some setup to be effective.

## Part 3: Using the Software

<!-- ### VSCode:

Visual Studio Code is the development environment we recommend using. It has many builtin features that are useful for big projects development. The setup script your ran before should have installed the newest version for you!

You won't be able to access VS Code through the GUI or by typing "code" into the command line. This is due to some features not being available on AFS.

You can alternatively run it from the terminal using:

      run-vscode-6106

This will launch vscode and you should be able to pass parameters to it, like you would normally use `code`. -->

### Clang

Clang is the C compiler that we will use in this class. We provide a custom version of clang that is built with OpenCilk. If you want to compile some file through the command line or while writing Makefiles, you will want to use:

```
clang-6106
```

### awsrun

awsrun is the program you will use to submit jobs to the class AWS instances for reliable performance benchmarking. You will learn more about his during your first homework. You can use it by running:

```
awsrun [binary]
```

## Part 4: Test

<!-- 1. **Open the `student_software` folder in VS code**
    It will prompt you whether to install the recommended extensions. Install them.
    If you miss the prompt:
    1. Press Ctrl-Shift-P
    2. Type `Extensions: Install Extensions` and select that option
    3. Look to the Recommended tab of the Extensions menu
    4. Click Install on each of the recommended extensions.

**If the extensions fail to install, restart VS Code and try installing them again.** -->

### Build the student_software test program

1. Start a new terminal in your VM or inside the `student_software` VS Code window, click on Terminal, then Select New Terminal

2. Inside the Terminal, run (You can ignore warnings/messages printed by the LLVM Gold plugin during compilation):

   ```
   cd ~/student_software
   make
   ./test_program
   awsrun ./test_program
   ```

   If everything worked correctly, you should see the following output.

   ```
   user@vm:~/student_software$ make
   clang-6106 -std=gnu11 -Wall -fopencilk  -O3 -DNDEBUG -ftree-vectorize -flto=full -march=native -Weverything -Werror -Wpedantic  -o fib.o -c fib.c
   clang-6106 -std=gnu11 -Wall -fopencilk  -O3 -DNDEBUG -ftree-vectorize -flto=full -march=native -Weverything -Werror -Wpedantic  -o sum.o -c sum.c
   clang-6106 -std=gnu11 -Wall -fopencilk  -O3 -DNDEBUG -ftree-vectorize -flto=full -march=native -Weverything -Werror -Wpedantic  -o main.o -c main.c
   clang-6106 -lrt -lm -fopencilk -flto -lXext -lX11  -o test_program fib.o sum.o main.o



   user@vm:~/student_software$ ./test_program
   Welcome to 6.106!


   user@vm:~/student_software$ awsrun ./test_program

   Submitting Job: ./test_program
   Waiting for job to finish...
   ==== Standard Output ====
   Welcome to 6.106!


   ==== Standard Error ====
   ```

   **If you did not see that, please let the staff know in a Piazza post, office hours, or recitation.**

<!-- ## Part 6: Troubleshooting Athena VDI FAQ

Please, read the following [FAQ](TROUBLESHOOTING.md) to familiarize yourself with some of the problems people have run into in the past and how to fix them. -->

<!-- ## (Optional) Part 5: Use Athena Dialup to Mount your locker locally

These are optional instruction on how to mount your locker directory locally on your machine through vscode or `sshfs`. You can completely rely on Athena VDI to complete the assignments for this class. You should only follow these steps if you prefer to minimize your interaction with the GUI provided by VMWare Horizon.

Athena Dialup is another way to get access to computing power on the Athena Infrastructure. You will have access there to your AFS directory as well. So, your home directory will be the same as in Athena VDI.

Athena Dialup only provides access to some machine through ssh, so you will only get access to a terminal on that machine.

     Note: on Athena Dialup, some software necessary software to work with the class might not run through athena dialup. We don't recommend trying to run software for the class from Athena Dialup

The nice thing is that you will be able to access your files from both ends. So, you can have both running. Use Athena Dialup for writing code on your AFS locker, but then switch to the Athena VDI GUI to run tasks.

1. Configure your development environment

    1. **Install VS Code**
    1. On your computer (NOT inside of your 6.106 VM), download and install Visual Studio Code from https://code.visualstudio.com/download
    2. **Install the Remote - SSH extension**
    1. Open VS Code
    1. Press Ctrl-Shift-P (on Windows/Linux) or Cmd-Shift-P (on Mac)
    1. Type `Extensions: Install Extensions` and select that option
    1. In the search box, paste: `ms-vscode-remote.remote-ssh`
    1. Install this extension
    3. **Restart VS Code**
    4. **Configure your SSH config**
    1. Open VS Code
    2. Press Ctrl-Shift-P (on Windows/Linux) or Cmd-Shift-P on Mac
    3. Type `Remote-SSH: Open Configuration File` and select that option
    4. Choose the first file
    5. Add the following entry to the file:
    ```
    Host athena
     HostName athena.dialup.mit.edu
     User [Your Kerberos without @mit.edu]
    ```
    It is likely, however, that this setup won't work, when you try to connect in the next step, since Athena Dialup uses two factor authentication. In that case, there is a fix that works if you are running Linux/MacOS (If you are running Windows, you will need to connect with `sshfs`. See below for more information). You will need to change the entry above to:
    ```
    Host athena
     HostName athena.dialup.mit.edu
     User [Your Kerberos without @mit.edu]
     ControlMaster auto
     ControlPath ~/.ssh/sockets/%r@%h-%p
     ControlPersist 600
    ```

2. **Connect with VSCode to Athena Dialup**

    1. Open VS Code
    2. Press Ctrl-Shift-P (on Windows/Linux) or Cmd-Shift-P on Mac
    3. Type `Remote-SSH: Connect to Host` and select that option
    4. Select `athena`
    5. It should ask you to do a two factor authentication. You should be able to enter your kerberos password, then use Duo. If your connection keeps resetting, then you will need to go back to step `6.3.4.5` and fix the ssh config entry (this would work for Linux/MacOS). If you are running Windows, see step `6.5` on how to use `sshfs`.
    6. Click "Open folder". You might be asked to authenticate again here.
    7. You can now choose which directory you want to load into your vscode from your Athena directory (this should be your home directory or a homework/project directory).

3. **Using sshfs to mount your AFS directory locally**:

    If you have gone through the previous steps and failed to ssh to athena dialup through VSCode (most likely you are using Windows), you can follow the following instructions to learn how to use `sshfs`/`fusermount3`. (Note: on older versions of Ubuntu, 18.04 or older, the command you will need to use is `fusermount` and the package to download it with is called `fuse`)

    1. If you are on Windows, the easiest way to be able to run the commands above is to use WSL to run Ubuntu. You can download Ubuntu20.04 through the Microsoft Store. It will provide with an Ubuntu terminal to run Linux executables.
    2. Install `sshfs` and `fusermount3`:
    ```
    sudo apt install sshfs
    sudo apt install fusermount3
    ```
    3. You can learn about both commands by reading the man pages:
    1. `sshfs`: https://man7.org/linux/man-pages/man1/SSHFS.1.html
    2. `fusermount3`: https://man7.org/linux/man-pages/man1/fusermount3.1.html
    4. You should create a directory to always mount you AFS directories to:
    ```
     mkdir ~/athena
    ```
    5. Mount your Athena home directory locally (which is your AFS directory):
    ```
    sshfs kerberos@athena.dialup.mit.edu: ~/athena
    ```
    Or mount a specific directory:
    ```
    sshfs kerberos@athena.dialup.mit.edu:/path/to/directory ~/athena
    ```
    6. Once you are done using the mounted filesystem, you should remember to always unmount it:
    ```
    fusermount3 -u ~/athena
    ```
    7. It might be worth it to create aliases for the commands above in order to avoid typing them every time by adding the following two lines to your `~/.bash_aliases` file.

    ```
    alias mount_athena="sshfs kerberos@athena.dialup.mit.edu: ~/athena"
    alias unmount_athena="fusermount3 -u ~/athena"
    ```

    You will have to close and rerun your terminal for these commands to be usable or just run

    ```
    source ~/.bash_aliases
    ```

    Now you can simply run them with:

    ```
    mount_athena
    unmount_athena
    ```

    8. Now you can open projects on your AFS directory like you would any other directory in VSCode:
    ```
    cd ~/athena/path/to/project
    code .
    ```

4. Install awsrun:

    1. From your Athena Dialup terminal, run:

````

./scripts/install_awsrun_athena_dialup.sh

```

```
```` -->
