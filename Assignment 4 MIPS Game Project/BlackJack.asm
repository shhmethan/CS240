# Phase 2: Blackjack for MARS
# Console game with procedures, arrays, loops, branching, input validation,
# dealer/player turn logic, Ace handling, bust detection, capacity checks, and replay.

.eqv MAX_HAND 12

.data
player_hand: .space 12
dealer_hand: .space 12

title:        .asciiz "\n=== BLACKJACK ===\n"
rules:        .asciiz "Get as close to 21 as possible without going over.\n"
player_text:  .asciiz "Your hand: "
dealer_text:  .asciiz "Dealer's hand: "
hidden_text:  .asciiz "[hidden]"
space_text:   .asciiz " "
value_text:   .asciiz "  Value: "
hit_prompt:   .asciiz "\nEnter 1 to hit or 2 to stand: "
invalid:      .asciiz "Invalid choice. Enter 1 or 2.\n"
replay_invalid:.asciiz "Invalid choice. Enter 1 to play again or 0 to quit.\n"
bust_player:  .asciiz "\nYou busted. Dealer wins.\n"
bust_dealer:  .asciiz "\nDealer busted. You win!\n"
player_wins:  .asciiz "\nYou win!\n"
dealer_wins:  .asciiz "\nDealer wins.\n"
tie_text:     .asciiz "\nIt's a tie.\n"
hand_limit:   .asciiz "The hand is full, so you must stand.\n"
replay_text:  .asciiz "\nPlay again? Enter 1 for yes or 0 for no: "
bye:          .asciiz "Thanks for playing Blackjack!\n"

ace_text:     .asciiz "A"
two_text:     .asciiz "2"
three_text:   .asciiz "3"
four_text:    .asciiz "4"
five_text:    .asciiz "5"
six_text:     .asciiz "6"
seven_text:   .asciiz "7"
eight_text:   .asciiz "8"
nine_text:    .asciiz "9"
ten_text:     .asciiz "10"
jack_text:    .asciiz "J"
queen_text:   .asciiz "Q"
king_text:    .asciiz "K"

.text
.globl main

main:
    jal  seed_random

new_round:
    la   $s3, player_hand
    la   $s4, dealer_hand
    li   $s1, 0                 # player count
    li   $s2, 0                 # dealer count

    # Two player cards.
    move $a0, $s3
    move $a1, $s1
    jal  deal_card_safe
    addi $s1, $s1, 1
    move $a0, $s3
    move $a1, $s1
    jal  deal_card_safe
    addi $s1, $s1, 1

    # Two dealer cards.
    move $a0, $s4
    move $a1, $s2
    jal  deal_card_safe
    addi $s2, $s2, 1
    move $a0, $s4
    move $a1, $s2
    jal  deal_card_safe
    addi $s2, $s2, 1

    li   $v0, 4
    la   $a0, title
    syscall
    li   $v0, 4
    la   $a0, rules
    syscall

    # Show dealer's first card, hiding the second.
    li   $v0, 4
    la   $a0, dealer_text
    syscall
    lbu  $a0, 0($s4)
    jal  print_card
    li   $v0, 4
    la   $a0, space_text
    syscall
    li   $v0, 4
    la   $a0, hidden_text
    syscall
    li   $v0, 11
    li   $a0, 10
    syscall

    jal  print_player_hand
    jal  player_turn
    li   $t7, 1
    beq  $v0, $t7, player_busted

    jal  dealer_turn
    jal  print_dealer_hand
    jal  decide_winner
    j    replay

player_busted:
    li   $v0, 4
    la   $a0, bust_player
    syscall
    j    replay

# Seed random generator 0 using the system time.
seed_random:
    li   $v0, 30
    syscall
    move $t0, $a0
    li   $v0, 40
    li   $a0, 0
    move $a1, $t0
    syscall
    jr   $ra

# Returns a card from 1 through 13 in v0.
random_card:
    li   $v0, 42
    li   $a0, 0
    li   $a1, 13
    syscall
    addi $v0, $a0, 1
    jr   $ra

# a0=array base, a1=index, a2=card.
store_card:
    addu $t0, $a0, $a1
    sb   $a2, 0($t0)
    jr   $ra

# a0=array base, a1=count; returns total in v0.
hand_value:
    li   $t0, 0                 # total
    li   $t1, 0                 # aces
    li   $t2, 0                 # index
