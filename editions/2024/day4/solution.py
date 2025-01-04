from typing import Any

from solvers.python_solver import Solver


def find_word(puzzle, target_word):

    def dfs(x, y, index, dx, dy):
        if index == len(target_word):
            return True
        if not (0 <= x < rows and 0 <= y < cols) or puzzle[x][y] != target_word[index]:
            return False
        return dfs(x + dx, y + dy, index + 1, dx, dy)

    search_directions = [
        (0, 1),  # Right
        (1, 0),  # Down
        (0, -1),  # Left
        (-1, 0),  # Up
        (1, 1),  # Down-right diagonal
        (1, -1),  # Down-left diagonal
        (-1, 1),  # Up-right diagonal
        (-1, -1)  # Up-left diagonal
    ]
    word_count = 0
    rows, cols = len(puzzle), len(puzzle[0])
    for i in range(rows):
        for j in range(cols):
            char = puzzle[i][j]
            if char == target_word[0]:
                for h, v in search_directions:
                    if dfs(i, j, 0, h, v):
                        word_count += 1
    return word_count


def find_crossed_word(puzzle, target_word):

    def check_diagonal(x, y, dx, dy):
        forward_match, reversed_match = True, True
        for k in range(len(target_word)):
            nx, ny = x + k * dx, y + k * dy
            if not (0 <= nx < rows and 0 <= ny < cols):
                return False
            if puzzle[nx][ny] != target_word[k]:
                forward_match = False
            if puzzle[nx][ny] != target_word[len(target_word) - 1 - k]:
                reversed_match = False
        return forward_match or reversed_match

    crossed_word_count = 0
    rows, cols = len(puzzle), len(puzzle[0])
    middle_char_index = (len(target_word) - 1) // 2
    middle_char = target_word[middle_char_index]
    for i in range(rows):
        for j in range(cols):
            if puzzle[i][j] == middle_char:
                if (check_diagonal(i - middle_char_index, j - middle_char_index, 1, 1) and  # \ diagonal
                        check_diagonal(i - middle_char_index, j + middle_char_index, 1, -1)):  # / diagonal
                    crossed_word_count += 1
    return crossed_word_count


class Solution(Solver):

    def parse_input(self) -> Any:
        return self.input_data.splitlines()

    def solve_first_part(self, parsed_input: Any) -> str:
        xmas_count = find_word(parsed_input, 'XMAS')
        return f'XMAS word count: {xmas_count}'

    def solve_second_part(self, parsed_input: Any) -> str:
        crossed_mas_count = find_crossed_word(parsed_input, 'MAS')
        return f'X-MAS word count: {crossed_mas_count}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
