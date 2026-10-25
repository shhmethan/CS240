.data
data_0: .asciiz "\n"
data_1: .asciiz "Fizz\n"
data_2: .asciiz "Buzz\n"
data_3: .asciiz "FizzBuzz\n"

.text
.globl main

main:
    addiu $t0, $zero, 1

label_00400004:
    addiu $at, $zero, 100
    slt $at, $at, $t0
    bne $at, $zero, label_004000AC
    addiu $at, $zero, 15
    div $t0, $at
    mfhi $t2
    beq $t2, $zero, label_00400094
    addiu $at, $zero, 3
    div $t0, $at
    mfhi $t2
    beq $t2, $zero, label_00400064
    addiu $at, $zero, 5
    div $t0, $at
    mfhi $t2
    beq $t2, $zero, label_0040007C
    addiu $v0, $zero, 1
    addu $a0, $t0, $zero
    syscall
    addiu $v0, $zero, 4
    la $a0, data_0
    syscall
    addi $t0, $t0, 1
    j label_00400004

label_00400064:
    addiu $v0, $zero, 4
    la $a0, data_1
    syscall
    addi $t0, $t0, 1
    j label_00400004

label_0040007C:
    addiu $v0, $zero, 4
    la $a0, data_2
    syscall
    addi $t0, $t0, 1
    j label_00400004

label_00400094:
    addiu $v0, $zero, 4
    la $a0, data_3
    syscall
    addi $t0, $t0, 1
    j label_00400004

label_004000AC:
    addiu $v0, $zero, 10
    syscall
