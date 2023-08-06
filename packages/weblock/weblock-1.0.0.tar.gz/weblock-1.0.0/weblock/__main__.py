import argparse
import os
from .encoder import encode_data, decode_data
from .wrapper import wrap_encoded_data

# Handle CLI args
ap = argparse.ArgumentParser("weblock")
ap.add_argument("input", help="Input HTML file")
ap.add_argument("key", help="Encryption key")
args = ap.parse_args()

# Sanity check inputs
if not os.path.exists(args.input):
    print("Input file does not exist")
    exit(1)
if len(args.key) == 0:
    print("Key must not be empty")
    exit(1)

# Load the input file
file = open(args.input, "r").read()

# Encode the file
encoded = encode_data(file, args.key)

# Wrap the file
wrapped = wrap_encoded_data(encoded)

print(wrapped)