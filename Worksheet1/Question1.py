file = open("users.txt", "r")

def login(inusername, inpassword):
    for line in file:
        if line.split(' ')[0] == inusername:
            if line.split(' ')[1] == inpassword:
                return True
            else:
                print("Incorrect Password")
                return False
        else:
            print("Incorrect Username")
            return False

username = raw_input()
password = raw_input()

print(login(username, password))

file.close()
