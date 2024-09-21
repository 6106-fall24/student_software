#!/usr/bin/env python

import argparse
import urllib
import urllib.parse
import urllib.request
import ssl
import os
import json
import traceback
import time
import base64

timeout = 120 # seconds

DEBUG = False

server_cert = """
-----BEGIN CERTIFICATE-----
MIIFmjCCA4KgAwIBAgIUI1Cc3I3rhIMUh68RuqWwnZcNd74wDQYJKoZIhvcNAQEL
BQAwVDELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAk1BMRIwEAYDVQQHDAlDYW1icmlk
Z2UxDDAKBgNVBAoMA01JVDEWMBQGA1UEAwwNNDQuMTk2LjE3My45MDAeFw0yNDA5
MjExNzI3MTRaFw0yNTA5MjExNzI3MTRaMFQxCzAJBgNVBAYTAlVTMQswCQYDVQQI
DAJNQTESMBAGA1UEBwwJQ2FtYnJpZGdlMQwwCgYDVQQKDANNSVQxFjAUBgNVBAMM
DTQ0LjE5Ni4xNzMuOTAwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQC/
0OHC3BUxELnLusQS1219jo875KOa3wq0VSAUL1bfmKZ2ZgKr6nyUZRj4HTJxUWQO
8NQUoMUeoejWA0DbbmqbLwf7ryFbsnrFOmuoZ0oshM3dYOiiPJ0IgH/kCtGMKCis
ZwID96RCdb8Uw+ErTcpZROjzqbVHrbscnRULsWkV9xrZQSuO7hFTSCPp6UfRqpXx
F26YqLgTOiGKoYCg2oN72SNHPpmjVpl6Dl8GhFM4J02ulp1y0gjiUIpoOdTRMl6o
940I96wzfcdXuEibpogIWTRowzD+4G5147fcXnTe4j6N95iqaaE2Vuxs2C1FwE//
bAZgCUzd5DTpo9wL6T41DpI5nI2XtvVkyk4mwGUaFHTTlwFYYVYlDl/YJfBK9jNj
0fXTWx5xQRp9zrImOOC3LTYAf+IpYHFVUy41vcY/fC0FLXscxOF7rVN0AV0SLd8T
DSdEGUycJQELdFb/2ljMgw3esz83afwaVkfPa/Hief4tc8ZwIVZrfxTk/booAEnD
pdgV/dw/FU0nfbXNJDftrk+0ccMUajQvdR8G1cJ15yfXkQmugDjNFadLCnl9GHdK
O6xfhLhflXiEl7pM/xTlmfPYL4z4POMtaV5OotgVSkS9c2o2C58uQmHjBUOSXgEk
g+R7Sy5azvyFd25lNVBQkk+hBON3ezgol2Ka/Yx0XwIDAQABo2QwYjAdBgNVHQ4E
FgQU2AfSIdrknC34qIFGh60ZubLl/MAwHwYDVR0jBBgwFoAU2AfSIdrknC34qIFG
h60ZubLl/MAwDwYDVR0TAQH/BAUwAwEB/zAPBgNVHREECDAGhwQsxK1aMA0GCSqG
SIb3DQEBCwUAA4ICAQAilO0O08naWohNOkffLwlRb5IfM2y0OOQhszvSPoaeJ8h0
lYgYg30o64fMDWEMfFTbL3MFQF2Bbc0MA7scAkMBxugbQKoTOZjPup+YX7Tzwdk+
nvmtxtip5X+FtxRbPZcsnhBuboRp5TU/hwnbIuCInXJ8Jk1eYhSizvEiH2+/gZt1
TbWcGrRArD8DitI1yt+V/7HJjbH0XYQy27A4NR0NtsgweBJ+2DKb0hAWqu78Z+nA
BkVhks/JZC8JkzYGFyLzPtmS70jPWv/LkJYh7/S8vF6F4PxxxZ1C9J0Yo1Obs3bx
yQciybf9B3dDUQgSzn+F6vh/F2JzNWoZ6LGI8yFm0quQL6oCiCQQPSw4HmpYv7Up
qB7seSYeOXePe50Cpp3bjJzeCEbzI/QXwosQs02oWgZFoQwsXUNeT25U9IEGW+v6
IMowpXHax4Y7bxt9PFSWMuOdoWs6BBzuKJAh15uJ9E2N3w+MifaOThPQnzAfvfli
+U2+BCGhFeXciV+hbcPzV9lAnjOAkWMxgS/V1AHPbZbbH5eVEg29w5Brtqau9ELu
8rYHAbVLbbAd74W3gPSYkesYdxZlzdqMeqUJSZ8YOR68024eEVF2el33EHUWvWra
Psvft3GfxVuse3uysSDB1EY266WZ8HjIwtXpkLHT/P4M+Dv2OSY1+tZLwRkG/A==
-----END CERTIFICATE-----
"""

