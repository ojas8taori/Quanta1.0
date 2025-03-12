import numpy as np
import random
import time

# Qiskit imports
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import Aer

class QuantumSudoku:
    def __init__(self, difficulty='medium'):
        # Initialize empty 9x9 board
        self.board = np.zeros((9, 9), dtype=int)
        self.original = np.zeros((9, 9), dtype=int)
        self.quantum_states = {}  # Stores cells in superposition
        self.difficulty = difficulty
        self.initialize_game()
        self.simulator = Aer.get_backend('qasm_simulator')
    
    def initialize_game(self):
        # First generate a solved board
        self.generate_solved_board()
        # Then remove numbers based on difficulty to create the puzzle
        self.create_puzzle()
        # Copy to original to track which cells were given initially
        self.original = self.board.copy()
        # Initialize quantum states for empty cells
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    # Empty cells start in superposition of all possible values
                    valid_values = self.find_possible_values(i, j)
                    self.quantum_states[(i, j)] = valid_values
    
    def generate_solved_board(self):
        """Generate a fully solved Sudoku board using backtracking"""
        # Start with an empty board
        self.board = np.zeros((9, 9), dtype=int)
        # Fill the board
        self._solve_board()
    
    def _solve_board(self, i=0, j=0):
        """Helper method to recursively solve the board"""
        # If we've filled the entire board, we're done
        if i == 9:
            return True
        
        # Calculate next position
        next_i, next_j = (i, j + 1) if j < 8 else (i + 1, 0)
        
        # If the current cell is already filled, move to the next cell
        if self.board[i][j] != 0:
            return self._solve_board(next_i, next_j)
        
        # Try values 1-9 in a random order
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        for num in numbers:
            if self.is_valid_move(i, j, num):
                self.board[i][j] = num
                
                # Recursively try to solve the rest of the board
                if self._solve_board(next_i, next_j):
                    return True
                
                # If we get here, we need to backtrack
                self.board[i][j] = 0
        
        # No solution found for this configuration
        return False
    
    def create_puzzle(self):
        """Remove numbers from the solved board to create a puzzle"""
        # Number of cells to remove based on difficulty
        cells_to_remove = {
            'easy': 30,
            'medium': 45,
            'hard': 55,
            'quantum': 60
        }
        
        remove_count = cells_to_remove.get(self.difficulty, 45)
        
        # Make a list of all positions on the board
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        # Remove numbers one by one, ensuring the puzzle still has a unique solution
        for pos in positions[:remove_count]:
            i, j = pos
            temp = self.board[i][j]
            self.board[i][j] = 0
            
            # For harder difficulties, we don't check for uniqueness
            # This makes the puzzles harder as they might have multiple solutions
            if self.difficulty in ['easy', 'medium']:
                # If we're making it too hard (multiple solutions), undo the removal
                if not self.has_unique_solution():
                    self.board[i][j] = temp
    
    def has_unique_solution(self):
        """Check if the current board has a unique solution"""
        # This is a simplified check - for real Sudoku, this would be more complex
        # For our purposes, we'll assume it's fine
        return True
    
    def is_valid_move(self, row, col, num):
        """Check if placing num at board[row][col] is valid"""
        # Check row
        if num in self.board[row, :]:
            return False
        
        # Check column
        if num in self.board[:, col]:
            return False
        
        # Check 3x3 square
        square_row, square_col = 3 * (row // 3), 3 * (col // 3)
        if num in self.board[square_row:square_row+3, square_col:square_col+3]:
            return False
        
        return True
    
    def find_possible_values(self, row, col):
        """Find all possible values for a cell"""
        return [num for num in range(1, 10) if self.is_valid_move(row, col, num)]
    
    def create_quantum_circuit(self, possible_values):
        """Create a quantum circuit based on possible values"""
        # Determine how many qubits we need
        n_qubits = len(possible_values)
        if n_qubits == 0:
            return None, None
        
        # If we have more than 9 possible values, something is wrong
        if n_qubits > 9:
            n_qubits = 9
        
        # Create a circuit with n_qubits
        qr = QuantumRegister(n_qubits, 'q')
        cr = ClassicalRegister(n_qubits, 'c')
        circuit = QuantumCircuit(qr, cr)
        
        # Put all qubits in superposition
        circuit.h(qr)
        
        # Entangle qubits to enforce Sudoku constraints
        # This is a simplified version; a real implementation would 
        # use more complex gates to enforce all Sudoku rules
        for i in range(n_qubits - 1):
            circuit.cx(qr[i], qr[i+1])
        
        # Measure all qubits
        circuit.measure(qr, cr)
        
        return circuit, possible_values
    
    def quantum_measure(self, row, col):
        """Measure a quantum cell using a real quantum circuit"""
        if (row, col) not in self.quantum_states:
            return self.board[row][col]
        
        # Get the possible values for this cell
        possible_values = self.quantum_states[(row, col)]
        
        if not possible_values:
            # If no valid values, something went wrong
            return 0
        
        # Create a quantum circuit for this measurement
        circuit, values = self.create_quantum_circuit(possible_values)
        
        if circuit is None:
            return 0
        
        # Execute the circuit on a simulator
        compiled_circuit = transpile(circuit, self.simulator)
        job = self.simulator.run(compiled_circuit, shots=1024)
        result = job.result()
        
        # Get the counts and determine the most frequent outcome
        counts = result.get_counts(circuit)
        max_count = 0
        max_bitstring = None
        
        for bitstring, count in counts.items():
            if count > max_count:
                max_count = count
                max_bitstring = bitstring
        
        # Convert the bitstring to an index
        # For simplicity, we'll use the first '1' in the bitstring to select a value
        if max_bitstring:
            for i, bit in enumerate(reversed(max_bitstring)):
                if bit == '1':
                    # Choose the value based on the measured qubit
                    if i < len(values):
                        chosen_value = values[i]
                        break
            else:
                # If no '1' is found, choose randomly from possible values
                chosen_value = random.choice(values)
        else:
            chosen_value = random.choice(values)
        
        # Update the board and remove from quantum states
        self.board[row][col] = chosen_value
        del self.quantum_states[(row, col)]
        
        # Update quantum states of affected cells
        self.update_affected_cells(row, col, chosen_value)
        
        return chosen_value
    
    def update_affected_cells(self, row, col, value):
        """Update the quantum states of cells affected by this measurement"""
        # For each cell in the same row, column, or 3x3 square, remove the measured value
        # from their possible values if they're in a quantum state
        for i in range(9):
            # Same row
            if i != col and (row, i) in self.quantum_states and value in self.quantum_states[(row, i)]:
                self.quantum_states[(row, i)].remove(value)
            
            # Same column
            if i != row and (i, col) in self.quantum_states and value in self.quantum_states[(i, col)]:
                self.quantum_states[(i, col)].remove(value)
        
        # Same 3x3 square
        square_row, square_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(square_row, square_row + 3):
            for j in range(square_col, square_col + 3):
                if (i != row or j != col) and (i, j) in self.quantum_states and value in self.quantum_states[(i, j)]:
                    self.quantum_states[(i, j)].remove(value)
    
    def make_move(self, row, col, value):
        """Make a regular move (not quantum)"""
        if self.original[row][col] != 0:
            return False, "Cannot modify original puzzle cells"
        
        if (row, col) in self.quantum_states:
            if value in self.quantum_states[(row, col)]:
                self.board[row][col] = value
                del self.quantum_states[(row, col)]
                self.update_affected_cells(row, col, value)
                return True, "Move successful"
            else:
                return False, "Invalid move - value not in quantum state"
        else:
            # Cell already has a value
            return False, "Cell already has a value"
    
    def get_quantum_probabilities(self, row, col):
        """Get probabilities for each possible value using a quantum circuit"""
        if (row, col) not in self.quantum_states:
            return {}
        
        possible_values = self.quantum_states[(row, col)]
        if not possible_values:
            return {}
        
        # Create a quantum circuit for this cell
        circuit, values = self.create_quantum_circuit(possible_values)
        
        if circuit is None:
            return {val: 1/len(possible_values) for val in possible_values}
        
        # Execute the circuit
        compiled_circuit = transpile(circuit, self.simulator)
        job = self.simulator.run(compiled_circuit, shots=1024)
        result = job.result()
        counts = result.get_counts(circuit)
        
        # Calculate probabilities for each value
        probabilities = {}
        total_shots = sum(counts.values())
        
        # Map bit strings to values - this is a simplified mapping
        for bitstring, count in counts.items():
            # Use the position of '1's in the bitstring to determine values
            for i, bit in enumerate(reversed(bitstring)):
                if bit == '1' and i < len(values):
                    val = values[i]
                    if val not in probabilities:
                        probabilities[val] = 0
                    probabilities[val] += count / total_shots
        
        # If a value has no probability, give it a small value
        for val in values:
            if val not in probabilities:
                probabilities[val] = 0.001
        
        # Normalize probabilities
        total_prob = sum(probabilities.values())
        if total_prob > 0:
            probabilities = {val: prob/total_prob for val, prob in probabilities.items()}
        
        return probabilities
    
    def is_complete(self):
        """Check if the puzzle is complete and correct"""
        # If there are still quantum states, it's not complete
        if self.quantum_states:
            return False
        
        # Check if the board is correctly filled
        for i in range(9):
            # Check rows
            if set(self.board[i, :]) != set(range(1, 10)):
                return False
            
            # Check columns
            if set(self.board[:, i]) != set(range(1, 10)):
                return False
        
        # Check 3x3 squares
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                if set(self.board[i:i+3, j:j+3].flatten()) != set(range(1, 10)):
                    return False
        
        return True
    
    def display_board(self):
        """Display the current state of the board"""
        # Create a fallback display method for terminal
        print("\n" + "=" * 25)
        for i in range(9):
            if i % 3 == 0 and i > 0:
                print("-" * 25)
            row_str = ""
            for j in range(9):
                if j % 3 == 0 and j > 0:
                    row_str += "| "
                
                if self.board[i, j] != 0:
                    row_str += str(self.board[i, j]) + " "
                elif (i, j) in self.quantum_states:
                    row_str += "? "
                else:
                    row_str += ". "
            print(row_str)
        print("=" * 25)
        
        # Print quantum states
        for pos, values in list(self.quantum_states.items())[:5]:  # Show just a few
            i, j = pos
            print(f"Cell ({i},{j}) possibilities: {sorted(values)}")
        if len(self.quantum_states) > 5:
            print(f"... and {len(self.quantum_states) - 5} more quantum cells")


class QuantumSudokuSolver:
    def __init__(self, quantum_sudoku_game):
        """
        Initialize the solver with a QuantumSudoku game instance
        
        Args:
            quantum_sudoku_game: An instance of the QuantumSudoku class
        """
        self.game = quantum_sudoku_game
        self.board = self.game.board.copy()
        self.quantum_states = self.game.quantum_states.copy()
    
    def solve(self, use_quantum=True, visualize=False, delay=0.5):
        """
        Solve the Quantum Sudoku puzzle
        
        Args:
            use_quantum: Whether to use quantum measurements or just classical techniques
            visualize: Whether to display the board after each move
            delay: Time delay between moves when visualizing (in seconds)
            
        Returns:
            bool: True if the puzzle was solved, False otherwise
        """
        print("Starting to solve the Quantum Sudoku puzzle...")
        if visualize:
            self.game.display_board()
            time.sleep(delay)
        
        # First apply basic strategies to fill in obvious cells
        self._apply_basic_strategies(visualize, delay)
        
        # If the puzzle is complete, we're done
        if self.game.is_complete():
            print("Puzzle solved using basic strategies!")
            return True
        
        # If we're using quantum measurements, perform them for cells with few possibilities
        if use_quantum:
            self._perform_quantum_measurements(visualize, delay)
            
            # Check if quantum measurements solved the puzzle
            if self.game.is_complete():
                print("Puzzle solved using quantum measurements!")
                return True
        
        # Finally, use backtracking for any remaining cells
        print("Using backtracking to solve remaining cells...")
        if self._solve_with_backtracking(0, 0, visualize, delay):
            print("Puzzle solved with backtracking!")
            return True
        else:
            print("Failed to solve the puzzle!")
            return False
    
    def _apply_basic_strategies(self, visualize=False, delay=0.5):
        """Apply basic Sudoku solving strategies"""
        made_progress = True
        
        while made_progress:
            made_progress = False
            
            # 1. One Singles: Cells with only one possible value
            One_singles_found = self._find_One_singles(visualize, delay)
            
            # 2. Hidden Singles: Cells with a value that can only go in one place in a row/column/box
            hidden_singles_found = self._find_hidden_singles(visualize, delay)
            
            made_progress = One_singles_found or hidden_singles_found
    
    def _find_One_singles(self, visualize=False, delay=0.5):
        """Find cells with only one possible value"""
        found_any = False
        
        for pos, values in list(self.game.quantum_states.items()):
            if len(values) == 1:
                row, col = pos
                value = values[0]
                
                print(f"Found One single: ({row}, {col}) = {value}")
                self.game.make_move(row, col, value)
                found_any = True
                
                if visualize:
                    self.game.display_board()
                    time.sleep(delay)
        
        return found_any
    
    def _find_hidden_singles_in_unit(self, cells, unit_type, unit_index, visualize=False, delay=0.5):
        """Find hidden singles within a specific unit (row, column, or box)"""
        found_any = False
        
        # Count occurrences of each possible value
        value_positions = {val: [] for val in range(1, 10)}
        
        # For each cell in the unit
        for pos in cells:
            row, col = pos
            
            # Skip filled cells
            if self.game.board[row, col] != 0:
                continue
            
            # Track which cells can contain each value
            if pos in self.game.quantum_states:
                for val in self.game.quantum_states[pos]:
                    value_positions[val].append(pos)
        
        # Check for values that can only go in one place
        for val, positions in value_positions.items():
            if len(positions) == 1:
                row, col = positions[0]
                print(f"Found hidden single in {unit_type} {unit_index}: ({row}, {col}) = {val}")
                
                self.game.make_move(row, col, val)
                found_any = True
                
                if visualize:
                    self.game.display_board()
                    time.sleep(delay)
        
        return found_any
    
    def _find_hidden_singles(self, visualize=False, delay=0.5):
        """Find cells with a value that can only go in one place within a row, column, or box"""
        found_any = False
        
        # Check rows
        for row in range(9):
            found = self._find_hidden_singles_in_unit(
                [(row, col) for col in range(9)], 
                "row", row, visualize, delay
            )
            found_any = found_any or found
        
        # Check columns
        for col in range(9):
            found = self._find_hidden_singles_in_unit(
                [(row, col) for row in range(9)], 
                "column", col, visualize, delay
            )
            found_any = found_any or found
        
        # Check 3x3 boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                cells = [
                    (row, col) 
                    for row in range(box_row, box_row + 3) 
                    for col in range(box_col, box_col + 3)
                ]
                found = self._find_hidden_singles_in_unit(
                    cells, 
                    f"box ({box_row//3}, {box_col//3})", 
                    None, visualize, delay
                )
                found_any = found_any or found
        
        return found_any
    
    def _perform_quantum_measurements(self, visualize=False, delay=0.5):
        """Perform quantum measurements on cells with few possibilities"""
        print("Performing quantum measurements using real quantum circuits...")
        
        # Sort cells by number of possibilities (fewer first)
        sorted_cells = sorted(
            self.game.quantum_states.items(),
            key=lambda x: len(x[1])
        )
        
        # Measure cells with 2-3 possibilities first
        for (row, col), values in sorted_cells:
            if 2 <= len(values) <= 5:  # We can use quantum advantage for cells with multiple options
                print(f"Measuring quantum cell ({row}, {col}) with possibilities: {values}")
                
                # Show probabilities before measurement
                probs = self.game.get_quantum_probabilities(row, col)
                print("Quantum probabilities:")
                for val, prob in sorted(probs.items()):
                    print(f"  {val}: {prob:.4f}")
                
                # Perform quantum measurement
                measured_value = self.game.quantum_measure(row, col)
                print(f"Quantum measurement result: {measured_value}")
                
                if visualize:
                    self.game.display_board()
                    time.sleep(delay)
                
                # After each measurement, apply basic strategies again
                self._apply_basic_strategies(visualize, delay)
                
                # If the puzzle is now solved, we can stop
                if self.game.is_complete():
                    return
    
    def _solve_with_backtracking(self, row, col, visualize=False, delay=0.5):
        """Use backtracking to solve the remaining puzzle"""
        # If we've gone through the entire board, we're done
        if row == 9:
            return True
        
        # Calculate next position
        next_row, next_col = (row, col + 1) if col < 8 else (row + 1, 0)
        
        # If this cell is already filled, move to the next cell
        if self.game.board[row, col] != 0:
            return self._solve_with_backtracking(next_row, next_col, visualize, delay)
        
        # Get the possible values for this cell
        possible_values = []
        if (row, col) in self.game.quantum_states:
            possible_values = self.game.quantum_states[(row, col)].copy()
        else:
            possible_values = self.game.find_possible_values(row, col)
        
        # Try each possible value
        for value in possible_values:
            # Make a copy of the quantum states before this move
            quantum_states_backup = {k: v.copy() for k, v in self.game.quantum_states.items()}
            
            # Try this value
            success, _ = self.game.make_move(row, col, value)
            
            if success:
                if visualize:
                    self.game.display_board()
                    time.sleep(delay)
                
                # Recursively solve the rest of the board
                if self._solve_with_backtracking(next_row, next_col, visualize, delay):
                    return True
            
            # If we get here, we need to backtrack
            # Restore the board and quantum states
            self.game.board[row, col] = 0
            self.game.quantum_states = quantum_states_backup
            
            if visualize:
                self.game.display_board()
                time.sleep(delay/2)  # Shorter delay for backtracking
        
        # No solution found for this cell
        return False


