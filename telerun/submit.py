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
MIIFmjCCA4KgAwIBAgIUb9dIdMa8pJtTQjQTNbk74eO9GO0wDQYJKoZIhvcNAQEL
BQAwVDELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAk1BMRIwEAYDVQQHDAlDYW1icmlk
Z2UxDDAKBgNVBAoMA01JVDEWMBQGA1UEAwwNNTQuMTY2LjE0LjExNzAeFw0yNDA5
MDMwMjIzMTZaFw0yNTA5MDMwMjIzMTZaMFQxCzAJBgNVBAYTAlVTMQswCQYDVQQI
DAJNQTESMBAGA1UEBwwJQ2FtYnJpZGdlMQwwCgYDVQQKDANNSVQxFjAUBgNVBAMM
DTU0LjE2Ni4xNC4xMTcwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQDC
QM8odyBBbVWM3bPYSS58ybuc5bz5Tm1Pk5NgZwabT8+6eph6yy/0UCQrvxM/ZRPo
89iGMD63lcdb3LNDcHRiZo3+kHvlgSDbhJbvb3Qo07FqgjX/Tl7BeRki0G5yM6wU
+ANqbQ+hdlmj2x/MnYBSUD3gTTr46g4c+H3nUcCCU1uu3K9sf1zdrEMUS7IElqpL
ZoJDGzBQrT3oFFn6lgbLsg3Spt8BkWxTJUK2t6pnNy8GgCOwlq9W726CI8LisbfG
fVJSHU+gG2T13bPxMXEesA2llivJnIxD3n0EpB8/W59Ha6qwwzcRKCDmTtv5Juqo
SfXpX5/ymoKZ5QrYXTmI1g5/mIhYYpVkeAwoYWb92YzUtqYr7MxV8oE90HKGA6hy
ZyiuNW3RtLFBNppYSEtfMhW9tnqDkFwi1li4QVA7ScqoxSWyFbNZ7XiUbCHY9NDr
qNXhlhSXE2kIXU/2EyX0S2U6y1BsYuIosB4QptnfqfxbBXkpMhpUsqkD+ETIljhG
9KiEbm5+UtnGWp4hcnfC6tBr7AxkuiYi6kzMlpPlz0ZVSBwiFSyJ0kDlqn3VWruQ
BrKjle849NHaqMSNiACBWA+b+lMa6WbHraxtKQ41ykjA2wTX83I4gJHA1sbz/YrM
22XEuMdXrASTcolkBpPam3JfbGXG/V5bZXsj4GqJGQIDAQABo2QwYjAdBgNVHQ4E
FgQUxqA4/KFu00gj+wEmtyX1wb6eH8IwHwYDVR0jBBgwFoAUxqA4/KFu00gj+wEm
tyX1wb6eH8IwDwYDVR0TAQH/BAUwAwEB/zAPBgNVHREECDAGhwQ2pg51MA0GCSqG
SIb3DQEBCwUAA4ICAQAS89/Eku40YhmqohnShvNx+tIFR3xhEieSXRR4N6ax/HWj
0OD7qDAvLyIQTnZMF/X6vXAwO3cZHvI0CPydKUMv9rrNKhRFVZtcIWAK1cz5aeZa
4+DgcpqmyTZgabtSoj+pVxxBaRHQwQ/4+eToAzATc/S9P93lqCf7itxRUxo5yJ4s
I5cqQrSUXsJMw9MgnMvZVsJu7WvZcfOqstPs9b2kOSJjanjA04jJ0a6/2TTj0g0Q
QdibQYT3/SwAOJyuVf4XDeiJP7lBLpujXZLtbs9oRYlMe9FSjyt43qtYNyA8t2Dt
2YBiAl6z0TZC4NIRE1DfXL00loEZ+0jkwcs32AmLwRhY2IRYVG/TVm9QTrLVrqKl
5mFPjGteyHFk5885ViGgxI5VKWxctlObuMp9HbiMlKZmMi89+GNmPRVq+sLV1g/L
KA2a9UNc5Grov4kVRdhCQBiL/Y/hSHeRQIGG3qve+TzgmW2XI7IthyPx1fSWwQpC
X8vDQ8BHmeM80Y1/WOi5NfLLsVHoLXi2z8TYeISLVXWE02OjpeezT1rQRb5vHdy8
5OYz4g5E5vwNZbVlwCwnxdVZ2kRh0jJ9OrsDei3v0Zeb0eCETfGrAvePpRHHl0kP
NZNzB8+DKbH4WZ3PQ2bHCx3BMw4LSB9sihcGUe9se+Lob+SnKeMNUYFlry4bQg==
-----END CERTIFICATE-----
"""

server_ip_port = "54.166.14.117:4443"
hidden_perf_directory = "/tmp/6106-student-jobs"

poll_interval = 0.25 # seconds

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
            with open(file, 'rb') as f:
                file_content = f.read()
                # write this to a hidden directory
                assert job_id is not None and script_args is not None
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