server_ip_port = "44.196.173.90:4443"
hidden_perf_directory = "/tmp/6106-student-jobs"

poll_interval = 1 # seconds

def process_response(response, script_args=None, job_id=None):
    result = json.loads(response["result"])["result_json"]
    if result["success"]:
        print("Job completed successfully.")
    else:
        print("Job failed.")
    print()
    print("--- Execution log:")
    print()
    print(result["execute_log"])
    
    if 'perf_data' in result and script_args:
        print()
        print("Perf data saved.")
        with open("perf.data", "wb") as f:
            f.write(base64.b64decode(result["perf_data"]))
        for idx, (orig_file, file) in enumerate(zip(script_args["orig_files"], script_args["files"])):
            if orig_file[:2] == './': 
                orig_file = orig_file[2:]
            with open(orig_file, 'rb') as f:
                orig_file_content = f.read()
                # write this to a hidden directory
                assert job_id is not None and script_args is not None
                # if job-{job_id} doesn't exist, create it
                if not os.path.exists(os.path.join(hidden_perf_directory, f"job-{job_id}")):
                    os.makedirs(os.path.join(hidden_perf_directory, f"job-{job_id}"))
                with open(os.path.join(hidden_perf_directory, f"job-{job_id}/{file}"), "wb") as f2:
                    f2.write(orig_file_content)
                    
    
def get_last_complete_job(username, token, ssl_ctx):
    query_params = {"username": username, "token": token}
    url_query = urllib.parse.urlencode(query_params)
    url = "https://" + server_ip_port + "/api/last_complete?" + url_query
    req = urllib.request.Request(url, method="GET")
    try: 
        with urllib.request.urlopen(req, context=ssl_ctx) as f:
            response = json.load(f)
            if response["success"]:
                print("Last completed job:")
                process_response(response)
                if "perf_data" in response["result"]:
                    print("Can't retrieve perf data for last job.")
    except urllib.error.HTTPError as e:
        if e.code == 400:
            response_json = json.load(e)
            if response_json["error"] == "pending_job":
                return None
        else: 
            response_json = json.load(e)
            error = response_json.get("error", None)
            if error: 
                print("\n" + "=" * 50)
                print("ERROR:".center(50))
                print("-" * 50)
                print(error)
                print("=" * 50 + "\n")


def submit_job(username, token, script_args, ssl_ctx, override_pending=False, is_util=False):
    query_params = {"username": username, "token": token, "debug": int(DEBUG)}
    if override_pending:
        query_params["override_pending"] = "1"
    query_params["is_util"] = 1 if is_util else 0
    url_query = urllib.parse.urlencode(query_params)
    url = "https://" + server_ip_port + "/api/submit?" + url_query

    file_dict = set()
    for idx, file in enumerate(script_args["orig_files"]):
        with open(file, 'rb') as f:
            file_content = f.read()
            base64_encoded = base64.b64encode(file_content).decode("utf-8")
            script_args[f"file{idx}"] = base64_encoded
        script_args["files"].append(os.path.basename(file))
        if os.path.basename(file) not in file_dict:
            file_dict.add(os.path.basename(file))
        else:
            print(f"Duplicate file: {os.path.basename(file)}, please ensure all files are unique.")
            raise Exception("Duplicate file")
    req_json = json.dumps(script_args).encode("utf-8")
    request = urllib.request.Request(url, data=req_json, method="POST")
    request.add_header("Content-Type", "application/json")
    
    try:
        response = urllib.request.urlopen(request, context=ssl_ctx)
        response_json = json.load(response)
        return response_json["job_id"]
    except urllib.error.HTTPError as e:
        if e.code == 400:
            response_json = json.load(e)
            if response_json["error"] == "pending_job":
                return None
        else: 
            response_json = json.load(e)
            error = response_json.get("error", None)
            if error: 
                print("\n" + "=" * 50)
                print("ERROR:".center(50))
                print("-" * 50)
                print(error)
                print("=" * 50 + "\n")
        raise e
    
def preprocess_args(script_args):
    remaining_args = []
    files = []
    do_perf = False
    for idx, arg in enumerate(script_args):
        if idx == 0 and arg.startswith("perf"):
            assert script_args[idx + 1] == "record"
            do_perf = True

        if os.path.isfile(arg):
            remaining_args.append(f"file{len(files)}")
            files.append(arg)
        else:
            remaining_args.append(arg)
    returns = {
        "command": " ".join(remaining_args),
        "orig_files": files,
        "files": [],
        "perf": do_perf, 
    }
    return returns

