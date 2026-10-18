# Compact Snake for MARS
# Bitmap Display: unit 8x8, display 512x256, base 0x10008000 ($gp)
# Keyboard and Display MMIO Simulator: connect it, then use W/A/S/D.
# The compact body representation is preserved: each body cell stores its
# next-direction byte in the unused top byte of the display word.

.eqv DELAY 100

.data
instructions: .asciiz "\n=== SNAKE ===\nUse W/A/S/D to move. Eat blue food. Avoid red walls and yourself.\n\n"
game_over_msg:.asciiz "\nGame over! Reset and run to play again.\n"

.text
.globl main

main:
    lui   $s6, 0xFFFF             # MMIO base and red wall color
    li    $s7, 0xC00140FF         # packed directions and blue food color
    jal   initialize_game
    jal   draw_walls
    jal   place_food
    li    $v0, 4
    la    $a0, instructions
    syscall

game_loop:
    sw    $s2, 0($s5)             # paint the current head
    li    $v0, 30                # current time
    syscall
    addiu $t8, $a0, DELAY         # busy-wait so the GUI stays responsive
wait:
    li    $v0, 30
    syscall
    slt   $t0, $a0, $t8
    bnez  $t0, wait

    jal   read_input
    jal   move_snake
    li    $t7, 1
    beq   $v0, $t7, ate_food
    li    $t7, 2
    beq   $v0, $t7, end_game
    j     game_loop

ate_food:
    jal   place_food
    j     game_loop

end_game:
    jal   show_game_over
    li    $v0, 10
    syscall

# Initialize the snake and its direction. The head starts at row 16, col 32.
initialize_game:
    addiu $s5, $gp, 4224         # head position
    move  $s3, $s5               # tail position
    li    $s4, 0x01000000        # initially move right
    ori   $s2, $s4, 0xFF00       # green body/head word
    jr    $ra

# Draw red walls around the 64x32-unit play area.
draw_walls:
    addiu $t0, $gp, 256
    addiu $t1, $gp, 8192
wall_loop:
    addiu $t0, $t0, -8
    addiu $t1, $t1, -256
    sw    $s6, 0($t0)
    sw    $s6, 4($t0)
    sw    $s6, 7936($t0)
    sw    $s6, 7940($t0)
    sw    $s6, 0($t1)
    sw    $s6, 252($t1)
    bne   $t0, $gp, wall_loop
    jr    $ra

# Place blue food in an empty display cell using the current clock value.
place_food:
    li    $v0, 30
    syscall
food_probe:
    andi  $t0, $a0, 0x1FFC
    addu  $t0, $t0, $gp
    lw    $t1, 0($t0)
    addiu $a0, $a0, 156
    bnez  $t1, food_probe
    sw    $s7, 0($t0)
    jr    $ra

# Convert only valid W/A/S/D keys into a direction. Other keys are ignored.
read_input:
    lw    $t0, 4($s6)
    li    $t1, 97                # a
    beq   $t0, $t1, valid_key
    li    $t1, 65                # A
    beq   $t0, $t1, valid_key
    li    $t1, 115               # s
    beq   $t0, $t1, valid_key
    li    $t1, 83                # S
    beq   $t0, $t1, valid_key
    li    $t1, 100               # d
    beq   $t0, $t1, valid_key
    li    $t1, 68                # D
    beq   $t0, $t1, valid_key
    li    $t1, 119               # w
    beq   $t0, $t1, valid_key
    li    $t1, 87                # W
    bne   $t0, $t1, read_done
valid_key:
    sll   $t0, $t0, 2
    andi  $t0, $t0, 0x18
    srav  $t0, $s7, $t0
    sll   $t0, $t0, 24           # direction stored in the top byte
    addu  $t1, $t0, $s4
    beqz  $t1, read_done         # do not reverse into the snake
    move  $s4, $t0
read_done:
    jr    $ra

# Move one step. Returns v0=0 normal, v0=1 food, v0=2 collision.
move_snake:
    ori   $s2, $s4, 0xFF00       # old head points toward new head
    sw    $s2, 0($s5)
    sra   $t0, $s4, 22           # direction byte -> byte offset
    addu  $s5, $s5, $t0
    lw    $t0, 0($s5)
    beq   $t0, $s7, move_food
    bnez  $t0, move_collision

    lw    $t0, 0($s3)             # follow the tail's direction
    sw    $zero, 0($s3)
    sra   $t0, $t0, 22
    addu  $s3, $s3, $t0
    move  $v0, $zero
    jr    $ra
move_food:
    li    $v0, 1
    jr    $ra
move_collision:
    li    $v0, 2
    jr    $ra

show_game_over:
    li    $v0, 4
    la    $a0, game_over_msg
    syscall
    jr    $ra
