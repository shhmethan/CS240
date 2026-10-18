# Module 4: MIPS Game Project

This repository contains three playable MIPS games created for Module 4:

1. **Tic-Tac-Toe**
2. **Blackjack**
3. **Snake** — the custom game

The games are written for the **MARS MIPS simulator** and demonstrate procedures, stack usage, arrays, branching, loops, system calls, user input, and graphical output.

## Files

| File | Game | Input/display method |
|---|---|---|
| `TicTacToe.asm` | Two-player Tic-Tac-Toe | Console input and MARS Bitmap Display |
| `BlackJack.asm` | Player-versus-dealer Blackjack | Console input and output; graphical display support is planned for the final version |
| `CustomGame.asm` | Snake | Keyboard and Display MMIO Simulator |

## Requirements

- MARS MIPS simulator
- Java Runtime Environment compatible with MARS
- A MARS Bitmap Display for Tic-Tac-Toe
- A MARS Keyboard and Display MMIO Simulator for Snake

The programs use MARS-specific system calls for random numbers, time, and input/output.

## Running Tic-Tac-Toe

1. Open `TicTacToe.asm` in MARS.
2. Open **Tools → Bitmap Display**.
3. Use these Bitmap Display settings:

   - Unit Width: `8`
   - Unit Height: `8`
   - Display Width: `256`
   - Display Height: `256`
   - Base Address: `0x10008000`

4. Connect the display to MARS.
5. Assemble and run the program.
6. Enter a square number from `1` through `9` in the MARS console.

The console shows the numbered board and instructions. The actual board, grid, X pieces, and O pieces appear in the Bitmap Display.

### Tic-Tac-Toe controls

```text
1 2 3
4 5 6
7 8 9
```

Players alternate between X and O. A move is rejected if it is outside the range `1–9` or if the selected square is already occupied.

## Running Blackjack

1. Open `BlackJack.asm` in MARS.
2. Assemble and run the program.
3. Follow the prompts in the MARS console.

### Blackjack controls

- Enter `1` to hit.
- Enter `2` to stand.
- Enter `1` at the replay prompt to play another round.
- Enter `0` at the replay prompt to quit.

The game stores player and dealer cards in byte arrays. Aces are automatically counted as either `11` or `1` when necessary. The dealer continues drawing until reaching a value of at least `17`.

## Running Snake

1. Open `CustomGame.asm` in MARS.
2. Open **Tools → Keyboard and Display MMIO Simulator**.
3. Connect the simulator to MARS.
4. Assemble and run the program.
5. Click inside the keyboard input area of the MMIO window.
6. Use the movement keys while the game is running.

### Snake controls

- `W` or `w`: move up
- `A` or `a`: move left
- `S` or `s`: move down
- `D` or `d`: move right

The snake grows when it reaches blue food. The game ends when the snake reaches a red wall or its own body. Other keyboard keys are ignored.

Snake uses display memory to store the snake body and food. Each body cell also stores the direction needed to find the next cell when the tail moves.

## Procedures and game state

### Tic-Tac-Toe

- `initialize_game` clears the board array.
- `clear_screen` resets the graphical display.
- `draw_grid` draws the board grid.
- `draw_piece` draws an X or O.
- `check_winner` and `check_line` evaluate winning combinations.

The board is stored as nine words in memory. A value of `1` represents X, and a value of `2` represents O.

### Blackjack

- `seed_random` initializes the random-number generator.
- `deal_card_safe` adds a card without exceeding the hand limit.
- `hand_value` calculates a hand's Blackjack value, including Ace handling.
- `player_turn` handles hit/stand input.
- `dealer_turn` performs the dealer's automatic turn.
- `decide_winner` compares the final hands.

The player and dealer hands are stored in separate 12-byte arrays.

### Snake

- `initialize_game` sets the starting position and direction.
- `draw_walls` creates the red boundary.
- `place_food` finds an empty display cell for food.
- `read_input` reads movement keys from the MMIO simulator.
- `move_snake` advances the snake and checks for food or collisions.
- `show_game_over` prints the ending message.

## Testing checklist

The final submission should include screenshots and test results for at least the following cases:

### Normal tests

1. Tic-Tac-Toe: X wins with a horizontal, vertical, or diagonal line.
2. Blackjack: The player stands and the dealer completes its turn.
3. Snake: The snake moves, reaches food, and grows.

### Edge-case tests

1. Tic-Tac-Toe: Enter a number below `1`, above `9`, or choose an occupied square.
2. Blackjack: Enter an invalid hit/stand option or replay option.
3. Snake: Press keys other than W/A/S/D and verify that they are ignored.
4. Snake: Run into a wall or the snake's own body.

## Assignment features demonstrated

- Multiple reusable MIPS procedures
- Stack use for saving return addresses
- Arrays and memory-based game state
- Conditional branches and loops
- MARS system calls
- User input and input validation
- Graphical display output
- Turn-based and real-time game logic
- Collision, bust, win, loss, and draw conditions

## Acknowledgments

This project uses the MARS MIPS simulator and concepts from the course materials, including the assigned ZyBooks Chapter 4 reading. Any outside code, examples, or assistance should be acknowledged in the final PDF according to the course requirements.

## Project status

Tic-Tac-Toe and Snake use graphical MARS tools. Before submitting the final project, verify that Blackjack also satisfies the assignment's graphic-display requirement and confirm all three programs using the test cases above.