value_loop:
    beq  $t2, $a1, adjust_aces
    addu $t3, $a0, $t2
    lbu  $t4, 0($t3)
    li   $t7, 1
    beq  $t4, $t7, add_ace
    li   $t7, 10
    ble  $t4, $t7, add_number
    addi $t0, $t0, 10
    addi $t2, $t2, 1
    j    value_loop
add_ace:
    addi $t0, $t0, 11
    addi $t1, $t1, 1
    addi $t2, $t2, 1
    j    value_loop
add_number:
    addu $t0, $t0, $t4
    addi $t2, $t2, 1
    j    value_loop
adjust_aces:
    li   $t7, 21
ace_adjust_loop:
    ble  $t0, $t7, value_done
    beq  $t1, $zero, value_done
    addi $t0, $t0, -10
    addi $t1, $t1, -1
    j    ace_adjust_loop
value_done:
    move $v0, $t0
    jr   $ra

# a0=card value; prints card name.
print_card:
    li $t7,1
    beq $a0,$t7,card_ace
    li $t7,2
    beq $a0,$t7,card_two
    li $t7,3
    beq $a0,$t7,card_three
    li $t7,4
    beq $a0,$t7,card_four
    li $t7,5
    beq $a0,$t7,card_five
    li $t7,6
    beq $a0,$t7,card_six
    li $t7,7
    beq $a0,$t7,card_seven
    li $t7,8
    beq $a0,$t7,card_eight
    li $t7,9
    beq $a0,$t7,card_nine
    li $t7,10
    beq $a0,$t7,card_ten
    li $t7,11
    beq $a0,$t7,card_jack
    li $t7,12
    beq $a0,$t7,card_queen
    la $a0, king_text
    j print_card_text
card_ace:
    la $a0, ace_text
    j print_card_text
card_two:
    la $a0, two_text
    j print_card_text
card_three:
    la $a0, three_text
    j print_card_text
card_four:
    la $a0, four_text
    j print_card_text
card_five:
    la $a0, five_text
    j print_card_text
card_six:
    la $a0, six_text
    j print_card_text
card_seven:
    la $a0, seven_text
    j print_card_text
card_eight:
    la $a0, eight_text
    j print_card_text
card_nine:
    la $a0, nine_text
    j print_card_text
card_ten:
    la $a0, ten_text
    j print_card_text
card_jack:
    la $a0, jack_text
    j print_card_text
card_queen:
    la $a0, queen_text
    j print_card_text
print_card_text:
    li $v0, 4
    syscall
    jr $ra

# Print player's complete hand and total.
print_player_hand:
    addi $sp, $sp, -4
    sw   $ra, 0($sp)
    li   $v0, 4
    la   $a0, player_text
    syscall
    li   $t0, 0
player_print_loop:
    beq  $t0, $s1, player_print_value
    addu $t1, $s3, $t0
    lbu  $a0, 0($t1)
    jal  print_card
    li   $v0, 4
    la   $a0, space_text
    syscall
    addi $t0, $t0, 1
    j    player_print_loop
player_print_value:
    li   $v0, 4
    la   $a0, value_text
    syscall
    move $a0, $s3
    move $a1, $s1
    jal  hand_value
    move $a0, $v0
    li   $v0, 1
    syscall
    li   $v0, 11
    li   $a0, 10
    syscall
    lw   $ra, 0($sp)
    addi $sp, $sp, 4
    jr   $ra

# Player turn. Returns v0=0 for stand, v0=1 for bust.
player_turn:
    addi $sp, $sp, -4
    sw   $ra, 0($sp)
player_choice:
    li   $v0, 4
    la   $a0, hit_prompt
    syscall
    li   $v0, 5
    syscall
    li   $t7, 1
    beq  $v0, $t7, player_hit
    li   $t7, 2
    beq  $v0, $t7, player_stand
    li   $v0, 4
    la   $a0, invalid
    syscall
    j    player_choice

player_hit:
    # Prevent writing past the 12-byte player_hand array.
    li   $t7, MAX_HAND
    bge  $s1, $t7, hand_full_stand
    move $a0, $s3
    move $a1, $s1
    jal  deal_card_safe
    addi $s1, $s1, 1
    jal  print_player_hand
    move $a0, $s3
    move $a1, $s1
    jal  hand_value
    li   $t7, 21
    bgt  $v0, $t7, player_bust_return
    j    player_choice

