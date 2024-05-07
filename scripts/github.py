#!/usr/bin/python3

# Note: This script also lives at https://6172-fall20-public.s3.amazonaws.com/github.py
# Thus, students can access it without first having to configure GitHub keys on their VM.
# Please make sure to also upload the latest version there by running `make upload-github`

import json
import urllib.request
import os
import subprocess
import sys

def prRed(skk): print("\033[91m{}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m{}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m{}\033[00m" .format(skk))
def prBoldYellow(skk): print("\033[01;33m{}\033[00m" .format(skk))


class UnauthenticatedError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

def make_github_request(path, authorization_token, json_payload=None):
    url = "https://github.mit.edu/api/v3{path}".format(path=path)
    headers = {
        "authorization": "token {authorization_token}".format(authorization_token=authorization_token),
        "accept": "application/vnd.github.v3+json",
    }
    if json_payload is not None:
        headers["content-type"] = "application/json"
    data = None if json_payload is None else json.dumps(json_payload).encode('utf8')
    req = urllib.request.Request(
        url,
        headers=headers,
        data=data
    )

    try:
        resp = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            prRed("Your GitHub access token is incorrect. Please correct it and re-run the script.")
            sys.stdout.flush()
            raise UnauthenticatedError()
        if e.code in (403, 404):
            prRed("Your GitHub access token is missing scopes. Please create a new access token with the scopes listed above.")
            raise UnauthorizedError()
        raise e
    status = resp.status
    response_body = resp.read().decode('utf8')
    json_body = json.loads(response_body)
    return json_body

def upsert_public_ssh_key():
    ssh_privatekey_path = os.path.expanduser("~") + "/.ssh/id_rsa"
    ssh_pubkey_path = ssh_privatekey_path + ".pub"
    if os.path.exists(ssh_privatekey_path) and os.path.exists(ssh_pubkey_path):
        prBoldYellow("Reusing existing key from " + ssh_privatekey_path)
        prBoldYellow("If you don't want this key to be used, delete it, remove it from your GitHub account, and rerun this script")
    else:
        subprocess.run(["ssh-keygen", "-t", "rsa", "-q", "-f", ssh_privatekey_path, "-N", ""], check=True)
    assert os.path.exists(ssh_privatekey_path)
    assert os.path.exists(ssh_pubkey_path)
    with open(ssh_pubkey_path) as f:
        ssh_key = f.read()
    return ssh_key

def get_github_username(authorization_token):
    user_info = make_github_request("/user", authorization_token)
    return user_info['login']

def call_lambda_function(github_username):
    # This is an AWS Lambda function. It lives here:
    # https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/setup_script/versions/$LATEST?tab=configuration
    # It creates the student copy of the repo and shares it with the student and staff
    url = "https://vws449ln9g.execute-api.us-east-1.amazonaws.com/default/setup_script"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = json.dumps({"username": github_username}).encode('utf8')
    req = urllib.request.Request(
        url,
        headers=headers,
        data=data
    )
    resp = urllib.request.urlopen(req)
    status = resp.status
    response_body = resp.read().decode('utf8')
    if status >= 400:
        raise RuntimeError("HTTP Exception: {status} {reason}:\n{body}".format(
            status=status,
            reason=resp.reason,
            body=response_body
        ))
    return response_body

def main(retries_remaining):
    try:
        token_file = os.path.join(os.path.expanduser("~"), ".github_token")
        authorization_token = None

        if os.path.exists(token_file):
            with open(token_file, "r") as f:
                authorization_token = f.read().strip()

        if authorization_token:
            prBoldYellow("Using existing token from " + token_file)
            prBoldYellow("If that token is wrong, please delete that file and rerun.")
            token_was_new = False
        else:
            authorization_token = input("Paste the access token here and press enter.\n")
            token_was_new = True

        prCyan("[1/4] Retrieving GitHub username")
        github_username = get_github_username(authorization_token)

        if token_was_new:
            with open(token_file, "w") as f:
                f.write(authorization_token)
        # add the SSH key in
        prCyan("[2/4] Generating SSH Key")
        public_ssh_key = upsert_public_ssh_key()
        prCyan("[3/4] Registering SSH key")
        try:
            make_github_request("/user/keys", authorization_token, {
                "title": "6.106 VM",
                "key": public_ssh_key
            })
        except urllib.error.HTTPError as e:
            if e.code == 422:
                print("SSH key already set up")
                pass  # ok, the SSH key is already on the account
            else:
                raise e
        prCyan("[4/4] Registering student username")
        _ = call_lambda_function(github_username)

        prGreen(f"Congrats! Your GitHub is set up. You can move on to the next step.")
    except (UnauthenticatedError, UnauthorizedError):
        if retries_remaining > 0:
            print("Retrying due to error...")
            try:
                main(retries_remaining - 1)  # try again on authorization failures
            except:
                raise
        else:
            raise

if __name__ == "__main__":
    prCyan("Welcome to MIT 6.106!")
    print("")
    print("We will now set up MIT GitHub.")
    print("Please navigate to \033[1;35mhttps://github.mit.edu/settings/tokens/new\033[00m and create a new personal access token with the following settings:")
    print("")
    print("Name this token MIT 6.106")
    print("")
    print("Then, select the following scopes (including all sub-scopes):")
    print(" - repo")
    print("   - repo:status")
    print("   - repo_deployment")
    print("   - public_repo")
    print("   - repo:invite")
    print(" - admin:public_key")
    print("   - write:public_key")
    print("   - read:public_key")
    print(" - user")
    print("   - read:user")
    print("   - user:email")
    print("   - user:follow")
    print("")
    prGreen("Finally, generate the token.")
    main(0)
