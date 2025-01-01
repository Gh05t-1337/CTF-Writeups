# T2: Yin and Yang

https://tryhackme.com/r/room/adventofcyber24sidequest

## SSH into Yin and Yang
We start by doing an nmap scan. a quick scan shows no open ports, so we have to scan all ports:
```bash
nmap -T4 -p- [IP-ADDRESS] -vv
```
after waiting a bit, this shows port 21337 on both machines. It's a website were we input the keycard code to unlock port 22 (ssh). We can now connect to both machines using the credentials given on tryhackme.

## Connecting Yin and Yang
We now need to get Yin and Yang to communicate using the [language of turtle robots](https://www.ros.org/). Here's a useful tutorial on that: [https://wiki.ros.org/ROS/Tutorials/MultipleMachines](https://wiki.ros.org/ROS/Tutorials/MultipleMachines). But before doing any of that, let's see if there's anything we can run with sudo:
```bash
sudo -l
```
On Yin we can run `/catkin_ws/yin.sh` as root, on Yang we can run `/catkin_ws/yang.sh` as root. If a ROS Master is running roscore, those two scripts start to communicate (not to each other as of now, but we'll change that). There's also a `start-yin.sh` and `start-yang.sh` on yin and yang respectively to start roscore.

For Yin and Yang to talk to each other, we need to run roscore on one of them (using the `start-[yin/yang].sh` script), and let both scripts talk over that ROS Master. If we run the start-yin.sh script, and then start the yin and yang scripts with sudo, only the yin.sh script works, as the the root user on yang has ROS\_MASTER\_URI set to localhost. Since we aren't root yet, we can't change that. But what we _can_ change, is the address localhost is pointing to in /etc/hosts as `/etc/hosts` has some weird privileges. So, we just need to change `/etc/hosts` so yang's localhost points to yin. After doing so, yang.sh works. We should now have a `yin.txt` file in yang's home directory, and `yang.txt` on yin.

<p align="center">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="images/yin-yang-darkmode.svg">
      <source media="(prefers-color-scheme: light)" srcset="images/yin-yang.svg">
      <img alt="Shows a black logo in light color mode and a white one in dark color mode." src="https://user-images.githubusercontent.com/25423296/163456779-a8556205-d0a5-45e2-ac17-42d089e3c3f8.png">
    </picture>
</p>

## So, they're communicating... Now what?
`yin.txt` and `yang.txt` are empty, so we still don't have any flags. But one thing we get is a private RSA key: we can do `rostopic echo /messagebus` on yin and it outputs yang's messages. a part of each message is an RSA key. It's time to look at what `yin.sh` and `yang.sh` are actually doing. if we run `ps aux|grep yin` on yin, we see a python script called `/catkin_ws/src/yin/scripts/runyin.py` running (same to yang, just different name). This is what's doing the communication. 

After taking a look at both scripts and understanding them, we can create the script `fake-runyin.py` using the RSA private key we found earlier, and some random string as `self.secret`, so we don't need sudo. At the start of `fake-runyin.py`'s handle\_yang\_request, we do `print(req.secret)` to get the content of secret.txt and just run `fake-runyin.py` instead of the real `runyin.py` on Yin.

```bash
python3 fake-runyin.py
```

Now that we have the RSA key as well as the secret, we can fully fake runyin.py and runyang.py. So, we just run `sudo /catkin_ws/yin.sh` on yin, while running a fake runyang.py on yang. Instead of `touch /home/yin/yang.txt`, we let our fake runyang.py run `/bin/bash` so we get a shell on yin. In `/root` we find our first flag. for yang's flag we just need to do the same in reverse.
