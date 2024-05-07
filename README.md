# 6.106 Student Software

Welcome to 6.106! This document will direct you through how to get setup with a VM and all the software you will need to use during the class.

## Part 1: VM Setup

The following section will guide you in setting up a local VM for running all course software. Recommended setup differs depending on your OS:

### macOS

For Macbooks, we recommend creating and running an Ubuntu machine with [OrbStack](https://orbstack.dev/).

1. Download OrbStack by downloading from the site above or by running the following command.

   ```
   brew install orbstack
   ```

2. Turn on Rosetta translation (this will allow your binaries to run much
   faster if you are on Apple silicon).

   ```
   orb config set rosetta true
   ```

3. Create a Linux VM for the class by opening named `6106` as follows:

   ```
   orb create -a amd64 ubuntu:noble 6106
   ```

   You can also create VMs through the OrbStack desktop app.

   We require for this class that you run an AMD VM, **not** an ARM VM.

4. SSH into your VM by running:

   ```
   ssh orb
   ```

5. Within the Linux terminal, install `git`:

   ```
   sudo apt-get update
   sudo apt-get install git
   ```

OrbStack supports file sharing between Linux and macOS, so you may choose to develop entirely within your macOS directories
if you find it convenient. Visit this [link](https://docs.orbstack.dev/machines/file-sharing) for more details.

You may also set up a remote VSCode connection from your Mac by downloading the
[Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)
extension and connecting to host `orb`.

### Windows

For Windows computers, we recommend running an Ubuntu distribution through Windows Subsystem for Linux (WSL).

1. Download WSL by running the following command:

   ```
   wsl --install --distribution Ubuntu-24.04
   ```

   If you have previously installed WSL, run the following command to update your VM to what we will be using in this class:

   ```
   wsl --set-default-version 2
   wsl --set-default Ubuntu-24.04
   ```

2. After installing, create a username and password as prompted.

3. Enter the WSL shell by running:

   ```
   wsl
   ```

The `C:` directory of your Windows machine is mapped to `/mnt/c/`.

### Linux

If you are working on a Linux machine, most of the course software should be natively compatible. However, the
setup scripts use the `apt` package manager to install packages, so if you are not using this package manager,
it would likely be easiest to do this setup in a virtual machine, e.g. setting up a Docker container. Some tools
used by this class also require a rather recent GLIBC version (2.32). If your GLIBC is not up to date, you should
also consider using a Docker container. For an example of how to set up a development environment in a Docker
container, see <https://code.visualstudio.com/docs/devcontainers/containers>.

<!-- Do note however that the course infrastructure was designed and tested for a clean install of Ubuntu 23.10.
You may run into less issues by developing on a VM with tools such as KVM or VMWare. -->

## Part 2: Configure Your 6.106 VM

Within your Linux machine,

### Configure GitHub credentials

1.  Check if an SSH key exists by running the following command.

    ```
    ls -al ~/.ssh
    ```

    If you find that `~/.ssh` does not exist or that no key (`id_ed25519.pub`) exists, continue to step 2.
    Otherwise, skip to step 3.

    **Note**: For users who already have SSH credentials on their local computers, OrbStack forwards your SSH-Agent to the VM.
    In this case there is no need to create a new SSH key as it should already exist at `~/.ssh` within the VM.
    Furthermore, if your local SSH key is already registered on GitHub, there is no need to add it a second time.
   
2.  Create an SSH key

    ```
    ssh-keygen -t ed25519 -C "your_email@example.com"
    ```

    Press **Enter** to accept the default file location, and enter a passphrase when prompted (or leave it empty).

3.  Copy the pub key from the terminal

    ```
    cat ~/.ssh/id_ed25519.pub
    ```

4.  Navigate to `Settings > SSH and GPG keys` on GitHub and click `New SSH Key`. Paste the pub key into the `Key` field and `Add SSH Key`.

5.  Verify your SSH connection

    ```
    ssh -T git@github.com
    ```

    You should see the following message

    ```
    Hi <user>! You've successfully authenticated, but GitHub does not provide shell access.
    ```

### Install the 6.106 software

1.  Clone this repo:

    ```
    git clone git@github.com:6106-fall24/student_software.git
    ```

2.  Inside the same terminal, after cloning the repository, run:

    ```
    cd student_software
    ./install.sh
    ```

    **Warning:** the installation will take quite a while (around 40 minutes in testing) and may
    occasionally require you to enter your password.

4.  After running the installation script, you will need to register your telerun credentials - run:

    ```
    authorize-telerun
    ```

    Enter your kerb as the username. To obtain your token, visit this [site](https://carlguo.scripts.mit.edu:444/serve_tokens.pl) and authenticate with your MIT certificate. If you don't have an MIT certificate or have not renewed your certificate since last school year, please generate one using [CertAid](https://ist.mit.edu/mit-apps/certaid) and reboot your computer. If the browser prompts you that the site is unsafe, just bypass the safety warning. 
5.  Configure your git identity:

    ```
    git config --global user.name "<your name>"
    git config --global user.email "<your github.com email>"
    ```

7.  (Optional) Configure git to use your favorite editor. For example, to use vim:

    ```
    git config --global core.editor vim
    ```

8.  Close your terminals and open a new one for some setup to be effective.

## Part 3: Using the Software

### Clang

Clang is the C compiler that we will use in this class. We provide a custom version of clang that is built with OpenCilk. If you want to compile some file through the command line or while writing Makefiles, you will want to use:

```
clang-6106
```

### telerun

telerun is the program you will use to submit jobs to the class instances for reliable performance benchmarking. You will learn more about his during your first homework. You can use it by running:

```
telerun [binary]
```

## Part 4: Test

### Build the student_software test program

1. Start a new terminal in your VM or through a remote VSCode window.

2. Inside the Terminal, run (You can ignore warnings/messages printed by the LLVM Gold plugin during compilation):

   ```
   cd ~/student_software
   make
   ./test_program
   telerun ./test_program
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


   user@vm:~/student_software$ telerun ./test_program

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
