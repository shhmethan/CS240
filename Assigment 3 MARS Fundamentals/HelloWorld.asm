.data
message: .asciiz "Hello World\n"

.text
.globl main
main:
    li $v0, 4          # Syscall 4: print string
    la $a0, message    # Address of the string
    syscall

    li $v0, 10         # Syscall 10: exit
    syscall