hand_full_stand:
    li   $v0, 4
    la   $a0, hand_limit
    syscall
    j    player_stand

player_bust_return:
    li   $v0, 1
    lw   $ra, 0($sp)
    addi $sp, $sp, 4
    jr   $ra
player_stand:
    move $v0, $zero
    lw   $ra, 0($sp)
    addi $sp, $sp, 4
    jr   $ra

# Dealer hits until total is 17 or more.
dealer_turn:
    addi $sp, $sp, -4
    sw   $ra, 0($sp)
dealer_loop:
    move $a0, $s4
    move $a1, $s2
    jal  hand_value
    li   $t7, 17
    bge  $v0, $t7, dealer_done
    # Stop safely if the dealer reaches the array capacity.
    li   $t7, MAX_HAND
    bge  $s2, $t7, dealer_done
    move $a0, $s4
    move $a1, $s2
    jal  deal_card_safe
    addi $s2, $s2, 1
    j    dealer_loop
dealer_done:
    lw   $ra, 0($sp)
    addi $sp, $sp, 4
    jr   $ra

# Print dealer's complete hand and total.
print_dealer_hand:
    addi $sp, $sp, -4
    sw   $ra, 0($sp)
    li   $v0, 4
    la   $a0, dealer_text
    syscall
    li   $t0, 0
dealer_print_loop:
    beq  $t0, $s2, dealer_print_value
    addu $t1, $s4, $t0
    lbu  $a0, 0($t1)
    jal  print_card
    li   $v0, 4
    la   $a0, space_text
    syscall
    addi $t0, $t0, 1
    j    dealer_print_loop
dealer_print_value:
    li   $v0, 4
    la   $a0, value_text
    syscall
    move $a0, $s4
    move $a1, $s2
    jal  hand_value
    move $a0, $v0
    li   $v0, 1
    syscall
    li   $v0, 11
    li   $a0, 10
    syscall
    lw   $ra, 0($sp)
    addi $sp, $sp, 4
    jr   $ra

# Compare totals and print the result.
decide_winner:
    addi $sp, $sp, -4
    sw   $ra, 0($sp)
    move $a0, $s3
    move $a1, $s1
    jal  hand_value
    move $t0, $v0
    move $a0, $s4
    move $a1, $s2
    jal  hand_value
    move $t1, $v0
    li   $t7, 21
    bgt  $t1, $t7, dealer_bust_result
    bgt  $t0, $t1, player_win_result
    blt  $t0, $t1, dealer_win_result
    li   $v0, 4
    la   $a0, tie_text
    syscall
    j    winner_return
dealer_bust_result:
    li   $v0, 4
    la   $a0, bust_dealer
    syscall
    j    winner_return
player_win_result:
    li   $v0, 4
    la   $a0, player_wins
    syscall
    j    winner_return
dealer_win_result:
    li   $v0, 4
    la   $a0, dealer_wins
    syscall
winner_return:
    lw   $ra, 0($sp)
    addi $sp, $sp, 4
    jr   $ra

# Ask whether to start another round.
replay:
    li   $v0, 4
    la   $a0, replay_text
    syscall
    li   $v0, 5
    syscall
    li   $t7, 1
    beq  $v0, $t7, new_round
    li   $t7, 0
    beq  $v0, $t7, exit_game
    li   $v0, 4
    la   $a0, replay_invalid
    syscall
    j    replay

exit_game:
    li   $v0, 4
    la   $a0, bye
    syscall
    li   $v0, 10
    syscall

# a0=array base, a1=index; draw and store a random card.
deal_card_safe:
    addi $sp, $sp, -12
    sw   $ra, 8($sp)
    sw   $a0, 0($sp)
    sw   $a1, 4($sp)
    li   $t7, MAX_HAND
    bge  $a1, $t7, deal_failed
    jal  random_card
    move $a2, $v0
    lw   $a0, 0($sp)
    lw   $a1, 4($sp)
    jal  store_card
    li   $v0, 1
    lw   $ra, 8($sp)
    addi $sp, $sp, 12
    jr   $ra

deal_failed:
    move $v0, $zero
    lw   $ra, 8($sp)
    addi $sp, $sp, 12
    jr   $ra

