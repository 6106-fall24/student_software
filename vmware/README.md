# 6.172 Student Software: VMware

Welcome to 6.172!
Follow these instructions to prepare your machine for 6.172
for this Fall.

Note that installing the 6.172 software will require you to download
around 7.5GB of data and will take around 16GB of disk space after installation.
If you have a slow network connection, please be patient with downloading.
Please contact the course staff ASAP if these requirements present
challenges so we can discuss alternative options.

## Part 1: Download and install the 6.172 software

1. **Download VMware**

    **VMWare is the only _supported_ way to run the 6.172 virtual disk image**.
    You can download VMWare from IS&T.
    
    - **Windows/Linux:** [VMWare Workstation Pro version 15](https://ist.mit.edu/vmware/workstation)
    - **macOS:** [VMWare Fusion Pro version 11.5 or 12](https://ist.mit.edu/vmware/fusion)

    You can get the serial key for unlimited access from the same link above under 'License Key'.

    **Note:** For Linux users, if clicking the **Finish** button during installation does not work, you may need to run VMWare from the terminal:
    ```
    sudo vmware
    ```

2. **Download the 6.172 VM**

    Download the VMWare image for 6.172 from [here](https://6172-fall21-public.s3.amazonaws.com/6172UbuntuVMF21.ova).

    Please confirm the filename of the file you downloaded is `6172UbuntuVMF21.ova`

3. **Import the 6.172 VM into VMWare**
    - For VMWare Workstation (Windows/Linux)

        Click [here](https://imgur.com/a/BBQBe9C) for image-based instructions.

        1. Click "File" > "Open..."
        3. Navigate to where you downloaded the VMWare image and select the `6172UbuntuVM.ova` file
        3. When prompted, you can opt to save the VM in the default directory or a location you prefer

        VMWare Workstation may complain about Intel VT-x being disabled. If that happens, you will need to enable virtualization VT-x options from your machine's BIOS. A typical path on Thinkpad machines would be:
        **BIOS -> Security -> Virtualization -> Enable VT-x options (~2 options) -> Save (F10)**

    - For VMWare Fusion (MacOS)

        Click [here](https://imgur.com/a/mMZcukN) for image-based instructions.

        1. Click "File" > "Import"
        2. Click the "Choose File..." button in the window that pops up
        3. Navigate to where you downloaded the VMWare image and select the `6172UbuntuVM.ova` file
        3. When prompted, you can opt to save the VM in the default directory or a location you prefer 


**If you ran into any issues, please let the staff know via a private Piazza post.**

## Part 2: Configure your 6.172 VM
_For part 2, as an alternative to the terminal inside your 6.172 Virtual Machine, you may use a native terminal, such as the Terminal application (on macOS or Linux) or PowerShell (on Windows), to SSH into your 6.172 VM. (You will need to run `hostname -I` inside your 6.172 VM to discover its IP address.) Running a terminal natively can be less laggy and eliminate copy-and-paste issues. Here, we assume you are using the terminal application inside your 6.172 VM, for simplicity._

0. **Ensure your VM is connected to the network**
    1. Open a terminal in your 6.172 VM and run:
        ```
        hostname -I       # should be an IP address
        ping google.com   # should not fail
        ```

    2. If either of these commands does not look right, reboot your VM.

1. **Configure MIT GitHub**
    1. Log in to [MIT GitHub](https://github.mit.edu/) with your Touchstone/Kerberos account.
    2. Start the 6.172 VM. The password for the `ubuntu` user is `ubuntu`.
    3. Open a terminal in your 6.172 VM and run:
        ```
        curl -fsSL https://6172-fall21-public.s3.amazonaws.com/github.py -o github.py
        python3 github.py
        ```
        Follow along with the prompt about creating a [GitHub Personal Access Token](https://github.mit.edu/settings/tokens).

2. **Clone this repository**

    1. Inside the terminal from the previous step, clone this repository:
        ```
        git clone git@github.mit.edu:6172-fall21/student_software.git
        ```
        It will ask you whether to trust the github.mit.edu SSH key. Allow it.

3. **Install the 6.172 software**
    1. Inside the same terminal, after cloning the repository, run:
        ```
        cd student_software
        ./vmware/install.sh
        ```

        Make sure to copy the last few lines of the output when the script prompts you to do so.
<!---
4. **Configure SSH Keys locally**
    1. Open a terminal on your host computer (NOT inside the VM)
    2. Run `cat ~/.ssh/id_rsa.pub`
        1. If that command fails because the file does not exist, run `ssh-keygen -t rsa`. Pres enter until it finishes; the defaults are fine.
        2. Run `cat ~/.ssh/id_rsa.pub`
--->

## Part 3: Configure your development environment

1. **Install VS Code**
    1. On your computer (NOT inside of your 6.172 VM), download and install Visual Studio Code from https://code.visualstudio.com/download
2. **Install the Remote - SSH extension**
    1. Open VS Code
    1. Press Ctrl-Shift-P (on Windows/Linux) or Cmd-Shift-P (on Mac)
    2. Type `Extensions: Install Extensions` and select that option
    3. In the search box, paste: `ms-vscode-remote.remote-ssh`
    4. Install this extension
3. **Restart VS Code**
4. **Configure your SSH config**
    1. Open VS Code
    2. Press Ctrl-Shift-P (on Windows/Linux) or Cmd-Shift-P on Mac
    3. Type `Remote-SSH: Open Configuration File` and select that option
    4. Choose the first file
    5. Paste the output from Part 2, Step 3, at the end of the file
        (after any existing configurations) and save the file. If copy-paste
        is not working, you will need to manually type these lines.


## Part 4: Test

1. **Open the `student_software` folder in VS code**
    1. Open VS Code
    2. Press Ctrl-Shift-P (on Windows/Linux) or Cmd-Shift-P on Mac
    3. Type `Remote-SSH: Connect to Host` and select that option
    4. Select `6172`
    5. If it prompts for a password, type `ubuntu`.
    6. Click "Open folder"
    7. Select `student_software` from the folder list
    8. It will prompt you whether to install the recommended extensions. Install them. 
        
        If you miss the prompt:
            1. Press Ctrl-Shift-P (on Windows/Linux) or Cmd-Shift-P (on Mac)
            2. Type `Extensions: Install Extensions` and select that option
            3. Look to the Recommended tab of the Extensions menu
            4. Click Install on each of the recommended extensions.
    
        **If the extensions fail to install, restart VS Code and try installing them again.**

2. **Build the student_software test program**
    1. Inside the `student_software` VS Code window, click on Terminal, then Select New Terminal
    2. Inside the Terminal that appears at the bottom, run:
        ```
        cd ~/student_software
        make
        ./test_program
        awsrun ./test_program
        ```
        If everything worked correctly, you should see the following output.

        ```
        ubuntu@6172vm:~/student_software$ make
        clang -std=gnu11 -Wall -fopencilk  -O3 -DNDEBUG -ftree-vectorize -flto=full -march=native -Weverything -Werror -Wpedantic  -o fib.o -c fib.c
        clang -std=gnu11 -Wall -fopencilk  -O3 -DNDEBUG -ftree-vectorize -flto=full -march=native -Weverything -Werror -Wpedantic  -o sum.o -c sum.c
        clang -std=gnu11 -Wall -fopencilk  -O3 -DNDEBUG -ftree-vectorize -flto=full -march=native -Weverything -Werror -Wpedantic  -o main.o -c main.c
        clang -lrt -lm -fopencilk -flto -lXext -lX11  -o test_program fib.o sum.o main.o


        ubuntu@6172vm:~/student_software$ ./test_program
        Welcome to 6.172!


        ubuntu@6172vm:~/student_software$ awsrun ./test_program

        Submitting Job: ./test_program
        Waiting for job to finish...
        ==== Standard Output ====
        Welcome to 6.172!


        ==== Standard Error ====
        ```

        **If you did not see that, please let the staff know in a Piazza post, office hours, or recitation.**
