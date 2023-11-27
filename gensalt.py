import bcrypt


for i in range(3):
    print(bcrypt.gensalt(12).decode())
