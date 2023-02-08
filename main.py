import multiprocessing
import sys
import getopt
import crypt
import time
from threading import Thread, Lock

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

#Contains cracked passwords
output = {}

#Set as command line argument
tries_limit = 0

# Thread safe integer accessed by all threads to track attempt count
attempts = 0
attempts_lock = Lock()
# --------------------------------------------------------------

# If true, threads are closed
check = False
# --------------------------------------------------------------

def main(shadow, users, threads):
    # Reads file and sends passwords to cracker method
    try:
        shadow_file = open(shadow, 'r')
    except:
        sys.exit("Could not open shadow file")

    lines = shadow_file.readlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        user = line.split(":")[0]
        if users and user not in users:
            continue
        if (line.split(":")[1] == "!!" or line.split(":")[1] == "*" or line.split(":")[1] == "" or line.split(":")[
            1] == "!*" or line.split(":")[1] == "!"):
            continue
        helper(line.split(":")[1],user,line.split(":")[1].split("$")[1],threads)

    print_()


def helper(target,user,hash,threads):
    # Create threads and distributes work
    global check
    length = 1
    while True:
        start = time.time()
        var = []
        if check:
            check = False
            break
        for i in range(threads):
            daemon = Thread(target=brute_force, name='Monitor',args=(length, target,user,hash,start))
            length += 1
            var.append(daemon)
        for x in var:
            x.start()
        for j in var:
            j.join()


def close_threads():
    # When check is true, threads close
    global check
    with attempts_lock:
        check = True

def brute_force(i, target,user,hash,start):
    # Configures brute force attack settings
    global attempts
    str_len = i
    while True:
        var = generate_words(str_len, "",target)
        if var and var == "MAX_":
            close_threads()
            set_output(user,"N/A","Tries limit reached",tries_limit,time.time()-start)

        elif var:
            close_threads()
            set_output(user,hashes[hash],var,attempts,time.time()-start)
            attempts = 0
        break


def generate_words(str_len, string,target):
    #Cracks passwords
    global attempts
    global check
    if str_len == 0 and crypt.crypt(string,target) == target:
        with attempts_lock:
            attempts +=1
        return string
    if str_len == 0:
        with attempts_lock:
            attempts +=1
        return False

    for i in range(len(AlphabetLower)):
        temp = string + AlphabetLower[i]
        res = generate_words(str_len-1, temp,target)
        #Return cracked password
        if res: return res

        #Other thread has cracked password
        if check: sys.exit()

        #Attempt limit reached
        if attempts == tries_limit:
            return "MAX_"


def set_output(user,hash,password,tries,time_):
    # Sets output
    output[user] = {}
    output[user]['hash'] = hash
    output[user]['password'] = password
    output[user]['tries'] = tries
    if time_ == "N/A":
        output[user]['time'] = "N/A"
        return
    output[user]['time'] = str(round(time_,5)) + " seconds"



def print_():
    # Displays program results when done
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

def set_min_thread():
    # Sets minimum thread count to cores on system
    return multiprocessing.cpu_count()

def validate_args(argv):
    global tries_limit
    users = []
    shadow = ""
    threads = False

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
            try:
                threads = int(value)
            except ValueError:
                threads = set_min_thread()
        elif arg in ['-a', '--attempts']:
            try:
                tries_limit = int(value)
            except ValueError:
                sys.exit("Error: main.py -f <Shadow File> -t <# threads> -a <# attempts> username(s)")

    if not threads:
        users = argv[4:]
    if threads <= 0 or not threads:
        print("Threads not specified, setting as # of cores")
        threads = set_min_thread()
        print(f"Thread count set as {threads}")


    if len(argv) > 6 and not users:
        users = argv[6:]

    if (shadow and tries_limit and threads):
        if not users:
            print("\nNo user specified, cracking all passwords!\n")
        return shadow, users, threads
    else:
        sys.exit("Error: main.py -f <Shadow File> -t <# threads> -a <# attempts> username(s)")

if __name__ == '__main__':
    shadow, users, threads = validate_args(sys.argv[1:])
    main(shadow, users, threads)
