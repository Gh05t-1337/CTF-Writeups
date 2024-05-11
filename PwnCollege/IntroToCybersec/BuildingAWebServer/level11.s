.intel_syntax noprefix
.globl _start

.section .text

_start:
    # setting up socket

    mov rdi,2
    mov rsi,1
    mov rdx,0
    mov rax,41	# socket(AF_INET,SOCK_STREAM,IPPROTO_IP)
    syscall

    mov rdi,3
    lea rsi,[sockaddr]
    mov rdx,16
    mov rax,49	# bind
    syscall

    mov rdi,3
    mov rsi,0
    mov rax,50	# listen(3,0)
    syscall

loop:
    # parent's main loop

    mov rdi,3
    mov rsi,0
    mov rdx,0
    mov rax,43	# accept(3,0,0)
    syscall

    mov rax,57	# fork
    syscall

    mov r8,rax
    cmp r8,0
    je child

    mov rdi,4
    mov rax,3   # close
    syscall
    jmp loop

child:
    mov rdi,3
    mov rax,3	# close
    syscall

    mov rdi,4
    lea rsi,[buf]
    lea rdx,[bufsize]
    mov rax,0	# read request
    syscall

    push rax

    mov cl, [buf] # check if post or get
    cmp cl, 'P'
    je post

get:
    lea rdi,[buf+4]     # buf+4 is start of filename in GET request
    mov [buf+20],WORD PTR 0x0000        # put zeroes at end of file name in GET request
    mov rsi,0
    mov rax,2   # open requested file
    syscall

    mov rdi,3
    lea rsi,[buf]
    lea rdx,[bufsize]
    mov rax,0   # read opened file
    syscall

    push rax

    mov rdi,3
    mov rax,3   # close
    syscall

    mov rdi,4
    lea rsi,[msg]
    mov rdx,19
    mov rax,1   # write 200 OK
    syscall

    mov rdi,4
    lea rsi,[buf]
    pop rax
    mov rdx,rax
    mov rax,1   # write file content
    syscall

    mov rdi, 0
    mov rax, 60     # SYS_exit
    syscall

post:
    lea rdi,[buf+5]	    # buf+5 is start of filename in POST request
    mov [buf+21],WORD PTR 0x0000	# put zeroes at end of file name in GET request
    mov rsi,65
    mov rdx,511
    mov rax,2	# open correct file
    syscall

    mov rdi,3   # first arg
    mov r8,182  # suspected offset of data in POST request
    mov cl, [buf+181] 
    cmp cl, '\n'    # check if data starts indeed at offset 182
    je passt
      add r8,1  # if it doesn't start at 182, it starts at 183.
    passt:
    lea rsi,[buf+r8]    # second arg
    pop rax
    sub rax,r8
    mov rdx,rax     # third arg (length of message = total post request length (rax) - offset of data (r8))
    mov rax,1   # write data to file
    syscall

    push rax

    mov rdi,3
    mov rax,3   # close
    syscall

    mov rdi,4
    lea rsi,[msg]
    mov rdx,19
    mov rax,1   # write 200 OK
    syscall

    mov rdi, 0
    mov rax, 60     # SYS_exit
    syscall

.section .data
    bufsize: .word 1024
    msg: .ascii "HTTP/1.0 200 OK\r\n\r\n"
    sockaddr:
        .2byte 2	# AF_INET
        .2byte 0x5000	# Port 80
        .4byte 0	# IP 0.0.0.0
        .8byte 0	# padding

.section .bss
    buf: .space 1024
