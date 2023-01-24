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

hashes = {"1":"MD5","2a":"Blowfish","2y":"Eksblowfish","5":"SHA-256", "6": "SHA-512","y": "yescrypt","2b":"bcrypt version 2b" }

output = {}
helper = 0
tries_limit = 0

def main(dictionary, shadow, users):

    try:
        shadow_file = open(shadow, 'r')
    except:
        sys.exit("Could not open shadow file")

    lines = shadow_file.readlines()
    for line in lines:
        line = line.strip()
        user = line.split(":")[0]
        if users and user not in users:
            continue
        if (line.split(":")[1] == "!!" or line.split(":")[1] == "*" or line.split(":")[1] == "" or line.split(":")[
            1] == "!*"):
            continue

        check = dict_crack(line.split(":")[1], user, dictionary, line.split(":")[1].split("$")[1])
        if not check:
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


def dict_crack(password, user, file, hash):
    tries = 1
    start = time.time()
    try:
        dictionary = open(file, 'r')
    except:
        sys.exit(f"Could not open file: {file}")

    lines = dictionary.readlines()
    if not lines: return False
    for line in lines:
        line = line.strip()
        if password == crypt.crypt(line, password):
            print(f"Password cracked successfully ->  User:{user} Pass:{line}\n")
            set_output(user,hashes[hash],line,tries,time.time()-start)
            return True
        tries += 1


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
            helper = 0
            return
        elif var:
            break
        str_len +=1
    set_output(user,hashes[hash],var,helper,time.time()-start)
    helper = 0



def print_():
    num = 1
    print(f"\nResults of the password cracking process!")
    print(f"\n------------------------------------------\n")
    for i in output:
        print(f"{num}. Username: {i}, Hash: { output[i]['hash']}, Password: {output[i]['password']}, Tries: {output[i]['tries']}, Time: {output[i]['time']}\n")
        num += 1



def validate_args(argv):
    global tries_limit
    users = []
    shadow = word_list = ""

    try:
        options, args = getopt.getopt(argv, "f:t:w:",
                                      ["file =",
                                       "tries =",
                                       "words ="])
    except Exception as e:
        print("Error: main.py -f <Shadow File> -t <tries> -w <Dictionary File> username(s)")
        sys.exit(f"{e}")

    for arg, value in options:
        if arg in ['-f', '--file']:
            shadow = value
        elif arg in ['-w', '--words']:
            word_list = value
        elif arg in ['-t', '--tries']:
            tries_limit = int(value)

    if len(argv) > 6:
        users = argv[4:]

    if (shadow and word_list and tries_limit):
        if not users:
            print("No user specified, cracking all passwords!")
        return word_list, shadow, users
    else:
        sys.exit("Error: main.py -f <Shadow File> -t <tries> -w <Dictionary File> username(s)")


if __name__ == '__main__':
    word_list, shadow, users = validate_args(sys.argv[1:])
    main(word_list, shadow, users)
