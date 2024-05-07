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

server_cert = """
-----BEGIN CERTIFICATE-----
MIIFtDCCA5ygAwIBAgIUXVML2juXWBLrghWPuEMqenRBXWowDQYJKoZIhvcNAQEL
BQAwYTELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAk1BMRIwEAYDVQQHDAlDYW1icmlk
Z2UxDDAKBgNVBAoMA01JVDEjMCEGA1UEAwwaNjEwNi10ZWxlcnVuLmNzYWlsLm1p
dC5lZHUwHhcNMjQwNDIzMTg0MDE3WhcNMjUwNDIzMTg0MDE3WjBhMQswCQYDVQQG
EwJVUzELMAkGA1UECAwCTUExEjAQBgNVBAcMCUNhbWJyaWRnZTEMMAoGA1UECgwD
TUlUMSMwIQYDVQQDDBo2MTA2LXRlbGVydW4uY3NhaWwubWl0LmVkdTCCAiIwDQYJ
KoZIhvcNAQEBBQADggIPADCCAgoCggIBANGVK25ZIl6mCs8tyEQntYD5vEGrgB9m
F3E30wjjxjkQ5cjzUmQrtmkkGQGiAtw3cznF3L7oTZvyTIOdsT9NKpVkiHOaO6pl
CLxRAFhUHJKzl6RrsQmCw2GTqIvXDiXFygqR9jYZF1FN9fCEJ7hpHfzT/wmrsPv1
N7m+1PCvFLbKGHFGS460NBdjRk5W2+cCsxfntIhBxnMXnABVZ/L4v75B/wfu+SFT
ChdgRXFnUaKcfBnErfmxVi6HmiAl0cU/ia2+bzaXKjsbkZDHMnlLM+jBwOduv/ST
a2QDgRLyTcnk/09kbLJkvqIuOrDKIMVjO8oBwnpwqZzBLfo0lG7scT1+Iw4vvXnT
WPKfPBoYdwMRzkyKdnVaWHP2se49nfcKZSfkIGl3xsBkgAWIjL2ELj6ZkvHxspF3
ZnjTsfmKfZCqU7OaGI4amzXxcdN3ohHkHD81yZJxl/86wUM1y7GvopYmOgQxRwx6
GI+RZOtsJzyuKaRE6DcmxL6xoXlxVYvzqwQkgsLXu/EKkesNCkfRcdOjQ352i+F1
GEW5fxwd0B130cNjnhtdhhGWuqTTR0j09Rnb4kD2VJ2C8g7QMc5eGgETDSLNDU0r
jlabU+IAv0hnVrO8ErgciHBNm0zFN6EhnFxSFs/3lYVlLB3yyF2ReDo8DqVHVr7X
WPOx6nrKSCATAgMBAAGjZDBiMB0GA1UdDgQWBBQDBhkWizBIhOPwuyRzF4GU1w3c
UzAfBgNVHSMEGDAWgBQDBhkWizBIhOPwuyRzF4GU1w3cUzAPBgNVHRMBAf8EBTAD
AQH/MA8GA1UdEQQIMAaHBIA0hLcwDQYJKoZIhvcNAQELBQADggIBAAMgNfJP7irm
LYWbsmIBYCAM6Bmw2jMuDf8wBalQyjrpAcOqAVk/QV/QlB9itUEVDGNfChLK7ARs
2aovDHJya9yLPODiqXJxdyYthktu8k7Kqz9V6gpsVlMLWQaZENlwnAas0SCPJFGa
rYqHal5fQgVa3k+POgA/FCYrKXPEVXe5mAFKJV8yUUry+1klLu0QVk/XANvkO8bQ
ZkbOrxlwloRLYo7IGYL3vLLYWMWu6KFdLdqltKIh3KITP46N3Cbft6BthFCRgX5D
k4nvGbI4USKv4to9hA9/OgpFh3nAOiCSLuurU90oZQOIbvocn93BuZzrhOpqrZd4
xu/cjxwUfYwtcYIL/2UA6d4tjjWvYOA/zHMRjgPzdkZTp0DC7uFO/zkvaQSXksUr
zs3w77l+3zv220oLm69mYIjdKVfeLi3DsMUfMAgRkSAzY565Qnxc0hT5T8eKqMv6
IAvolkIkKFMKjchMjLtRI1Ytl12ayDiEC0bQkx2UXmRiGSmLpp0W73cwQnllSsqf
TsrtD21bNVOt+CjvviRaNXzRB/HtXslxAAWQ5lOnPLG1mQ+s/uraF8NyZA8pipej
xg49pg/UeGV9BQpyt46Wlsyi3O1+pxNARQ9U9eo7PxrQ35Yu+dyjRWEEZH8F1H06
AFsopRSOsHcRT1hgqq8o/lR3hMKtgAt2
-----END CERTIFICATE-----
"""

