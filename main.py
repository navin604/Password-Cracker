import sys
import getopt
import crypt

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
        if password == crypt.crypt(line, password):
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
    #main(dictionary,shadow, users)




