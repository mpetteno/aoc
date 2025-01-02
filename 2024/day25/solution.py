
def parse_input():
    schematics = open('input.txt').read().split('\n\n')
    locks = []
    keys = []
    for schematic in schematics:
        lines = schematic.split()
        pin_heights = tuple(col.count('#') - 1 for col in zip(*lines))
        (keys, locks)[lines[0] == '#####'].append(pin_heights)
    return locks, keys


if __name__ == "__main__":
    locks, keys = parse_input()
    valid_lock_key_pairs = []
    for lock in locks:
        for key in keys:
            zipped = list(zip(lock, key))
            if all(lp + kp <= len(zipped) for lp, kp in zipped):
                valid_lock_key_pairs.append((lock, key))
    print(f'Number of valid lock-key pairs: {len(valid_lock_key_pairs)}')
