import sys
import getopt
import crypt
import time

AlphabetLower = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g',
    'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't', 'u',
    'v', 'w', 'x', 'y', 'z'
]

hashes = {"1":"MD5","2a":"Blowfish","2y":"Eksblowfish","5":"SHA-256", "6": "SHA-512","y": "yescrypt" }

output = {}
helper = 0

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
            set_output(user,"N/A","N/A","N/A","N/A")

        print(f"Cracking password for {user}:")
        check = dict_crack(line.split(":")[1], user, dictionary, line.split(":")[1].split("$")[1])
        if not check:
            brute_force(line.split(":")[1],user,line.split(":")[1].split("$")[1])



    print_()




def set_output(user,hash,password,tries,time_):
    output[user] = {}
    output[user]['hash'] = hash
    output[user]['password'] = password
    output[user]['tries'] = tries
    output[user]['time'] = str(round(time_,5)) + " seconds"


def dict_crack(password, user, file, hash):
    tries = 1
    start = time.time()
    try:
        dictionary = open(file, 'r')
    except IOError:
        sys.exit("Could not open file: ", file)

    lines = dictionary.readlines()
    for line in lines:
        line = line.strip()
        if password == crypt.crypt(line, password):
            print(f"Password cracked successfully:  {line}\n")
            set_output(user,hashes[hash],line,tries,time.time()-start)
            return True
        tries += 1


def generate_words(str_len, string,target):
    global helper
    if(str_len == 0):
        return False
    if crypt.crypt(string,target) == target:
        return string
    for i in range(26):
        temp = string + AlphabetLower[i]
        helper +=1
        res= generate_words(str_len-1, temp,target)
        if res: return res



def brute_force(target,user,hash):
    global helper
    str_len = 1
    start = time.time()
    while True:
        var= generate_words(str_len, "",target)
        if var: break
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
    users = []
    shadow = word_list = ""

    try:
        options, args = getopt.getopt(argv, "f:w:",
                                      ["file =",
                                       "words ="])
    except:
        print("Error: main.py -f <Shadow File> -w <Dictionary File> username(s)")
        exit(1)

    for arg, value in options:
        if arg in ['-f', '--file']:
            shadow = value
        elif arg in ['-w', '--words']:
            word_list = value

    if len(argv) > 4:
        users = argv[4:]

    if (shadow and word_list):
        if not users:
            print("No user specified, cracking all passwords!")
        return word_list, shadow, users
    else:
        sys.exit("Error: main.py -f <Shadow File> -w <Dictionary File> username(s)")


if __name__ == '__main__':
    word_list, shadow, users = validate_args(sys.argv[1:])
    main(word_list, shadow, users)
