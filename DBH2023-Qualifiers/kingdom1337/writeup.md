# kingdomof1337
using a pyc decompiler like pycdc, one can get most of the python code of vuln.py. using a debugger like trepan-xpy, one can understand it further. the important functions are 'run\_message' and 'King.modt'. If king doesn't have the attribute 'shout', it will just output 'I have no messages today.'. So, the first goal is, to use build some json code, that makes use of 'run\_message' to add the attribute 'shout' to king. this can be accomplished using following json:
`{"__class__":{"__base__":{"__base__":{"__base__":{"shout":"our_message"}}}}}`
use trepan-xpy to understand why and how this works.
next, we take a look on how the king shouts our message. it uses:
`popen("echo " + say).read().strip()`
So, it just runs the bash command 'echo our_message'. We can easily inject some code there, for example by using:
`{"__class__":{"__base__":{"__base__":{"__base__":{"shout":"&&ls"}}}}}`
to get the files in the current directory. using:
`{"__class__":{"__base__":{"__base__":{"__base__":{"shout":"&&ls ..\"}}}}}`
we see where the flag is, and print it using:
`{"__class__":{"__base__":{"__base__":{"__base__":{"shout":"&&cat ..\flag.txt"}}}}}`
