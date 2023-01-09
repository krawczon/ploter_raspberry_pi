def reader(filename):
    data = []
    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        command = line.split()
        if len(command) > 0:
            if command[0] == 'M300':
                action = command[3].split(')')
                if action[0] == 'up' or action[0] == 'down':
                    data.append(action[0])
            elif command[0] == 'G1':
                if command[1][0] == 'X':
                    x = command[1].split('X')
                    pos_x = abs(float(x[1]))
                if command[2][0] == 'Y':
                    y = command[2].split('Y')
                    pos_y = abs(float(y[1]))
                data.append((pos_x, pos_y)) 

    return data
