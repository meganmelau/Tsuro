import os
import subprocess
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import sys
import json
import time

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Allowed strategies
strategies = ["dumb", "less_dumb"]

# Variables for key values
strat = "strategy"
name = "name"
ip = "127.0.0.1"
port = 8000


if __name__ == "__main__":
    # Starts Tsuro Server
    p = subprocess.Popen(args=".\\xserver", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    input_content = sys.stdin.readline()
    json_array = json.loads(input_content)

    if len(json_array) > 5 or len(json_array) < 3:
        raise Exception("Must have 3 to 5 players.")

    # Creats the client and start up per player
    client_processes = []
    for player_specification in json_array:
        client = subprocess.Popen(args=(".\\xclient {} {} {} {}".format(ip, str(port), player_specification[name],
                                                                        player_specification[strat].lower())),
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
        client_processes.append(client)
        time.sleep(1)
    out, err = p.communicate()
    print(out.decode("utf-8"))
