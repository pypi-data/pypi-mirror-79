# WebLock
WebLock is a simple tool for hiding an HTML file behind a password on a static server

## How it works

WebLock uses a very simple sequential system:

 1. User writes an HTML file they want to protect
 2. User runs weblock against that file with a secret key, and saves the output
 3. User opens the outputted HTML file, and enters the secret key when asked
 4. The outputted HTML file uses some simple JavaScript code to overwrite itself in the browser with the decrypted file contents

## Installation

To install, simply clone this repo, then run

```sh
python3 setup.py install
weblock
```