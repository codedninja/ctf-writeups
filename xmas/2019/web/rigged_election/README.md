# Rigged Election
## Challenge
>Come one, come all! We've opened up a brand new website that allows the Lapland people to vote the next big town hall project! Just upload your ideas on the platform and vote using your CPU power. We've made sure voting takes a great amount of effort, so there's no easy way to play the system.
>
>If you are indeed able to vote more than 250 times, you will be congratulated as an active Lapland citizen and receive a prize worthy of this title.

## Vulnerability
The vulnerability was it checks only the first 6 characters of the hash. The issue though is to generate new hashes for every new challenge hash takes too long. Instead you cache the first 6 characters of the hash with the string that generated the hash. Then when you get a new challenge hash look up the hash if it was generated already to save time.

## Solution

[solve.py](solve.py)
