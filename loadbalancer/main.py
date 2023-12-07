
import sys
from src.server import run

if len(sys.argv) < 2:
    print("Need to specify port to run in!")
    exit(1)

port = int(sys.argv[1])

run(port)

print(f"Running in port {port}")


