from django.test import TestCase
# TESTS
'''def testAuthLevel():
    print('-------- AuthLevel -------\n')
    user = 'example.user'
    AuthLevelKey = generateAuthKey(user, 0)
    print(f'({user})seed --> {AUTHLEVELKEYS["USER_LEVEL_KEY"]}\nAuthKey --> {AuthLevelKey}\n')
    res, AuthLevel = validarAuthKey(user, AuthLevelKey)
    print(f'validation {res}\nvalidationLevel {AuthLevel}')

    print('---------- END ----------')

def testJWT():
    print('-------- TEST JWT --------\n')
    user = 'example.user'
    ssid = createSSID(user)
    print(f'({user})seed --> {SALT_KEY}\nSSID --> {ssid}\n')

    res = validarSSID(ssid)
    print(f'payload {res}\n')
    print('---------- END ----------')
def generalTest(user):
    print('-------- GENERAL TEST --------\n')

    # USER VIEW
    ssid = createSSID(user)
    print(f'user: {user}\nGEN ssid: {ssid}')

    # SERVER VIEW
    validation, authLevel = validarSSID(ssid)
    print(f'validation: {validation}\nAuthLevel: {authLevel}')
    print('---------- END ----------')

os.system('cls')
user = 'user.ejemplo'
generalTest(user)
'''