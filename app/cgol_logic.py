from typing import List, Tuple

GRID_WIDTH = 60
GRID_HEIGHT = 40
MAX_GENERATIONS = 1000

def word_to_binary(word: str) -> List[int]:
    """
    Convert a word into a binary list (0 = dead cell, 1 = live cell).
    Each character becomes 8 bits (ASCII).
    """
    binary_str = ''.join(format(ord(char), '08b') for char in word)
    return [int(bit) for bit in binary_str]


def create_seed_grid(word: str) -> List[List[int]]:
    """
    Create a 60x40 grid with the word's binary bits placed at the center.
    If the binary is too long, wrap to the next row.
    """
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    binary_list = word_to_binary(word)

    # Find starting row and column so it's centered
    start_row = GRID_HEIGHT // 2
    total_bits = len(binary_list)
    bits_per_row = GRID_WIDTH

    # Determine how many rows we need
    rows_needed = (total_bits + bits_per_row - 1) // bits_per_row

    # Shift starting row upwards so block is vertically centered
    start_row = (GRID_HEIGHT // 2) - (rows_needed // 2)

    index = 0
    for r in range(start_row, start_row + rows_needed):
        if r < 0 or r >= GRID_HEIGHT:
            break  # Avoid overflow vertically

        row_bits = binary_list[index:index + bits_per_row]
        index += len(row_bits)

        # Center horizontally
        start_col = (GRID_WIDTH - len(row_bits)) // 2
        for c, bit in enumerate(row_bits):
            grid[r][start_col + c] = bit

    return grid


def count_alive_neighbors(grid: List[List[int]], row: int, col: int) -> int:
    """Count the number of alive neighbors around a cell."""
    directions = [(-1,-1), (-1,0), (-1,1),
                  (0,-1),         (0,1),
                  (1,-1),  (1,0),  (1,1)]
    count = 0
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < GRID_HEIGHT and 0 <= c < GRID_WIDTH:
            count += grid[r][c]
    return count


def next_generation(grid: List[List[int]]) -> List[List[int]]:
    """Compute the next generation grid according to Conway's rules."""
    new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            alive_neighbors = count_alive_neighbors(grid, r, c)
            if grid[r][c] == 1:
                if alive_neighbors in (2, 3):
                    new_grid[r][c] = 1
            else:
                if alive_neighbors == 3:
                    new_grid[r][c] = 1
    return new_grid


def run_game_of_life(seed_word: str) -> Tuple[int, int]:
    """
    Run Conway's Game of Life starting with a seed word.
    Returns: (generations until stable, total cells spawned)
    """
    grid = create_seed_grid(seed_word)
    seen_states = set()
    total_alive_cells = sum(sum(row) for row in grid)

    generations = 0
    while generations < MAX_GENERATIONS:
        generations += 1

        # Store state for repetition detection
        state_tuple = tuple(tuple(row) for row in grid)
        if state_tuple in seen_states:
            break  # pattern repeated
        seen_states.add(state_tuple)

        new_grid = next_generation(grid)
        total_alive_cells += sum(sum(row) for row in new_grid if row.count(1) > 0)

        if new_grid == grid:
            break  # pattern stabilized
        if sum(sum(row) for row in new_grid) == 0:
            break  # extinction

        grid = new_grid

    return generations, total_alive_cells
