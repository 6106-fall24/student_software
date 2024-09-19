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
MIIFmDCCA4CgAwIBAgIUfiuE1HuIO7z2hnQmhDXOExQQc14wDQYJKoZIhvcNAQEL
BQAwUzELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAk1BMRIwEAYDVQQHDAlDYW1icmlk
Z2UxDDAKBgNVBAoMA01JVDEVMBMGA1UEAwwMMy44NC4xMjIuMjI5MB4XDTI0MDkx
NzIzMTYwMloXDTI1MDkxNzIzMTYwMlowUzELMAkGA1UEBhMCVVMxCzAJBgNVBAgM
Ak1BMRIwEAYDVQQHDAlDYW1icmlkZ2UxDDAKBgNVBAoMA01JVDEVMBMGA1UEAwwM
My44NC4xMjIuMjI5MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA1R++
x+KNLaruTkpXJwHNdTUhycNPU+tFT4Nf2p+52v7r1qn320jchKBTSA7iaQ3RmhNB
O8nTmyGxuklFcrG9O9581aOLhrA+0Q+i4jptwFDAtn7XaMGdYwT44HV+iVN1dg2C
ZdYohEAaNFFLigz1HLVftY91uf1/0w6fpaR8cFcCt/qmbdLsuvTs1/FDoWmtUngt
znidIn6kkwSvNedrP7lfAEzci1jARr3Kmd+g3ETuabnnp+8qwbov3xpvX5c6Z1Ay
skLAx8J/4bdNLvH3iwSaXjDn1tLNqZ2xcJDSthuF0am+e75WsI76qNTf0leeYDx+
zbWMOEQwx3ev9oyJ3VVcensXs6Mm2KjDc8MsGOFdBrQWUUrzFZSuWeFedfHFz4st
4sVD6pKE17ukRTnzdK+F09jSfLbqq+mWlk3JxrFwIhwCjYYpEGJRp2hzvPNnYEEF
w42d9HQZOwkrCDYbskEgKwdpGwxAhfZUyEHrmwnrxbaq335oib2Lv6ElXwCaqJJc
2T8JdqR3moKr7JDclLtUJYL3fbHk2DtYlQgolaRfLSqd7WlBS0wrekHJEAsY/mEU
OefwRHX/R94Am1OFMts+JzkKpEoKy35hLwfM9XNdKEk6y5fClzfOnmvbMWEnBOXP
2cHWWD9VhWNTvG0TyisdDB3lFM3GwmWd0CLAJRECAwEAAaNkMGIwHQYDVR0OBBYE
FBmqzLbEm+YkguFDTlgIigUaDZKOMB8GA1UdIwQYMBaAFBmqzLbEm+YkguFDTlgI
igUaDZKOMA8GA1UdEwEB/wQFMAMBAf8wDwYDVR0RBAgwBocEA1R65TANBgkqhkiG
9w0BAQsFAAOCAgEAoaP0kRXSFV9KjZtgBF1Qxjnuwv8r427hiRACoxoCY6bhCoow
3ql+Upjr2aN+pXlcxM34P657sW4MgtuSbm+ikcWumWr6eHyxQaumBn8LhbOJJwIw
SI9MVIT7I49Eh5+3qCdBd+pSHJh+QFy8ANMXFnRh7A4u7wsIFvBMQ3jkGlZ2H/rH
KDeWG/wwcxMXGGl12NDCl8A+VRdPuH0LLPxxzZoGEQXgehDHeKhX4k8KxbcPNyjE
yhKjV55d5KbE/EE5FDNu2YaBjjpJ+ALK5yCbauHbA9Iau2kbgbUknb5C0StaxyA0
qTex27pONTC+ijoATS1TPmhtYf2tv9v/MEMGSwic9qzZXOD3D/BSyF5vwFpjhqcL
0iZ8clDf+dLmJq/XceFRFWmdGHZRlE/5lVDeM7jpFLxHt23UTpMkC+x82BKGJPHR
32jR4wzbnrNBIvYq2AqWOApc4OVwFJ+h4fwfMUTBu5uLR6xdlCZHONgBS5hPgf1q
zGVrEgBi2JgAPCKMUyJWmZrD7fxcQCj9K3oOz3iDd+baCRahkccsSvRdVQunmmJ2
vrrAXIzTR3knr4IEchvO/Ufj/bqzms8RDmuNjY0WexEfPCl/JExIEzsY9XCTNE05
0IxQ4aY0auw8jBtPBOgtFxVuR/zOe1MNEFFQDBy/0r05RoYpER48eRU348k=
-----END CERTIFICATE-----
"""

server_ip_port = "3.84.122.229:4443"
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
        for idx, file in enumerate(script_args["files"]):
            if file[:2] == './': 
                file = file[2:]
            with open(file, 'rb') as f:
                file_content = f.read()
                # write this to a hidden directory
                assert job_id is not None and script_args is not None
                if not os.path.exists(os.path.join(hidden_perf_directory, f"job-{job_id}")):
                    os.makedirs(os.path.join(hidden_perf_directory, f"job-{job_id}"))
                with open(os.path.join(hidden_perf_directory, f"job-{job_id}/{file}"), "wb") as f2:
                    f2.write(file_content)
                    
    
def get_last_complete_job(username, token, ssl_ctx):
    query_params = {"username": username, "token": token}
    url_query = urllib.parse.urlencode(query_params)
    url = "https://" + server_ip_port + "/api/last_complete?" + url_query
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, context=ssl_ctx) as f:
        response = json.load(f)
        if response["success"]:
            print("Last completed job:")
            process_response(response)
            if "perf_data" in response["result"]:
                print("Can't retrieve perf data for last job.")

def submit_job(username, token, script_args, ssl_ctx, override_pending=False, is_util=False):
    query_params = {"username": username, "token": token}
    if override_pending:
        query_params["override_pending"] = "1"
    query_params["is_util"] = 1 if is_util else 0
    url_query = urllib.parse.urlencode(query_params)
    url = "https://" + server_ip_port + "/api/submit?" + url_query
    
    if "files" in script_args:
        for idx, file in enumerate(script_args["files"]):
            with open(file, 'rb') as f:
                file_content = f.read()
                base64_encoded = base64.b64encode(file_content).decode("utf-8")
                script_args[f"file{idx}"] = base64_encoded
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
        "files": files,
        "perf": do_perf
    }
    return returns

def main():
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
