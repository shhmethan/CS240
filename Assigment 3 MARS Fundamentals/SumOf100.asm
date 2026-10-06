.text
.globl main

#	int i = 2; 
#	int sum = 0;
#	
#	for(int i = 1; i<=100; i++) {
#		sum += i;
#	}


main:
    li $t0, 2          		# Current number
    li $t1, 0			# Running sum

loop:                           # Start of loop
    bgt  $t0, 100, finished     # Finish when current number is greater than 100
    add  $t1, $t1, $t0          # sum += current number
    addi $t0, $t0, 2            # Move to the next number
    j loop

finished:                       # End of loop
    li $v0, 1			
    move $a0, $t1
    syscall

    li $v0, 10
    syscall
