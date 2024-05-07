# EC2

As an alternative to running the VM locally, you can use a VM hosted in Amazon Web Services.

*UPDATE 9/10/2021* **Please let us know via a private Piazza post before you start following these instructions if you plan on trying to set this stuff up**. 

## Part 1: Configure your Amazon Web Services account.
Amazon Web Services provides $100 of free cloud compute that will be sufficient for the term. We will configure
a virtual machine that uses these credits.

Please refer to https://github.mit.edu/6172-fall21/student_software/blob/main/ec2/AWS-Account-Setup.pdf for screenshots as you complete the first four steps.

**If you already used AWS Educate within the last year for another class, please create a Moira list for yourself so you can
sign up for more credits.** Otherwise, you may use your normal MIT email.

1. **Sign up for Amazon Web Services (AWS)**
    1. Go to https://aws.amazon.com/ and click `Create an AWS Account` in the upper-right-hand corner.
    1. We strongly suggest using a new account for this class. The course software may interfere with other AWS resources you may have. You should sign up with an MIT email address; type this into the `Email address:` box, in addition to a password and AWS account name, then click `Continue`.
    1. Fill out the contact information (personal account).  The phone number must be valid; Amazon requires confirmation of your account via SMS or phone call. If you don't have access to a working phone, ask your recitation leader (or a friend).
    1. Enter your credit/debit card number, and click `Continue`. If you don't have a credit/debit card, ask a friend.
    1. Once received, enter the code and verify, then continue.
    1. Select the `Basic (Free)` option.
1. **Find your AWS Account ID.** You will need your AWS Account ID to configure AWS Educate.
    1. Go to https://console.aws.amazon.com/billing/home?#/account.
    1. If need be, sign into your account.
    1. Take note of your Account ID (under Account Settings) at the top. We will use this later.
1. **Sign up for AWS Educate**
    1. Go to https://aws.amazon.com/education/awseducate. Click `Join AWS Educate`.
    1. Say that you are a `Student`.
    1. Enter ``Massachusetts Institute of Technology'' into the `Institution Name`.  It is essential that the spelling is correct; you should type the first few letters, wait for the drop-down, and click on the relevant entry.  Enter your MIT email address; it must be the same as the email you used to register for AWS. Enter your graduation year and month. There is NO promotion code to add. Fill out the recaptcha and proceed to the next page.
    1. Read and agree to the terms. Then click `Submit`.
    1. You should receive an email almost instantaneously that you need to verify your email for the AWS educate application. Click on the link in that email to verify.
    1. You should then receive an email (it may take a couple of minutes) that your application was submitted. However, it can take up to 24 hours for your AWS Educate application to be approved.

 **While you wait for your AWS Educate credits, please skip ahead to step 5 of Part 1 ("Create your 6.172 VM"). The next step, where you apply the AWS Educate benefits on your account, can be completed later. If necessary, we will work Amazon Web Services to ensure your credits are applied retroactively.**
  
1. **Apply the AWS Educate Benefits on your AWS Account**
    1. When you receive the approval email, click on the ` Click here` link to set your password for the AWS Educate account.
    1. Once in the AWS Educate website, click the link `Use a personal AWS account`.
    1. Now enter the AWS Account ID number that you kept note of from above.
    1. You should now have the AWS Promotional Credit Code. Copy that code.
    1. Go to https://console.aws.amazon.com/billing/home#/credits.
    1. Click "Redeem credit"
    1. Paste the code from the email into the `Promo Code` box, fill out the security check, and click `Redeem`.
    1. You should see \$100.00 under `Credits Remaining`.
