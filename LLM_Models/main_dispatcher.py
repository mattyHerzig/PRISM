import json
import subprocess
import sys

with open("model_config.json", "r") as f:
    path = json.load(f)["script_path"]

diff_path = sys.argv[1]
pr_number = sys.argv[2]

subprocess.run(["python", path, diff_path, pr_number])
