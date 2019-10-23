#!/usr/bin/python
# 
# Patlabor 
# 
# Version:
#       1.0
# Author:
#       bigb0ss
# 
# Description:
#       This helps to find main_arena offset value for both 32-bit and 64-bit libc.so.6
#

class color:
    yellow = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    red = '\033[91m'
    end  = '\033[0m'
    
import subprocess
import sys
import re

def help():
    print(" ")
    print("              _   _       _                ")
    print("  _ __   __ _| |_| | __ _| |__   ___  _ __ ")
    print(" | '_ \ / _` | __| |/ _` | '_ \ / _ \| '__|")
    print(" | |_) | (_| | |_| | (_| | |_) | (_) | |   ")
    print(" | .__/ \__,_|\__|_|\__,_|_.__/ \___/|_|   ")
    print(" |_|                             bigb0ss   ")
    print(" ")
    print(color.yellow + "[*] Usage: python " + sys.argv[0] + color.red + ' "libc.so.6"' + color.yellow + 'of your choice' + color.end)
    
if len(sys.argv) < 2 or len(sys.argv) > 2:
    help()
    sys.exit(1)
else:
    file = sys.argv[1]

def version(file):
    output = subprocess.check_output(["strings", file])
    for line in output.splitlines():  
        if re.search("glibc 2", line): 
            print(color.blue + "[+] Libc Version     : " + color.end + line)

def build_id(file):
    output = subprocess.check_output(["file", file])
    for line in output.split(', '):  
        if re.search("BuildID", line):  
            print(color.blue + "[+] BuildID          : " + color.end + line)

def arch(file):
    output = subprocess.check_output(["file", file])
    for line in output.split(' '):
        if re.search("bit", line):
            print(color.blue + "[+] Arch             : " + color.end + color.red + line + color.end)

def malloc_hook(file):
    output = subprocess.check_output(["objdump", "-j", ".data", "-d", file])
    for line in output.splitlines():  
        if re.search("__malloc_hook", line):    
            line = line.split(" ")
            line = line[0]
            line = int(line, 16)
            line = str(line)
            return(line)    
malloc_hook(sys.argv[1])
malloc_hook_output = malloc_hook(sys.argv[1])
malloc_hex = int(malloc_hook_output)

#
# 32-bit: main_arena_offset = __malloc_hook + 0x18
# 64-bit: main_arena_offset = __malloc_hook + (__mallock_hook - __realloc_hook) * 2
#
def main_arena_offset(file):
    output = subprocess.check_output(["file", file])
    # 32-bit
    if re.search("32-bit", output): 
        a = int(malloc_hook_output) 
        b = int(0x18)   
        main_arena = a + b
        print(color.green + "[+] main_arena_offset: " + color.end + hex(main_arena))
    # 64-bit
    elif re.search("64-bit", output):
        output = subprocess.check_output(["objdump", "-j", ".data", "-d", file])
        for line in output.splitlines():
            if re.search("__realloc_hook", line):
                line = line.split(" ")
                line = line[0]
                line = int(line, 16)    
                realloc_hook_output = str(line)
                realloc_print = int(line)
                print(color.blue + "[+] realloc_hook     : " + color.end + hex(realloc_print))
                a = int(malloc_hook_output) 
                b = int(realloc_hook_output)
                offset = a - b
                c = int(offset)
                main_arena = a + c * 2
                print(color.green + "[+] main_arena_offset: " + color.end + hex(main_arena))
    else:
        print("[-] Libc fucked -_-")

def main():
    help()
    arch(sys.argv[1])
    build_id(sys.argv[1])
    malloc_hook(sys.argv[1])
    main_arena_offset(sys.argv[1])

if __name__ == "__main__":
    main()

