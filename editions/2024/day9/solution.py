import copy
from typing import Any

from solvers.python_solver import Solver


def compact_disk(unwrapped_disk_content, files, free_space):
    frag_disk_content = copy.deepcopy(unwrapped_disk_content)
    fb_idxs = [x for row in [list(range(s, e)) for s, e in files] for x in row]
    curr_block_pos = len(fb_idxs) - 1
    fs_idxs = [x for row in [list(range(s, e)) for s, e in free_space] for x in row]
    curr_free_space_pos = 0
    while fs_idxs[curr_free_space_pos] < fb_idxs[curr_block_pos]:
        frag_disk_content[fs_idxs[curr_free_space_pos]] = frag_disk_content[fb_idxs[curr_block_pos]]
        frag_disk_content[fb_idxs[curr_block_pos]] = -1
        curr_free_space_pos += 1
        curr_block_pos -= 1
    return sum([i * x for i, x in enumerate(frag_disk_content) if x != -1])


def defrag_disk(unwrapped_disk_content, files, free_space):
    defrag_disk_content = copy.deepcopy(unwrapped_disk_content)
    for file_id in range(len(files) - 1, -1, -1):
        file_start_idx, file_end_idx = files[file_id]
        curr_file_size = file_end_idx - file_start_idx
        for j in range(len(free_space)):
            fs_start_idx, fs_end_idx = free_space[j]
            curr_free_space_size = fs_end_idx - fs_start_idx
            if curr_free_space_size >= curr_file_size and fs_start_idx < file_start_idx:
                for k in range(fs_start_idx, fs_start_idx + curr_file_size):
                    defrag_disk_content[k] = file_id
                defrag_disk_content[file_start_idx:file_end_idx] = [-1] * curr_file_size
                if curr_free_space_size > curr_file_size:
                    free_space[j] = fs_start_idx + curr_file_size, fs_end_idx
                else:
                    free_space.pop(j)
                break
    return sum([i * x for i, x in enumerate(defrag_disk_content) if x != -1])


class Solution(Solver):

    def parse_input(self) -> Any:
        disk_content = self.input_data.strip()
        unwrapped = []
        f = []
        fs = []
        for i, char in enumerate(disk_content):
            n = int(char)
            start_idx = len(unwrapped)
            end_idx = start_idx + n
            if i % 2 == 0:
                f_id = i // 2
                f.append((start_idx, end_idx))
                unwrapped.extend([f_id for _ in range(n)])
            else:
                fs.append((start_idx, end_idx))
                unwrapped.extend([-1 for _ in range(n)])
        return unwrapped, f, fs

    def solve_first_part(self, parsed_input: Any) -> str:
        unwrapped_disk_content, files, free_space = parsed_input
        compacted_disk_checksum = compact_disk(unwrapped_disk_content, files, free_space)
        return f'Compacted disk checksum {compacted_disk_checksum}'

    def solve_second_part(self, parsed_input: Any) -> str:
        unwrapped_disk_content, files, free_space = parsed_input
        defrag_disk_checksum = defrag_disk(unwrapped_disk_content, files, free_space)
        return f'De-fragmented disk checksum {defrag_disk_checksum}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
