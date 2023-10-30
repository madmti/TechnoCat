import bcrypt
import os
from dotenv import load_dotenv
load_dotenv()
# SECRET KEYS
SALT_KEY = os.getenv('SALT_KEY').encode()
AUTHLEVELKEYS = {
    'USER_LEVEL_KEY': os.getenv('USER_LEVEL_KEY').encode(),
    'SUPER_LEVEL_KEY': os.getenv('SUPER_LEVEL_KEY').encode(),
}

def generateAuthKey(user:str, authlevel:int) -> bytes:
    key = 'USER_LEVEL_KEY' if authlevel == 0 else 'SUPER_LEVEL_KEY'
    forHash = (bcrypt.gensalt(12).decode()+user).encode()
    auhtKey = bcrypt.hashpw(AUTHLEVELKEYS[key], forHash)
    return auhtKey

def validarAuthKey(AuthKey:bytes) -> list:
    isValidUser = bcrypt.checkpw(AUTHLEVELKEYS['USER_LEVEL_KEY'], AuthKey)
    isValidAdmin = bcrypt.checkpw(AUTHLEVELKEYS['SUPER_LEVEL_KEY'], AuthKey)
    isValid = isValidAdmin or isValidUser
    return [isValid, int(isValidAdmin)]

# proxima actualizacion

user = 'example.usera'
key = generateAuthKey(user, 1)
validacion = validarAuthKey(key)
print(key)
print(validacion)