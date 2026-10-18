# snake-tiny.asm - size-optimized Snake for MARS. No .data at all.
#
# Setup in MARS:
#   Tools > Bitmap Display: unit 8x8, display 512x256,
#           base address 0x10008000 ($gp) -> Connect to MIPS
#   Tools > Keyboard and Display MMIO Simulator -> Connect to MIPS
#   Run, then type w/a/s/d in the MMIO keyboard box (upper or lower case).
#   Dying ends the program; Reset + Run to play again.
#
# Size tricks:
#   - Background is 0, so zero-initialized memory is a free clear screen.
#   - No body array: each body cell stores the direction to the next segment
#     in its top byte (the display ignores bits 24-31). The tail just follows.
#   - Key -> direction: ((key >> 1) & 3) indexes a 4-byte table packed into
#     one register. Works for wasd and WASD.
#   - The keyboard data register always holds the last key, so no ready-bit
#     check; at start it is 0, which maps to "left".
#   - 0xFFFF0000 (MMIO base) doubles as the wall colour (red).
#   - The packed table doubles as the food colour (blue).
#   - Dying branches past the last instruction, which ends the program.
#   - Food position comes from the clock value the delay loop leaves in $a0.

.eqv DELAY 100                      # ms per move

    lui   $s6, 0xFFFF               # MMIO base / wall colour
    li    $s7, 0xC00140FF           # dir/4 table: a=-1 s=64 d=1 w=-64 / food colour
    li    $v0, 30                   # syscall 30 = time in ms
    addiu $s5, $gp, 4224            # head: row 16, col 32
    move  $s3, $s5                  # tail
    addiu $t0, $gp, 256             # top/bottom row pointer
    addiu $t1, $gp, 8192            # left/right column pointer
walls:
    addiu $t0, $t0, -8
    addiu $t1, $t1, -256
    sw    $s6, 0($t0)               # top row, 2 cells
    sw    $s6, 4($t0)
    sw    $s6, 7936($t0)            # bottom row, 2 cells
    sw    $s6, 7940($t0)
    sw    $s6, 0($t1)               # left column
    sw    $s6, 252($t1)             # right column
    bne   $t0, $gp, walls

food:                               # probe cells from a pseudo-random start
    andi  $t0, $a0, 0x1FFC
    addu  $t0, $t0, $gp
    lw    $t1, 0($t0)
    addiu $a0, $a0, 156             # odd cell step: visits every cell
    bnez  $t1, food
    sw    $s7, 0($t0)

draw:
    sw    $s2, 0($s5)               # paint head
    syscall                         # busy-wait DELAY ms (no syscall 32:
    addiu $t8, $a0, DELAY           # sleeping freezes the MARS GUI)
wait:
    syscall
    slt   $t0, $a0, $t8
    bnez  $t0, wait

    lw    $t0, 4($s6)               # last key typed
    sll   $t0, $t0, 2
    andi  $t0, $t0, 0x18            # 8 * ((key >> 1) & 3)
    srav  $t0, $s7, $t0
    sll   $t0, $t0, 24              # direction kept as (dir/4) << 24
    addu  $t1, $t0, $s4
    beqz  $t1, keep                 # ignore reversing into yourself
    move  $s4, $t0
keep:
    ori   $s2, $s4, 0xFF00          # body cell: direction byte + green
    sw    $s2, 0($s5)               # old head now points at new head
    sra   $t0, $s4, 22              # direction in bytes
    addu  $s5, $s5, $t0
    lw    $t0, 0($s5)
    beq   $t0, $s7, food            # ate food: grow (tail stays)
    bnez  $t0, end                  # wall or body: game over

    lw    $t0, 0($s3)               # tail cell says where the next one is
    sw    $zero, 0($s3)
    sra   $t0, $t0, 22
    addu  $s3, $s3, $t0
    j     draw
end:
