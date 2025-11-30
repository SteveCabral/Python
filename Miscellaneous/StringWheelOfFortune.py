# StringWheelOfFortune.py
class WheelOfFortunePhraseBoard:
    """
    Mimics the Wheel of Fortune phrase board layout.
    
    Board dimensions: 14 columns x 4 rows
    Row 1 (index 0): columns 2-13 available (12 characters)
    Row 2 (index 1): columns 1-14 available (14 characters)
    Row 3 (index 2): columns 1-14 available (14 characters)
    Row 4 (index 3): columns 2-13 available (12 characters)
    
    Total available positions: 12 + 14 + 14 + 12 = 52 characters
    """
    
    ROWS = 4
    COLS = 14
    MAX_PHRASE_LENGTH = 52
    
    def __init__(self, phrase: str):
        """
        Initialize the phrase board with a phrase.
        
        Args:
            phrase: A string up to 52 characters (letters, spaces, punctuation)
        """
        if len(phrase) > self.MAX_PHRASE_LENGTH:
            raise ValueError(f"Phrase cannot exceed {self.MAX_PHRASE_LENGTH} characters")
        
        self.phrase = phrase.upper()
        self.board = self._create_board()
    
    def _get_row_layout(self, row_index: int) -> tuple:
        """
        Get the starting column and max columns for a given row.
        
        Args:
            row_index: Row index (0-3)
            
        Returns:
            tuple: (start_col, num_cols) - start column index and number of columns available
        """
        if row_index == 0 or row_index == 3:  # First and fourth rows
            return (1, 12)  # Start at column 1 (0-indexed), 12 columns (2-13 in 1-indexed)
        else:  # Second and third rows
            return (0, 14)  # Start at column 0, all 14 columns available
    
    def _create_board(self) -> list:
        """
        Create the phrase board layout by placing words properly across rows.
        Centers the phrase both horizontally (per row) and vertically (across all rows).
        
        Returns:
            list: 4x14 2D array representing the phrase board
        """
        # Initialize empty board
        board = [[' ' for _ in range(self.COLS)] for _ in range(self.ROWS)]
        
        # Split phrase into words
        words = self.phrase.split()
        
        # First pass: distribute words across rows
        rows_content = []
        current_row_words = []
        current_row_length = 0
        
        for word_idx, word in enumerate(words):
            word_length = len(word)
            
            # Calculate length including space before word (except first word in row)
            needed_length = word_length
            if current_row_words:
                needed_length += 1  # Space before word
            
            # Determine max length for current row position
            row_num = len(rows_content)
            if row_num >= self.ROWS:
                raise ValueError("Phrase is too long to fit on the board")
            
            _, max_cols = self._get_row_layout(row_num)
            
            # Check if word fits on current row
            if current_row_length + needed_length <= max_cols:
                current_row_words.append(word)
                current_row_length += needed_length
            else:
                # Save current row and start new row
                if current_row_words:
                    rows_content.append(current_row_words)
                
                # Check if single word fits on new row
                row_num = len(rows_content)
                if row_num >= self.ROWS:
                    raise ValueError("Phrase is too long to fit on the board")
                
                _, max_cols = self._get_row_layout(row_num)
                if word_length > max_cols:
                    raise ValueError(f"Word '{word}' is too long to fit on a single row")
                
                current_row_words = [word]
                current_row_length = word_length
        
        # Don't forget the last row
        if current_row_words:
            rows_content.append(current_row_words)
        
        # Determine vertical centering: calculate starting row
        used_rows = len(rows_content)
        start_row = (self.ROWS - used_rows) // 2
        
        # Second pass: place words on board with horizontal centering per row
        for content_idx, row_words in enumerate(rows_content):
            actual_row = start_row + content_idx
            start_col, max_cols = self._get_row_layout(actual_row)
            
            # Build the row text with spaces between words
            row_text = ' '.join(row_words)
            text_length = len(row_text)
            
            # Calculate horizontal centering offset
            padding = (max_cols - text_length) // 2
            current_col = start_col + padding
            
            # Place characters on board
            for char in row_text:
                if current_col < start_col + max_cols:
                    board[actual_row][current_col] = char
                    current_col += 1
        
        return board
    
    def get_board(self) -> list:
        """
        Get the phrase board as a 2D array.
        
        Returns:
            list: 4x14 2D array representing the phrase board
        """
        return [row[:] for row in self.board]  # Return a copy
    
    def display(self):
        """
        Display the phrase board in a formatted way.
        """
        border = '+' + '-' * (self.COLS * 2 + 1) + '+'
        print(border)
        for row_idx, row in enumerate(self.board):
            row_str = '| '
            for col_idx, char in enumerate(row):
                # Show unavailable positions as grayed out
                start_col, max_cols = self._get_row_layout(row_idx)
                if col_idx < start_col or col_idx >= start_col + max_cols:
                    row_str += '  '  # Unavailable position
                else:
                    row_str += f'{char} '
            row_str += '|'
            print(row_str)
        print(border)
    
    def reveal_letter(self, letter: str) -> int:
        """
        Reveal all instances of a letter on the board.
        
        Args:
            letter: The letter to reveal
            
        Returns:
            int: Number of times the letter appears
        """
        letter = letter.upper()
        count = 0
        for row in self.board:
            count += row.count(letter)
        return count
    
    def __str__(self):
        """String representation of the board."""
        result = []
        for row in self.board:
            result.append(''.join(row))
        return '\n'.join(result)


# Example usage and testing
if __name__ == '__main__':
    # Test with a sample phrase
    phrase = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    
    print(f"Phrase: '{phrase}'")
    print(f"Phrase length: {len(phrase)} characters\n")
    
    board = WheelOfFortunePhraseBoard(phrase)
    
    print("Phrase Board Display:")
    board.display()
    
    print("\nBoard Array:")
    board_array = board.get_board()
    for i, row in enumerate(board_array):
        print(f"Row {i+1}: {row}")
    
    print("\n" + "="*50)
    
    # Test with another phrase
    phrase2 = "A FUN FAMILY GAME"
    print(f"\nPhrase: '{phrase2}'")
    print(f"Phrase length: {len(phrase2)} characters\n")
    
    board2 = WheelOfFortunePhraseBoard(phrase2)
    board2.display()
    
    print("\nBoard Array:")
    board_array2 = board2.get_board()
    for i, row in enumerate(board_array2):
        print(f"Row {i+1}: {row}")
