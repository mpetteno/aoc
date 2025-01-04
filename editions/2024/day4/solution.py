def find_word(puzzle, target_word):
    def dfs(x, y, index, dx, dy):
        # If the index reaches the length of the word, it means we found the word
        if index == len(target_word):
            return True
        # Check boundaries and character match
        if not (0 <= x < R and 0 <= y < C) or puzzle[x][y] != target_word[index]:
            return False
        # Move to the next character in the current direction
        return dfs(x + dx, y + dy, index + 1, dx, dy)

    target_word = 'XMAS'
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
    R, C = len(puzzle), len(puzzle[0]) - 1
    for i in range(R):
        for j in range(C):
            char = lines[i][j]
            if char == target_word[0]:
                for h, v in search_directions:
                    if dfs(i, j, 0, h, v):
                        word_count += 1
    return word_count


def find_crossed_word(puzzle, target_word):

    def check_diagonal(x, y, dx, dy):
        forward_match, reversed_match = True, True
        for i in range(len(target_word)):
            nx, ny = x + i * dx, y + i * dy
            if not (0 <= nx < R and 0 <= ny < C):
                return False
            if puzzle[nx][ny] != target_word[i]:
                forward_match = False
            if puzzle[nx][ny] != target_word[len(target_word) - 1 - i]:
                reversed_match = False
        return forward_match or reversed_match

    crossed_word_count = 0
    R, C = len(puzzle), len(puzzle[0]) - 1
    middle_char_index = (len(target_word) - 1) // 2
    middle_char = target_word[middle_char_index]
    for i in range(R):
        for j in range(C):
            if puzzle[i][j] == middle_char:
                if (check_diagonal(i - middle_char_index, j - middle_char_index, 1, 1) and  # \ diagonal
                        check_diagonal(i - middle_char_index, j + middle_char_index, 1, -1)):  # / diagonal
                    crossed_word_count += 1
    return crossed_word_count


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.readlines()
        xmas_count = find_word(lines, 'XMAS')
        print(f'(Part 1) XMAS word count: {xmas_count}')
        crossed_mas_count = find_crossed_word(lines, 'MAS')
        print(f'(Part 2) X-MAS word count: {crossed_mas_count}')
