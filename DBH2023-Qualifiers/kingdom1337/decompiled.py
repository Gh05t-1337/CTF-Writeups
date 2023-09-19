# Source Generated with Decompyle++
# File: vuln.pyc (Python 3.10)

# Unsupported opcode: JUMP_IF_NOT_EXC_MATCH
from os import popen
import json

class Kingdom:
    pass


class Queen(Kingdom):
    pass


class Rook(Queen):
    pass


class Pawn(Rook):
    pass


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

DISALLOWED_INPUT = [
    '(',
    ')',
    '\\']
pawn = Pawn()
king = King()
print('Welcome to the kingdom of 1337, today\'s message: "h4ck 7h3 p14n37!"')
print('I, the pawn, will take your message to the king.')
print('Our hierarchy is strict, the message will only reach him, if the correct hierarchy is followed.')
USER_INPUT = input('Your Message: ')
print('')
if any((lambda y: [ x in USER_INPUT for x in y ])(DISALLOWED_INPUT)):
    print('Disallowed characters found in input')
    exit(1)

try:
    json_input = json.loads(USER_INPUT)
except json.decoder.JSONDecodeError:
    print('Your message needs to follow the offical format called "JSON".')
    exit(1)

run_message(json_input,pawn)
print(king.motd())
# WARNING: Decompyle incomplete

