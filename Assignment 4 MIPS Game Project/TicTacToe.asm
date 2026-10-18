# Phase 1: Graphical Tic-Tac-Toe for MARS
# Bitmap Display settings:
#   Unit width: 8, Unit height: 8
#   Display width: 256, Display height: 256
#   Base address: 0x10008000
# Instructions/input appear in the MARS console; the board appears graphically.

.eqv DISPLAY_BASE 0x10008000

.data
displayAddress: .word 0x10008000
board:        .space 36
title:        .asciiz "\n=== TIC-TAC-TOE ===\n"
instructions: .asciiz "Choose a square from 1 to 9:\n\n 1 | 2 | 3\n---+---+---\n 4 | 5 | 6\n---+---+---\n 7 | 8 | 9\n\n"
prompt_x:     .asciiz "Player X, choose a square: "
prompt_o:     .asciiz "Player O, choose a square: "
invalid:      .asciiz "Invalid choice. Enter an empty square from 1 to 9.\n"
x_wins:       .asciiz "Player X wins!\n"
o_wins:       .asciiz "Player O wins!\n"
draw_msg:     .asciiz "The game is a draw.\n"
again_prompt: .asciiz "Play again? Enter 1 for yes or 0 for no: "
bye:          .asciiz "Thanks for playing!\n"

.text
.globl main

main:
    la   $s0, board

new_game:
    jal  initialize_game
    jal  clear_screen
    jal  draw_grid
    li   $v0, 4
    la   $a0, title
    syscall
    li   $v0, 4
    la   $a0, instructions
    syscall
    li   $s1, 1                 # current player: 1 = X, 2 = O
    li   $s2, 0                 # move count

game_loop:
    li   $v0, 4
    li   $t7, 1
    beq  $s1, $t7, print_x_prompt
    la   $a0, prompt_o
    syscall
    j    get_move

print_x_prompt:
    la   $a0, prompt_x
    syscall

get_move:
    li   $v0, 5
    syscall
    move $t0, $v0
    slti $t7, $t0, 1
    bne  $t7, $zero, bad_move
    slti $t7, $t0, 10
    beq  $t7, $zero, bad_move
    addi $t1, $t0, -1
    sll  $t2, $t1, 2
    addu $t3, $s0, $t2
    lw   $t4, 0($t3)
    bne  $t4, $zero, bad_move

    sw   $s1, 0($t3)
    addi $s2, $s2, 1

    li   $t5, 3
    div  $t1, $t5
    mflo $a1                   # row
    mfhi $a0                   # column
    move $a2, $s1
    jal  draw_piece

    jal  check_winner
    move $s3, $v0
    bne  $s3, $zero, game_over
    li   $t6, 9
    beq  $s2, $t6, game_draw

    li   $t6, 3
    sub  $s1, $t6, $s1
    j    game_loop

bad_move:
    li   $v0, 4
    la   $a0, invalid
    syscall
    j    game_loop

game_over:
    li   $v0, 4
    li   $t7, 1
    beq  $s3, $t7, show_x_win
    la   $a0, o_wins
    syscall
    j    ask_again
show_x_win:
    la   $a0, x_wins
    syscall
    j    ask_again

game_draw:
    li   $v0, 4
    la   $a0, draw_msg
    syscall

ask_again:
    li   $v0, 4
    la   $a0, again_prompt
    syscall
    li   $v0, 5
    syscall
    li   $t7, 1
    beq  $v0, $t7, new_game
    li   $v0, 4
    la   $a0, bye
    syscall
    li   $v0, 10
    syscall

# Clear the nine board words.
initialize_game:
    move $t0, $s0
    li   $t1, 0
init_loop:
    sw   $zero, 0($t0)
    addi $t0, $t0, 4
    addi $t1, $t1, 1
    li   $t7, 9
    blt  $t1, $t7, init_loop
    jr   $ra

# Fill the 32x32 Bitmap Display with dark gray.
clear_screen:
    addi $sp, $sp, -4
    sw   $ra, 0($sp)
    li   $s4, 0                 # y
clear_y:
    li   $s5, 0                 # x
clear_x:
    move $a0, $s5
    move $a1, $s4
    li   $a2, 0x00202020
    jal  draw_pixel
    addi $s5, $s5, 1
    li   $t7, 32
    blt  $s5, $t7, clear_x
    addi $s4, $s4, 1
    li   $t7, 32
    blt  $s4, $t7, clear_y
    lw   $ra, 0($sp)
    addi $sp, $sp, 4
    jr   $ra

# Draw vertical lines at x=8,16 and horizontal lines at y=8,16.
draw_grid:
    addi $sp, $sp, -4
    sw   $ra, 0($sp)

    # The board is 24 units wide and high.
    # Each cell is 8 units, so boundaries are at 0, 8, 16, and 24.
    li   $s4, 0
vertical_lines:
    li   $a0, 0
    move $a1, $s4
    li   $a2, 0x00FFFFFF
    jal  draw_pixel

    li   $a0, 8
    move $a1, $s4
    li   $a2, 0x00FFFFFF
    jal  draw_pixel

    li   $a0, 16
    move $a1, $s4
    li   $a2, 0x00FFFFFF
    jal  draw_pixel

    li   $a0, 24
    move $a1, $s4
    li   $a2, 0x00FFFFFF
    jal  draw_pixel

    addi $s4, $s4, 1
    li   $t7, 25
    blt  $s4, $t7, vertical_lines

    li   $s4, 0
