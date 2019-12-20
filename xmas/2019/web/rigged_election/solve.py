import hashlib
import requests
import math
import random

jar = requests.cookies.RequestsCookieJar()

hashes = {}

# Go to home page and get first session
r = requests.get("http://challs.xmas.htsp.ro:11001/", cookies=jar)

jar = r.cookies

print(jar.get_dict())

def generateRandom(length):
    results = ''
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    charsLength = len(chars)

    for x in range(length):
        ran = math.floor(random.random() * charsLength)
        results += chars[ran]

    return results

def vote():
    global hashes
    global jar

    id = 19534
    upvote = "%60~%21%40%23%24%25%5E%26%2A%28%29_%2B-%3D%7B%7D%7C%5B%5D%5C%3A%22%3B%27%3C%3E%3F%2C.%2F"

    r = requests.get("http://challs.xmas.htsp.ro:11001/vote?g=9001", cookies=jar)
    work = r.text

    # Check if work is inside of hashes already
    if work in hashes:
        sendVote(hashes[work])
        return

    while True:
        randomLength = math.floor(7 + random.random() * 18)
        stringGen = generateRandom(randomLength)
        md5Gen = hashlib.md5(("watch__bisqwit__" + stringGen).encode("utf-8")).hexdigest()
    
        # if gen is alread inside of hashes then continue
        if md5Gen[0:len(work)] in hashes:
            continue
        else:
            hashes[md5Gen[0:len(work)]] = stringGen

        if md5Gen[0:len(work)] == work:
            sendVote(stringGen)
            return

def sendVote(stringGen):
    global jar

    r = requests.get("http://challs.xmas.htsp.ro:11001/vote.php?id="+str()+"&h="+stringGen+"&u=1", cookies=jar)

    print(r.text)

for x in range(300):
    vote()


