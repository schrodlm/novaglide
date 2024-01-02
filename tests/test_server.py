import json
def main():
    #TODO: put the test calls here
    js = {'sender': 'SERVER', 'status': 'READY'}
    encoded = json.dumps(js).encode()
    print(json.loads(encoded))
if __name__ == "__main__":
    main()