horizontal_lines:
    move $a0, $s4
    li   $a1, 0
    li   $a2, 0x00FFFFFF
    jal  draw_pixel

    move $a0, $s4
    li   $a1, 8
    li   $a2, 0x00FFFFFF
    jal  draw_pixel

    move $a0, $s4
    li   $a1, 16
    li   $a2, 0x00FFFFFF
    jal  draw_pixel

    move $a0, $s4
    li   $a1, 24
    li   $a2, 0x00FFFFFF
    jal  draw_pixel

    addi $s4, $s4, 1
    li   $t7, 25
    blt  $s4, $t7, horizontal_lines

    lw   $ra, 0($sp)
    addi $sp, $sp, 4
    jr   $ra

# a0 = column, a1 = row, a2 = player.
draw_piece:
    li   $t7, 1
    beq  $a2, $t7, draw_x
    j    draw_o

draw_x:
    addi $sp, $sp, -4
    sw   $ra, 0($sp)
    sll  $s4, $a0, 3
    sll  $s5, $a1, 3
    addi $s4, $s4, 2
    addi $s5, $s5, 2
    li   $s6, 0
draw_x_loop:
    addu $a0, $s4, $s6
    addu $a1, $s5, $s6
    li   $a2, 0x00FF4040
    jal  draw_pixel
    addu $a0, $s4, $s6
    sub  $a1, $s5, $s6
    addi $a1, $a1, 3
    li   $a2, 0x00FF4040
    jal  draw_pixel
    addi $s6, $s6, 1
    li   $t7, 4
    blt  $s6, $t7, draw_x_loop
    lw   $ra, 0($sp)
    addi $sp, $sp, 4
    jr   $ra

draw_o:
    addi $sp, $sp, -4
    sw   $ra, 0($sp)
    sll  $s4, $a0, 3
    sll  $s5, $a1, 3
    addi $s4, $s4, 2
    addi $s5, $s5, 2
    li   $s6, 0
draw_o_loop:
    addu $a0, $s4, $s6
    move $a1, $s5
    li   $a2, 0x004080FF
    jal  draw_pixel
    addu $a0, $s4, $s6
    addi $a1, $s5, 3
    li   $a2, 0x004080FF
    jal  draw_pixel
    move $a0, $s4
    addu $a1, $s5, $s6
    li   $a2, 0x004080FF
    jal  draw_pixel
    addi $a0, $s4, 3
    addu $a1, $s5, $s6
    li   $a2, 0x004080FF
    jal  draw_pixel
    addi $s6, $s6, 1
    li   $t7, 4
    blt  $s6, $t7, draw_o_loop
    lw   $ra, 0($sp)
    addi $sp, $sp, 4
    jr   $ra

# a0=x unit, a1=y unit, a2=0x00RRGGBB color.
draw_pixel:
    sll  $t0, $a1, 5
    addu $t0, $t0, $a0
    sll  $t0, $t0, 2
    lw   $t1, displayAddress
    addu $t1, $t1, $t0
    sw   $a2, 0($t1)
    jr   $ra

# Returns v0=0 for no winner, v0=1 for X, v0=2 for O.
check_winner:
    addi $sp, $sp, -4
    sw   $ra, 0($sp)
    li $a0, 0
    li $a1, 1
    li $a2, 2
    jal check_line
    bne $v0,$zero,winner_done
    li $a0, 3
    li $a1, 4
    li $a2, 5
    jal check_line
    bne $v0,$zero,winner_done
    li $a0, 6
    li $a1, 7
    li $a2, 8
    jal check_line
    bne $v0,$zero,winner_done
    li $a0, 0
    li $a1, 3
    li $a2, 6
    jal check_line
    bne $v0,$zero,winner_done
    li $a0, 1
    li $a1, 4
    li $a2, 7
    jal check_line
    bne $v0,$zero,winner_done
    li $a0, 2
    li $a1, 5
    li $a2, 8
    jal check_line
    bne $v0,$zero,winner_done
    li $a0, 0
    li $a1, 4
    li $a2, 8
    jal check_line
    bne $v0,$zero,winner_done
    li $a0, 2
    li $a1, 4
    li $a2, 6
    jal check_line
winner_done:
    lw   $ra, 0($sp)
    addi $sp, $sp, 4
    jr   $ra

# a0,a1,a2 are board indices for one line.
check_line:
    sll  $t0, $a0, 2
    addu $t0, $s0, $t0
    lw   $t3, 0($t0)
    beq  $t3, $zero, no_line
    sll  $t0, $a1, 2
    addu $t0, $s0, $t0
    lw   $t4, 0($t0)
    bne  $t3, $t4, no_line
    sll  $t0, $a2, 2
    addu $t0, $s0, $t0
    lw   $t5, 0($t0)
    bne  $t3, $t5, no_line
    move $v0, $t3
    jr   $ra
no_line:
    move $v0, $zero
    jr   $ra