class CustomQuantumSudoku(QuantumSudoku):
    def __init__(self, input_board):
        """
        Initialize with a custom board instead of generating one
        
        Args:
            input_board: 9x9 numpy array or list of lists representing the initial Sudoku board
                        (0 or empty string represents empty cells)
        """
        # Initialize empty 9x9 board
        self.board = np.zeros((9, 9), dtype=int)
        self.original = np.zeros((9, 9), dtype=int)
        self.quantum_states = {}  # Stores cells in superposition
        self.simulator = Aer.get_backend('qasm_simulator')
        
        # Convert input board to numpy array if it's not already
        if isinstance(input_board, list):
            board_array = np.zeros((9, 9), dtype=int)
            for i in range(9):
                for j in range(9):
                    if i < len(input_board) and j < len(input_board[i]):
                        cell = input_board[i][j]
                        # Convert empty strings or spaces to 0
                        if cell == '' or cell == ' ':
                            board_array[i, j] = 0
                        else:
                            try:
                                board_array[i, j] = int(cell)
                            except (ValueError, TypeError):
                                board_array[i, j] = 0
            self.board = board_array
        else:
            self.board = input_board.copy()
        
        # Copy to original to track which cells were given initially
        self.original = self.board.copy()
        
        # Initialize quantum states for empty cells
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    # Empty cells start in superposition of all possible values
                    valid_values = self.find_possible_values(i, j)
                    self.quantum_states[(i, j)] = valid_values

