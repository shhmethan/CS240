.data
newline: .asciiz "\n"
fizz: .asciiz "Fizz\n"
buzz: .asciiz "Buzz\n"
fizzBuzz: .asciiz "FizzBuzz\n"

.text
.globl main

# int i = 1;
#
# while (i <= 100) {
#     if(i % 3 ==0 && i % 5 == 0) {print("FizzBuzz\n"); i++; continue;}
#     if(i % 3 == 0) {print("Fizz\n"); i++; continue;}
#     if(i % 5 == 0) {print("Buzz\n"); i++; continue;}
#
#     print(i);
#     print("\n");
#     i++;
# }


main:
    li $t0, 1                  # Current integer

loop:                          # Start of loop
    bgt $t0, 100, finished	# if i > 100 → finished
    
    rem $t2, $t0, 15
    beq $t2, $zero, printFizzBuzz	# if i % 3 == 0 && i % 5 ==0 → PRINT_FIZZ_BUZZ
    rem $t2, $t0, 3
    beq $t2, $zero, printFizz	# if i % 3 == 0 → PRINT_FIZZ
    rem $t2, $t0, 5
    beq $t2, $zero, printBuzz	# if i % 5 == 0 → PRINT_BUZZ

				
    li $v0, 1                  
    move $a0, $t0              
    syscall                    # Print current integer

    li $v0, 4                  
    la $a0, newline            
    syscall                    # Print newline

    addi $t0, $t0, 1           # Move to the next integer
    j loop                     # Repeat the loop

printFizz:
    li $v0, 4      
    la $a0, fizz
    syscall			# Print "Fizz"
    
    addi $t0, $t0, 1           # Move to the next integer
    j loop                     # Repeat the loop
    
printBuzz:
    li $v0, 4      
    la $a0, buzz
    syscall			# Print "Buzz"
    
    addi $t0, $t0, 1           # Move to the next integer
    j loop                     # Repeat the loop

printFizzBuzz:
    li $v0, 4      
    la $a0, fizzBuzz
    syscall			# Print "FizzBuzz"
    
    addi $t0, $t0, 1           # Move to the next integer
    j loop                     # Repeat the loop
    
finished:                      # End of loop
    li $v0, 10                 # Select exit syscall
    syscall                    # Exit program
