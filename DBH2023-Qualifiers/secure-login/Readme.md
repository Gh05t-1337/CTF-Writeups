# secure-login
## Challenge
We get the code of a webpage. we have to login as admin to gain the flag from the webpage-ip/flag directory

## Solution
Using the same nonce (IV, initialization vector) twice in AES-GCM is a bad idea. See: https://crypto.stackexchange.com/questions/26790/how-bad-it-is-using-the-same-iv-twice-with-aes-gcm

By inspecting `app.py` we see, that AES-GCM is used, to generate a token that is then saved into a cookie. this token is also used in `get_user`, to get the users name and output the users flag on /flag. So we need to generate a cookie that makes `get_user` return `admin`.

Let's take a look at `gen_token`:
```python
def gen_token(user):
    cipher = AES.new(key=KEY, mode=AES.MODE_GCM)
    ciphertext = cipher.encrypt(user.username.encode())
    return base64.b64encode(cipher.nonce + ciphertext).decode()
```
It encodes the username using AES-GCM and saves it to ciphertext. It then returns the base64 of nonce+ciphertext. This output will be saved as cookie.

Let's now take a look at `get_user`:
```python
def get_user():
    if 'user' not in request.cookies:
        return None
    ciphertext = base64.b64decode(request.cookies['user'].encode())
    cipher = AES.new(key=KEY, mode=AES.MODE_GCM, nonce=ciphertext[:16])
    user = cipher.decrypt(ciphertext[16:])
    return users[user.decode()]
```
It decodes the base64 encoded cookie and saves it in ciphertext. In the first 16 bytes of ciphertext, the nonce is stored. In the last few bytes, the AES encoded username is stored. It decodes the username using the nonce, and saves it in `user`. Then it returns the corresponding user.

The vulnerability here is that if we know the nonce and AES encoded username for a user called "admin+", we also know how the AES encoded username of "admin" looks when using the same nonce: if the AES encoded username of "admin+" is: 42 a3 50 fe c3 01, the AES encoded username of "admin" with the same nonce will be: 42 a3 50 fe c3.

So, to get the flag we just:
- create a user called 'admin+'
- convert cookie from base64 to hex
- delete last byte of hex
- convert back to base64
- use as new cookie
- look at the /flag page

we then get the flag: DBH{7h3_b357_crypt0_d035n7_h31p_1f_y0u_4r3_u51ng_17_wr0ng} 
