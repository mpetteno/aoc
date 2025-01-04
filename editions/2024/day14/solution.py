
def parse_input():
    robots = open("input.txt").readlines()
    positions = []
    velocities = []
    for robot in robots:
        p, v = robot.split(" ")
        col, row = p.split("=")[1].split(",")
        positions.append((int(row), int(col)))
        v_col, v_row = v.split("=")[1].split(",")
        velocities.append((int(v_row), int(v_col)))
    return positions, velocities


def get_quadrant(x, y):
    if x == MID_ROW or y == MID_COL:
        return -1
    if x < MID_ROW and y < MID_COL:
        return 0
    elif x < MID_ROW and y > MID_COL:
        return 1
    elif x > MID_ROW and y < MID_COL:
        return 2
    else:
        return 3


def move_robot(steps, robot_pos, robot_vel):
    p_row, p_col = robot_pos
    vel_row, vel_col = robot_vel
    new_pos_row = (p_row + vel_row * steps) % AREA_ROWS
    new_pos_col = (p_col + vel_col * steps) % AREA_COLS
    return new_pos_row, new_pos_col


def get_safety_factor(q_count):
    score = q_count[0]
    for c in q_count[1:]:
        score *= c
    return score


def check_aligned_robots(area, min_count, horizontal: bool = True):
    a = AREA_ROWS if horizontal else AREA_COLS
    b = AREA_COLS if horizontal else AREA_ROWS
    for i in range(a):
        count = 0
        for j in range(b):
            if (horizontal and area[i][j] == 1) or (not horizontal and area[j][i] == 1):
                count += 1
                if count >= min_count:
                    return True
            else:
                count = 0
    return False


if __name__ == "__main__":
    AREA_COLS = 101
    AREA_ROWS = 103
    TIME_STEPS = 100
    MID_ROW, MID_COL = AREA_ROWS // 2, AREA_COLS // 2
    robots_init_pos, robots_vel = parse_input()
    quadrants_count = [0] * 4
    for i in range(len(robots_init_pos)):
        final_pos_row, final_pos_col = move_robot(TIME_STEPS, robots_init_pos[i], robots_vel[i])
        quadrant = get_quadrant(final_pos_row, final_pos_col)
        if quadrant != -1:
            quadrants_count[quadrant] += 1
    safety_factor = get_safety_factor(quadrants_count)
    print(f'(Part 1) Safety factor: {safety_factor}')
    area_map = [[0] * AREA_COLS for _ in range(AREA_ROWS)]
    MIN_ALIGNED_ROBOTS = 10
    timesteps_count = 0
    while True:
        # Move each robot for a single time step
        timesteps_count += 1
        for k in range(len(robots_init_pos)):
            curr_pos_x, curr_pos_y = robots_init_pos[k]
            final_pos_row, final_pos_col = move_robot(1, robots_init_pos[k], robots_vel[k])
            area_map[curr_pos_x][curr_pos_y] = 0
            robots_init_pos[k] = final_pos_row, final_pos_col
            area_map[final_pos_row][final_pos_col] = 1
        # Check for aligned robots
        if (check_aligned_robots(area_map, min_count=MIN_ALIGNED_ROBOTS)
                or check_aligned_robots(area_map, min_count=MIN_ALIGNED_ROBOTS, horizontal=False)):
            break
    print(f'(Part 2) XMas tree timesteps: {timesteps_count}')