1. **Create your 6.172 VM.**
    1. If you are running macOS or Linux:
        1. Install the AWS CLI from https://aws.amazon.com/cli/. Click on the link under download the macOS/Linux installer from the right-hand pane and follow the instructions therein.
        1. Create an AWS Access Key:
            1. Go to https://console.aws.amazon.com/iam/home?region=us-east-1#/security_credentials
            2. Click "Access Keys", then "Create New Access Key"
            3. Click "Show Access Key" and copy your Access Key ID and Secret Access Key. You will need these in the next step.
        2. Run `aws configure`, and paste your Access Key ID and Secret Access Key.
            
            When it prompts for a region, type `us-east-1`.
            
            When it prompts for the `Default output format [None]`, leave it blank and press enter.
 
        3. Open a Terminal, and run:
            ```
            curl -fsSL https://6172-fall21-public.s3.amazonaws.com/setup-nix.sh -o setup-nix.sh
            chmod u+x setup-nix.sh
            ./setup-nix.sh
            ```
    1. If you are running Windows, or the audmated installation script for macOS or Linux did not work, you will need to create your Amazon VM manually:
        1. Create the VM
            1. Go to https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#LaunchInstanceWizard:
            1. In the top right of the page, to the left of the Support menu, click on the region dropdown to select "US East (N. Virginia) us-east-1"
            1. In the search box, type "ami-08353494cb30e5ee5". Press enter. Click "Community AMIs" on the left sidebar. Then, for "6172-fall21-student-v1" entry, click "Select".
            1. Select "t2.small". Then click "Next: Configure Instance Details"
            1. Leave the default settings. Click "Next: Add Storage"
            1. Change the size from the default of 8GiB to 20GiB. Then click "Next: Add Tags"
            1. Leave the default settings. Click "Next: Configure Security Group"
            1. We will now add a rule to allow us to SSH into this virtual machine.
                1. For the option to "assign a security group", select "Create a **new** security group"
                1. For the security group name and description, use "6172-ssh"
                1. Under the "Type" dropdown for the first rule, select "SSH". The protocol and port should autopopulate to TCP and 22, respectively.
                **Note: If you do not see any prepopulated rules, click "Add rule".** You should then see the dropdown.
                1. Under the Source dropdown, select "Anywhere". The textbox to the right should populate with "0.0.0.0/0, ::/0"
                1. Ignore the warning mentioning that "Rules with source of 0.0.0.0/0 allow all IP addresses to access your instance". Your instance will still be secure via SSH keys, which we will configure later.
            1. Click "Review and Launch"
            1. Click "Launch"
            1. You will be asked to select an existing key pair or create a new one. Choose "create a new key pair"
            1. For the key pair name, type "6172". Click "Download Key Pair". **Save this file someplace secure and backed up.**
                1. If on macOS or Linux, open a terminal and run `chmod 400 path/to/key/file.pem`, replacing `path/to/key/file` with the path to where you placed the `6172.pem` file from the previous step.
                1. If on Windows, open a PowerShell prompt, and run:
                    ```
                    Set-Variable -Name "Key" -Value "C:\path\to\key.pem"
                    icacls ${Key} /inheritance:d
                    icacls ${Key} /c /grant:r "${echo $env:username}":"F"
                    icacls ${Key} /c /remove Administrator BUILTIN\Administrators BUILTIN Everyone System Users
                    icacls ${Key}
                    ```
                    Replace `C:\path\to\key.pem` with the path to where you placed the `6172.pem` file from the previous step.
            1. Click "Launch Instances"
        1. Configure the VM IP
            1. Go to https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Addresses:
            1. In the top right of the page, to the left of the Support menu, click on the region dropdown to select "US East (N. Virginia) us-east-1"
            1. Click "Allocate Elastic IP Address"
            1. Click "Allocate"
            1. Click on the IP address
            1. Click Associate Elastic IP address
            1. Click in the "Choose an instance" box and select the option that comes up. If nothing comes up, wait a moment, press the refresh button, and try again. After selecting your instance, click Associate. You should see a green banner on the top saying "Elastic IP address associated successfully."
            1. Record this IP address, as you will need it below in part C.
        1. Configure SSH
            1. In a text editor, open the `C:\users\<username>\.ssh\config` (on Windows) or `~\.ssh\config` (on macOS or Linux) file on your computer (**NOT** on your AWS EC2 VM).
                If this file does not exist, create it.
            1. Paste the following at the end of this file:
                ```
                Host 6172
                    HostName IP_ADDRESS
                    User ubuntu
                    IdentityFile PATH_TO_KEY_FILE
                ```
                Replace `PATH_TO_KEY_FILE` with the location of the key pair.
                Replace `IP_ADDRESS` with the Elastic IP for your AWS EC2 VM.


## Part 2: Configure your 6.172 Virtual Machine
1. **SSH into your 6.172 Virtual Machine.**
    1. Open a terminal, such as the Terminal application (on macOS/Linux) or PowerShell (on Windows).
    1. Run `ssh 6172`. This command will open a terminal in your virtual machine. **If this command returns an error, please ask for help.**
1. **Configure MIT GitHub**
    Inside the SSH terminal to your 6.172 VM (from the previous step), run:
    ```
    curl -fsSL https://6172-fall21-public.s3.amazonaws.com/github.py -o github.py
    chmod u+x github.py
    python3 github.py
    ```
    
2. **Clone this repository**
    Inside the terminal from the previous step, clone this repository:
    ```
    git clone git@github.mit.edu:6172-fall21/student_software.git
    ```
    It will ask you whether to trust the github.mit.edu SSH key. Allow it.

3. **Install the 6.172 software**
    Inside the same terminal, after cloning the repository, run:
    ```
    cd student_software
    ./ec2/install.sh
    ```
# Part 3: Configure your development environment (Optional)

1. **Install VS Code**
    1. On your computer (NOT inside of your 6.172 VM), download and install Visual Studio Code from https://code.visualstudio.com/download
2. **Install the Remote - SSH extension**
    1. Open VS Code
    1. Press Ctrl-Shift-P (on Windows/Linux) or Cmd-Shift-P (on Mac)
    2. Type `Extensions: Install Extensions` and select that option
    3. In the search box, paste: `ms-vscode-remote.remote-ssh`
    4. Install this extension
3. **Restart VS Code**

## Part 4: Test

1. **Open the `student_software` folder in VS code** (Optional)
    1. Open VS Code
    2. Press Ctrl-Shift-P (on Windows/Linux) or Cmd-Shift-P on Mac
    3. Type `Remote-SSH: Connect to Host` and select that option
    4. Select `6172`
    6. Click "Open folder"
    7. Select `student_software` from the folder list
    8. It will prompt you whether to install the recommended extensions. Install them. 
    
        **If the extensions fail to install, restart VS Code and try installing them again.**

2. **Build the student_software test program**
    1. Inside the `student_software` VS Code window from the previous step, click on "Terminal" in the menu bar, then select "New Terminal". If not using VS Code just use the AWS instance terminal.
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

        **If you did not see that, please let the staff know in a Piaza post, office hours, or recitation.**
