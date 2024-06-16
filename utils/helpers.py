def print_headers(parsed_headers: dict):
    print("Request Method:", parsed_headers["method"])
    print("Request Path:", parsed_headers["path"])
    print("HTTP Version:", parsed_headers["version"])
    print("Headers:")
    for key, value in parsed_headers["headers"].items():
        print(f"{key}: {value}")

