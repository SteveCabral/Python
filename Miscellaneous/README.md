# Miscellaneous Python Projects

## Table of Contents

- [StringWheelOfFortune.py](#stringwheeloffortunepy)
- [PythonTest.py](#pythontestpy)

---

## StringWheelOfFortune.py

# Wheel of Fortune Phrase Board

## Overview

The `StringWheelOfFortune.py` module provides a Python class that accurately mimics the classic Wheel of Fortune game show phrase board. The `WheelOfFortunePhraseBoard` class implements the exact layout and behavior of the iconic puzzle board, including proper word wrapping, horizontal and vertical centering, and the unique column structure.

## WheelOfFortunePhraseBoard Class

### Description

The `WheelOfFortunePhraseBoard` class creates a digital representation of the Wheel of Fortune phrase board with authentic dimensions and layout constraints.

### Board Specifications

#### Dimensions
- **Total Size:** 14 columns × 4 rows
- **Maximum Capacity:** 52 characters (including spaces)

#### Row Layout
The board has a distinctive structure where the first and last rows have reduced character capacity:

| Row | Available Columns | Character Capacity | Column Range (1-indexed) |
|-----|-------------------|-------------------|-------------------------|
| 1   | 12 characters     | Columns 2-13      | `[1-12]` (0-indexed)   |
| 2   | 14 characters     | Columns 1-14      | `[0-13]` (0-indexed)   |
| 3   | 14 characters     | Columns 1-14      | `[0-13]` (0-indexed)   |
| 4   | 12 characters     | Columns 2-13      | `[1-12]` (0-indexed)   |

This creates the characteristic "stepped" appearance of the classic game board.

### Features

#### 1. Intelligent Word Wrapping
- Words are never split across rows
- Automatically moves to the next row when a word doesn't fit
- Validates that individual words aren't too long for any single row
- Preserves spaces between words

#### 2. Horizontal Centering
- Each row's content is centered within its available column space
- Calculates optimal padding for balanced appearance
- Maintains word spacing and readability

#### 3. Vertical Centering
- Phrases are centered across all 4 rows
- Automatically determines the optimal starting row based on phrase length
- Examples:
  - **1-row phrase:** Appears on row 2 (middle rows)
  - **2-row phrase:** Appears on rows 2-3 (centered vertically)
  - **3-row phrase:** Appears on rows 1-3
  - **4-row phrase:** Uses all rows

#### 4. Validation
- Ensures phrase doesn't exceed 52 characters
- Validates that words fit within row constraints
- Raises descriptive errors for invalid inputs

### Constructor

```python
WheelOfFortunePhraseBoard(phrase: str)
```

**Parameters:**
- `phrase` (str): The puzzle phrase, up to 52 characters. Can include letters, spaces, and punctuation.

**Raises:**
- `ValueError`: If phrase exceeds 52 characters
- `ValueError`: If a single word is too long to fit on any row
- `ValueError`: If the phrase is too long to distribute across all rows

**Example:**
```python
board = WheelOfFortunePhraseBoard("A FUN FAMILY GAME")
```

### Public Methods

#### `get_board() -> list`

Returns a 2D array representation of the phrase board.

**Returns:**
- `list`: A 4×14 2D list where each element represents a board position. Returns a copy to prevent external modification.

**Example:**
```python
board = WheelOfFortunePhraseBoard("HELLO WORLD")
board_array = board.get_board()
# board_array is a 4x14 list of characters
```

#### `display()`

Prints a formatted visual representation of the phrase board to the console, complete with borders and proper spacing. The display shows the phrase with both horizontal centering (each row's content centered within its available columns) and vertical centering (the phrase centered across all 4 rows).

**Returns:** None (prints to stdout)

**Example Output:**
```
+-----------------------------+
|                             |
|   A   F U N   F A M I L Y   |
|        G A M E              |
|                             |
+-----------------------------+
```

**Note:** The output demonstrates how a 2-row phrase is vertically centered (appearing on rows 2-3) with each row's text horizontally centered within its available column space.

#### `reveal_letter(letter: str) -> int`

Counts how many times a specific letter appears in the phrase.

**Parameters:**
- `letter` (str): The letter to search for (case-insensitive)

**Returns:**
- `int`: Number of occurrences of the letter

**Example:**
```python
board = WheelOfFortunePhraseBoard("HELLO WORLD")
count = board.reveal_letter('L')  # Returns 3
```

#### `__str__() -> str`

Returns a string representation of the board (4 lines, 14 characters each).

**Returns:**
- `str`: Multi-line string representation

**Example:**
```python
board = WheelOfFortunePhraseBoard("TEST")
print(str(board))
```

### Private Methods

#### `_get_row_layout(row_index: int) -> tuple`

Determines the available columns for a specific row.

**Parameters:**
- `row_index` (int): Row index (0-3)

**Returns:**
- `tuple`: (start_col, num_cols) - starting column index and number of available columns

**Internal Use:** This method encapsulates the board's unique layout logic.

#### `_create_board() -> list`

Creates the phrase board layout with proper word distribution, horizontal centering per row, and vertical centering across all rows.

**Algorithm:**
1. **First Pass:** Distributes words across rows while respecting word boundaries
2. **Second Pass:** Places content with both horizontal and vertical centering applied

**Returns:**
- `list`: The initialized 4×14 board array

## Usage Examples

### Basic Usage

```python
from StringWheelOfFortune import WheelOfFortunePhraseBoard

# Create a board with a phrase
board = WheelOfFortunePhraseBoard("THE QUICK BROWN FOX")

# Display the board
board.display()

# Get the board as an array
board_array = board.get_board()

# Check for a letter
occurrences = board.reveal_letter('O')
print(f"Letter 'O' appears {occurrences} times")
```

### Integration with Game Logic

```python
# Game setup
phrase = "WHEEL OF FORTUNE"
board = WheelOfFortunePhraseBoard(phrase)

# Player guesses a letter
guess = 'E'
count = board.reveal_letter(guess)

if count > 0:
    print(f"Correct! '{guess}' appears {count} time(s)")
    board.display()
else:
    print(f"Sorry, '{guess}' is not in the puzzle")
```

### Accessing Board Data

```python
board = WheelOfFortunePhraseBoard("PYTHON PROGRAMMING")
board_array = board.get_board()

# Iterate through all positions
for row_idx, row in enumerate(board_array):
    for col_idx, char in enumerate(row):
        if char != ' ':
            print(f"Row {row_idx+1}, Col {col_idx+1}: {char}")
```

## Technical Details

### Character Limits

| Configuration | Maximum Characters |
|---------------|-------------------|
| Row 1 or 4    | 12 characters     |
| Row 2 or 3    | 14 characters     |
| Total Board   | 52 characters     |

### Storage Structure

The board is stored internally as a 2D list:
- Outer list: 4 elements (rows)
- Inner lists: 14 elements each (columns)
- Each element: Single character or space

### Coordinate System

- **Rows:** 0-indexed from top to bottom (0-3)
- **Columns:** 0-indexed from left to right (0-13)
- **Unavailable positions:** Filled with spaces but not used for phrase content

## Error Handling

The class provides comprehensive validation with descriptive error messages:

```python
# Phrase too long
try:
    board = WheelOfFortunePhraseBoard("A" * 60)
except ValueError as e:
    print(e)  # "Phrase cannot exceed 52 characters"

# Word too long for any row
try:
    board = WheelOfFortunePhraseBoard("SUPERCALIFRAGILISTICEXPIALIDOCIOUS")
except ValueError as e:
    print(e)  # "Word 'SUPERCALIFRAGILISTICEXPIALIDOCIOUS' is too long to fit on a single row"
```

## Design Patterns

### Encapsulation
- Private methods (`_create_board`, `_get_row_layout`) hide implementation details
- Public interface is clean and intuitive

### Immutability
- `get_board()` returns a copy to prevent external modification
- Internal state protected from unintended changes

### Single Responsibility
- Each method has a clear, focused purpose
- Separation of concerns between layout logic and display logic

## Testing

The module includes comprehensive test examples in the `__main__` block:

```bash
python StringWheelOfFortune.py
```

This will demonstrate:
- Long phrase handling
- Short phrase handling
- Centering behavior
- Board array structure

## Future Enhancements

Potential additions to consider:
- Hidden letter display (showing only revealed letters)
- Category label support
- Multiple phrase/puzzle support
- Export to different formats (JSON, XML)
- Custom board dimensions
- Animation support for letter reveals

## License

This code is provided as-is for educational and entertainment purposes.

## Author

Created for Python learning and game development projects.

---

**Last Updated:** November 29, 2025

---

## PythonTest.py

A simple Python testing file used for experimenting with basic Python string operations and case transformations.

### Contents

- Basic string variable manipulation
- String case conversion methods (`.upper()`, `.swapcase()`, `.title()`)
- Example code for learning Python fundamentals

### Usage

```bash
python PythonTest.py
```

This file is primarily used for quick Python syntax testing and experimentation.