def main():
    if DEBUG:
        print("DEBUG:", DEBUG)
    parser = argparse.ArgumentParser()
    # parser.add_argument('script_args', nargs=argparse.REMAINDER, help='Arguments for the script')
    parser.add_argument(
        "--auth",
        help="Authentication token (defaults to ./auth.json in the same directory as this script)",
        default=None
    )
    parser.add_argument(
        "--cores", 
        type=int,
        help="Number of cores to request",
        default=1
    )
    parser.add_argument("--username", type=str, help="Username", default="")
    parser.add_argument("--token", type=str, help="Token", default="")
    parser.add_argument("--override-pending", action="store_true", help="Allow overriding pending jobs")
    parser.add_argument("--utils", action="store_true", help="Use utility queue instead of main queue, for testing purposes instead of benchmarking performance. Timeout will be longer.")
    parser.add_argument("--bypass-last-job", action="store_true", help="Bypass checking for your last job.")
    args, script_args = parser.parse_known_args()
    if len(script_args) == 0:
        print("Please provide a script to run.")
        exit(1)
    
    # turn script_args into a dictionary 
    script_args = preprocess_args(script_args)
    script_args["cores"] = args.cores
    
    if args.username != "" and args.token != "":
        username = args.username
        token = args.token
    else:
        ## Check if auth token is valid
        token_path = f"{os.path.expanduser('~')}/.telerun/auth.json"
        if not os.path.isfile(token_path):
            if args.auth is None:
                print("Please provide an authentication token.")
                exit(1)
            if not os.path.isfile(args.auth):
                print("Invalid authentication token.")
                exit(1)
            if not os.path.exists(os.path.dirname(token_path)):
                os.system("mkdir -p " + os.path.dirname(token_path))   
            os.system(f"cp {args.auth} {token_path}")
            print("Authentication token copied to", token_path)
                
        ## Load auth token
        with open(token_path, "r") as f:
            auth = json.load(f)
        username = auth["username"]
        token = auth["token"]
    is_util = args.utils
    ssl_ctx = ssl.create_default_context(cadata=server_cert)

    if not args.bypass_last_job:
        last_complete_job = get_last_complete_job(username, token, ssl_ctx)

    job_id = submit_job(username, token, script_args, ssl_ctx, override_pending=args.override_pending, is_util=is_util)
    if job_id is None:
        print("You already have a pending job. Pass '--override-pending' if you want to replace it.")
        exit(1)
    print("Submitted job")

    already_claimed = False
    old_time = time.time()
    while True:
        
        if time.time() - old_time > timeout:
            print("Time limit exceeded.")
            break
        try:
            time.sleep(poll_interval)
                
            url_query = urllib.parse.urlencode({"username": username, "token": token, "job_id": job_id})
            req = urllib.request.Request(
                "https://" + server_ip_port + "/api/status?" + url_query,
                method="GET",
            )
            with urllib.request.urlopen(req, context=ssl_ctx) as f:
                response = json.load(f)
            
            state = response["state"]
            if state == "pending":
                continue
            elif state == "claimed":
                if not already_claimed:
                    print("Compiling and running, took {:.2f} seconds to be claimed.".format(time.time() - old_time)) 
                    already_claimed = True
                continue
            elif state == "complete":
                # TODO: Don't double-nest JSON!
                process_response(response, script_args=script_args, job_id=job_id) 
                
                req = urllib.request.Request(
                    "https://" + server_ip_port + "/api/reported?" + url_query,
                    method="POST",
                )    
                with urllib.request.urlopen(req, context=ssl_ctx) as f:
                    response = json.load(f)
                    print("Reported job completion.")
                    
                break
        except urllib.error.HTTPError as e:
            if e.code == 400:
                response_json = json.load(e)
                if response_json["error"] == "pending_job":
                    return None
            else: 
                response_json = json.load(e)
                error = response_json.get("error", None)
                if error: 
                    print("\n" + "=" * 50)
                    print("ERROR:".center(50))
                    print("-" * 50)
                    print(error)
                    print("=" * 50 + "\n")
            raise e
        except KeyboardInterrupt as e: 
            print("Keyboard Interrupted.")
            if not already_claimed: 
                url_query = urllib.parse.urlencode({"username": username, "token": token, "job_id": job_id})
                req = urllib.request.Request(
                    "https://" + server_ip_port + "/api/delete?" + url_query,
                    method="POST",
                )
                with urllib.request.urlopen(req, context=ssl_ctx) as f:
                    response = json.load(f)
                    if response["success"]:
                        print("Job removed successfully.")
            break
        except Exception as e:
            traceback.print_exc()
            continue

if __name__ == "__main__":
    os.makedirs(hidden_perf_directory, exist_ok=True)
    main()
