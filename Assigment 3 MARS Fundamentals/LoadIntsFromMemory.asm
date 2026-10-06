# [Setup]
li $t0, 5
li $t1, 6

li $t3, 268500992
li $t4, 268501024

sw $t0, 0($t3)
sw $t1, 0($t4)

# [Clear]
li $t0, 0
li $t1, 0
li $t3, 0
li $t4, 0

# 0. Load the two immediate memory addresses into registers
li $t3, 268500992
li $t4, 268501024
li $t5, 268501056

# 1. Load values from memory into registers
lw $t0, 0($t3)
lw $t1, 0($t4)

# 2. Add $t0 and $t1 into $t2
add $t2, $t0, $t1

# 3. Store the sum in memory
sw $t2, 0($t5)