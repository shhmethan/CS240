.data
newline: .asciiz "\n"

.text
.globl main

# int i = 1;
#
# while (i <= 100) {
#     print(i);
#     print("\n");
#     i++;
# }

main:
    li $t0, 1                  # Current integer

loop:                          # Start of loop
    bgt $t0, 100, finished     # Finish when current integer is greater than 100

    li $v0, 1                  # Select print-integer syscall
    move $a0, $t0              # Move current integer into the syscall argument
    syscall                    # Print current integer

    li $v0, 4                  # Select print-string syscall
    la $a0, newline            # Load address of newline string
    syscall                    # Print newline

    addi $t0, $t0, 1           # Move to the next integer
    j loop                     # Repeat the loop

finished:                      # End of loop
    li $v0, 10                 # Select exit syscall
    syscall                    # Exit program