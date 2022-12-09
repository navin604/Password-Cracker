import crypt
import sys
import getopt
from hmac import compare_digest as compare_hash

def main(dictionary,shadow):
    results = {}
    try:
        shadow_file = open(shadow,'r')
    except:
        sys.exit("Could not open shadow file")

    lines = shadow_file.readlines()
    for line in lines:
        line = line.strip()
        user = line.split(":")[0]
        if (line.split(":")[1] == "!!" or line.split(":")[1] == "*" or line.split(":")[1] == ""or line.split(":")[1] == "!*" ):
            print(f"No password listed for {user}\n")
        else:
            print(f"Cracking password for {user}:")
            result = crack_pass(line.split(":")[1],dictionary)
            if (result):
                results[user] = result
    if (len(results) !=0):
        print_(results)


def crack_pass(password,file):
    try:
        dictionary = open(file, 'r')
    except IOError:
        sys.exit("Could not open file: ", file)

    lines = dictionary.readlines()
    for line in lines:
        line = line.strip()
        if (compare_hash(password, crypt.crypt(line, password))):
            print(f"Password cracked successfully:  {line}\n")
            return line
    print("Failed to crack password")
    return False

def print_(results):
    i = 1
    print(f"\nThe following passwords have been cracked!")
    print(f"\n------------------------------------------\n")
    for user, password in results.items():
        print(f"{i}. Username: {user}, Password: {password}\n")
        i+=1

def validate_args(argv):
    dictionary = ""
    shadow = ""
    try:
        opts, args = getopt.getopt(argv, "d:s:")
    except getopt.GetoptError:
        print('main.py -d <Dictionary File> -s <Shadow File>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -d <Dictionary File> -s <Shadow File>')
            sys.exit()
        elif opt in ("-d"):
            dictionary = arg
        elif opt in ("-s"):
            shadow = arg
    if (shadow and dictionary):
        return dictionary, shadow
    else:
        sys.exit("Error: main.py -d <Dictionary File> -s <Shadow File>'")

if __name__ == '__main__':
    dictionary, shadow = validate_args(sys.argv[1:])
    main(dictionary,shadow)