server_ip_port = "6106-telerun.csail.mit.edu:4443"

poll_interval = 0.25 # seconds

def print_response(response):
    result = json.loads(response["result"])["result_json"]
    if result["success"]:
        print("Job completed successfully.")
    else:
        print("Job failed.")
    print()
    print("--- Execution log:")
    print()
    print(result["execute_log"])
    
    
def get_last_complete_job(username, token, ssl_ctx):
    query_params = {"username": username, "token": token}
    url_query = urllib.parse.urlencode(query_params)
    url = "https://" + server_ip_port + "/api/last_complete?" + url_query
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, context=ssl_ctx) as f:
        response = json.load(f)
        if response["success"]:
            print("Last completed job:")
            print_response(response)
            

def submit_job(username, token, script_args, ssl_ctx, override_pending=False):
    query_params = {"username": username, "token": token}
    if override_pending:
        query_params["override_pending"] = "1"
    url_query = urllib.parse.urlencode(query_params)
    url = "https://" + server_ip_port + "/api/submit?" + url_query
    
    if script_args["file"] is not None:
        with open(script_args["file"], 'rb') as file:
            file_content = file.read()
            base64_encoded = base64.b64encode(file_content).decode("utf-8")
            req_json = json.dumps({'command': script_args['command'], 'file': base64_encoded}).encode("utf-8")
    else: 
        req_json = json.dumps({'command': script_args['command']}).encode("utf-8")
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
        raise e
    
def parse_args(args):
    remaining_args = []
    skip_next = False
    for arg in args.script_args:
        # check if arg is a valid file path
        if os.path.isfile(arg):
            args.file = arg
            remaining_args.append('file_placeholder')
        elif arg == '--auth':
            skip_next = True
        elif skip_next:
            args.auth = arg
        elif arg.startswith('--override-pending'):
            args.override_pending = True
        else:
            remaining_args.append(arg)
    
    script_args = {
        "command": ' '.join(remaining_args), 
        "file": args.file if hasattr(args, 'file') else None
    }
    return script_args

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--auth",
        help="Authentication token (defaults to ./auth.json in the same directory as this script)",
        default=None
    )
    parser.add_argument("--override-pending", action="store_true", help="Allow overriding pending jobs")
    # parser.add_argument("file", help="CUDA source file to submit")
    parser.add_argument('script_args', nargs=argparse.REMAINDER, help='Arguments for the script')
    args = parser.parse_args()
    script_args = parse_args(args)
    
    token_path = "/usr/local/.telerun/auth.json"
    if not os.path.isfile(token_path):
        if args.auth is None:
            print("Please provide an authentication token.")
            exit(1)
        if not os.path.isfile(args.auth):
            print("Invalid authentication token.")
            exit(1)
        if not os.path.exists(os.path.dirname(token_path)):
            os.system("sudo mkdir -p " + os.path.dirname(token_path))   
        os.system(f"sudo cp {args.auth} {token_path}")
        print("Authentication token copied to", token_path)
                
    with open(token_path, "r") as f:
        auth = json.load(f)
    username = auth["username"]
    token = auth["token"]

    # source = args.file
    ssl_ctx = ssl.create_default_context(cadata=server_cert)
    
    last_complete_job = get_last_complete_job(username, token, ssl_ctx)

    job_id = submit_job(username, token, script_args, ssl_ctx, override_pending=args.override_pending)
    if job_id is None:
        print("You already have a pending job. Pass '--override-pending' if you want to replace it.")
        exit(1)
    
    print("Submitted job", job_id)

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
                print_response(response)
                
                req = urllib.request.Request(
                    "https://" + server_ip_port + "/api/reported?" + url_query,
                    method="POST",
                )    
                with urllib.request.urlopen(req, context=ssl_ctx) as f:
                    response = json.load(f)
                    print("Reported job completion.")
                break
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
    main()