import sys
import getopt
import crypt
import time

output = {}
hashes = {"1":"MD5","2a":"Blowfish","2y":"Eksblowfish","5":"SHA-256", "6": "SHA-512","y": "yescrypt" }

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

        elif (line.split(":")[1] == "!!" or line.split(":")[1] == "*" or line.split(":")[1] == "" or line.split(":")[
            1] == "!*"):
            set_output(user,"N/A","N/A","N/A","N/A")

        else:
            print(f"Cracking password for {user}:")
            crack_pass(line.split(":")[1], user, dictionary, line.split(":")[1].split("$")[1])
    print_()

def set_output(user,hash,password,tries,time_):
    print("!")
    output[user] = {}
    output[user]['hash'] = hash
    output[user]['password'] = password
    output[user]['tries'] = tries
    print("2")
    output[user]['time'] = str(time_) + " seconds"
    print("!3")

def crack_pass(password, user, file, hash):
    tries = 1
    start = time.time()
    try:
        dictionary = open(file, 'r')
    except IOError:
        sys.exit("Could not open file: ", file)

    lines = dictionary.readlines()
    for line in lines:
        print(tries)
        line = line.strip()
        if password == crypt.crypt(line, password):
            print(f"Password cracked successfully:  {line}\n")
            set_output(user,hashes[hash],line,tries,time.time()-start)
            return line
        tries += 1
    print("Failed to crack password")
    set_output(user,"N/A","Failed to crack",tries,time.time()-start)


def print_():
    cnt = 1
    print(f"\nResults of the password cracking process!")
    print(f"\n------------------------------------------\n")
    for i in output:
        print(f"{cnt}. Username: {i}, Hash: { output[i]['hash']}, Password: {output[i]['password']}, Tries: {output[i]['tries']}, Time: {output[i]['time']}\n")
        cnt += 1



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