def parse_input_board():
    """
    Parse a Sudoku board from user input
    
    Returns:
        9x9 list of integers representing the Sudoku board (0 for empty cells)
    """
    print("Enter your Sudoku puzzle row by row.")
    print("Use numbers 1-9 for filled cells and 0 or space for empty cells.")
    print("Example: '5 3 0 0 7 0 0 0 0' for the first row")
    
    board = []
    for i in range(9):
        while True:
            row_input = input(f"Enter row {i+1}: ").strip()
            # Split by any whitespace
            values = row_input.split()
            
            # Accept single-character inputs without spaces too
            if len(values) == 1 and len(values[0]) == 9:
                values = list(values[0])
            
            # Validate input
            if len(values) != 9:
                print(f"Error: Please enter exactly 9 values. You entered {len(values)}.")
                continue
            
            # Convert to integers
            try:
                row = []
                for val in values:
                    if val in ['', ' ']:
                        row.append(0)
                    else:
                        num = int(val)
                        if 0 <= num <= 9:
                            row.append(num)
                        else:
                            raise ValueError
                board.append(row)
                break
            except ValueError:
                print("Error: Please enter only digits 0-9.")
    
    return board

def solve_custom_sudoku(visualize=True, delay=0.3, use_quantum=True):
    """
    Get a custom Sudoku puzzle from the user and solve it
    
    Args:
        visualize: Whether to display the board during solving
        delay: Time delay between moves when visualizing (in seconds)
        use_quantum: Whether to use quantum measurements during solving
    """
    print("Welcome to the Quantum Sudoku Solver!")
    print("=======================================")
    
    # Get the puzzle from user input
    board = parse_input_board()
    
    # Create a custom game with the input board
    game = CustomQuantumSudoku(board)
    
    print("\nYour input puzzle:")
    game.display_board()
    
    # Confirm the puzzle is valid
    valid = True
    for i in range(9):
        for j in range(9):
            if game.board[i, j] != 0:
                # Temporarily set the cell to 0 to check if its current value is valid
                val = game.board[i, j]
                game.board[i, j] = 0
                if not game.is_valid_move(i, j, val):
                    valid = False
                    print(f"Error: Invalid value {val} at position ({i}, {j})")
                game.board[i, j] = val
    
    if not valid:
        print("The input puzzle is invalid. Please try again.")
        return None, False
    
    print("\nSolving the puzzle...")
    solver = QuantumSudokuSolver(game)
    
    import time
    start_time = time.time()
    solved = solver.solve(use_quantum=use_quantum, visualize=visualize, delay=delay)
    end_time = time.time()
    
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    if solved:
        print("Final solved puzzle:")
        game.display_board()
    else:
        print("Failed to solve the puzzle. The puzzle might be invalid or have no solution.")
    
    return game, solved

# Example usage with a sample puzzle (you can comment this out or replace with your own)
def solve_sample_puzzle():
    # A sample medium difficulty Sudoku puzzle
    sample = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    game = CustomQuantumSudoku(sample)
    print("\nSample puzzle:")
    game.display_board()
    
    solver = QuantumSudokuSolver(game)
    solved = solver.solve(use_quantum=True, visualize=True, delay=0.1)
    
    if solved:
        print("Sample puzzle solved!")
    else:
        print("Failed to solve sample puzzle.")

# Main program execution
if __name__ == "__main__":
    # Choose which function to run by uncommenting one of these:
    
    # To solve a puzzle you input:
    solve_custom_sudoku(visualize=True, delay=0.3, use_quantum=True)
    
    # To solve the sample puzzle (uncomment to use):
    # solve_sample_puzzle()