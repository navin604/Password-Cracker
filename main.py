import sys
import getopt
import crypt
import time

AlphabetLower = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g',
    'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't', 'u',
    'v', 'w', 'x', 'y', 'z','A','B','C',
    'D','E','F','G','H','I','J','K','L',
    'M','N','O','P','Q','R','S','T','U',
    'V','W','X','Y','Z','0','1','2','3','4',
    '5','6','7','8','9'
]

hashes = {"1":"MD5","2a":"Blowfish - 2a","2y":"Eksblowfish - 2y","5":"SHA-256", "6": "SHA-512","y": "yescrypt","2b":"bcrypt version 2b" }

output = {}
helper = 0
tries_limit = 0

def main(shadow, users):

    try:
        shadow_file = open(shadow, 'r')
    except:
        sys.exit("Could not open shadow file")

    lines = shadow_file.readlines()
    for line in lines:
        line = line.strip()
        if not line:
            print("Empty line in shadow file! Check and see if you are using the wrong file!\n")
            continue
        user = line.split(":")[0]
        if users and user not in users:
            continue
        if (line.split(":")[1] == "!!" or line.split(":")[1] == "*" or line.split(":")[1] == "" or line.split(":")[
            1] == "!*" or line.split(":")[1] == "!"):
            continue

        brute_force(line.split(":")[1],user,line.split(":")[1].split("$")[1])
    print_()

def set_output(user,hash,password,tries,time_):
    output[user] = {}
    output[user]['hash'] = hash
    output[user]['password'] = password
    output[user]['tries'] = tries
    if time_ == "N/A":
        output[user]['time'] = "N/A"
        return
    output[user]['time'] = str(round(time_,5)) + " seconds"


def generate_words(str_len, string,target):
    global helper
    if str_len == 0 and crypt.crypt(string,target) == target:
        return string
    if str_len == 0:
        return False

    for i in range(len(AlphabetLower)):
        helper +=1
        temp = string + AlphabetLower[i]
        res = generate_words(str_len-1, temp,target)
        if res: return res
        if helper == tries_limit:
            return "MAX_"

def brute_force(target,user,hash):
    global helper
    str_len = 1
    start = time.time()
    while True:
        var = generate_words(str_len, "",target)
        if var and var == "MAX_":
            set_output(user,"N/A","Tries limit reached",helper,time.time()-start)
            break
        elif var:
            set_output(user,hashes[hash],var,helper,time.time()-start)
            break
        str_len +=1
    helper = 0



def print_():
    print(f"\nResults of the password cracking process!")
    print(f"------------------------------------------\n")
    if len(output) == 0:
        print("No users cracked!\n")
        return
    for i in output:
        print(f"Username: {i}\n")
        print(f"Hash: { output[i]['hash']}\n" )
        print(f"Password: {output[i]['password']}\n")
        print(f"Tries: {output[i]['tries']}\n")
        print(f"Time: {output[i]['time']}\n")
        print(f"------------------------------------------\n")

def validate_args(argv):
    global tries_limit
    users = []
    shadow = ""

    try:
        options, args = getopt.getopt(argv, "f:t:a:",
                                      ["file =",
                                       "threads =",
                                       "attempts ="])
    except Exception as e:
        print("Error: main.py -f <Shadow File> -t <# threads> -a <# attempts> username(s)")
        sys.exit(f"{e}")

    for arg, value in options:
        if arg in ['-f', '--file']:
            shadow = value
        elif arg in ['-t', '--threads']:
            threads = int(value)
        elif arg in ['-a', '--attempts']:
            tries_limit = int(value)

    if len(argv) > 6:
        users = argv[6:]

    if (shadow and tries_limit and threads):
        if not users:
            print("\nNo user specified, cracking all passwords!\n")
        return shadow, users, threads
    else:
        sys.exit("Error: main.py -f <Shadow File> -t <# threads> -a <# attempts> username(s)")

if __name__ == '__main__':
    shadow, users, threads = validate_args(sys.argv[1:])
    #main(shadow, users)