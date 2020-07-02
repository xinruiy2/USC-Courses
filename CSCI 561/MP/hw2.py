import os
import heapq
import copy
import random



def little_go():
    try:
        os.remove("output.txt")
    except OSError:
        pass

    f = open("input.txt", "r")
    f_1 = open("output.txt", "w")
    count = 0
    color = -1
    start = True
    black_num = 0
    white_num = 0
    curr_step = 0
    new_move = [] #last move
    cap_moves = [] #my captured moves

    previous_board = []
    current_board = []
    for line in f:
        line = line.strip()
        if count == 0:
            color = line[0]
        elif count < 6:
            previous_board.append([])
            for char in line:
                previous_board[-1].append(char)
        else:
            current_board.append([])
            for char in line:
                current_board[-1].append(char)
                if char == '1':
                    start = False
                    white_num += 1
                elif char == '2':
                    start = False
                    black_num += 1
            if len(new_move) == 0:
                for i in range(5):
                    if previous_board[count - 6][i] == '0' and current_board[count - 6][i] != '0':
                        new_move = [count-6, i]
        count += 1
    #function finds the best next_move
    if start:
        try:
            os.remove("step.txt")
        except OSError:
            pass
        f_step = open("step.txt", "w")
        f_step.write(str(1))
        f_step.close()
        f_1.write(str(2) + "," + str(2))
        f_1.close()
    else:
        if max(white_num, black_num) == 1 and color == "2":
            try:
                os.remove("step.txt")
            except OSError:
                pass
            f_step = open("step.txt", "w")
            f_step.write(str(1))
            f_step.close()
            curr_step = 1
        else:
            f_step = open("step.txt", "r")
            for line in f_step:
                curr_step = int(line) + 1
            try:
                os.remove("step.txt")
            except OSError:
                pass
            f_step = open("step.txt", "w")
            f_step.write(str(curr_step))
            f_step.close()

        if color == '2':
            next_move = find_best_move_1(previous_board, current_board, color, new_move, 5, color,curr_step)
        else:
            next_move = find_best_move(previous_board, current_board, color, new_move, 5, color,curr_step)
        if len(next_move) == 0:
            f_1.write("PASS")
        else:
            f_1.write(str(next_move[0]) + "," + str(next_move[1]))
        f_1.close()

def diff(board, color):
    diff_val = 0
    for i in range(5):
        for j in range(5):
            if board[i][j] == color:
                diff_val += 1
            elif board[i][j] != '0':
                diff_val -= 1
    return diff_val


def find_eye(board,color):
    eyeScore = 0
    for i in range(5):
        for j in range(5):
            if board[i][j] == '0':
                IfMyEye = 1
                IfOpEye = -1
                for a, b in ((i+1,j),(i-1,j),(i,j+1),(i,j-1)):
                    if 0 <= a < 5 and 0 <= b <5:
                        if board[a][b] == '0':
                            IfMyEye = 0
                            IfOpEye = 0
                            break
                        elif board[a][b] == color:
                            IfOpEye = 0
                        else:
                            IfMyEye = 0
                eyeScore += IfOpEye + IfMyEye
    return eyeScore



def find_best_move(prev, curr, color, new_move, depth, my_color, early_move = -1):
    #base case
    if depth == 1:
        if color == '1':
            limit = 4
        else:
            limit = 3
        if early_move != -1 and early_move <= limit:
            valid_move, capture_dict = check_valid_move(prev,curr,color,new_move, True)
        else:
            valid_move, capture_dict = check_valid_move(prev,curr,color,new_move)
        if len(valid_move) >= 5:
            valid_move = heapq.nlargest(5,valid_move)
        if len(valid_move) == 0:
            return diff(curr, my_color)
        else:
            if color == '1' and early_move == 12:
                max = -12
                for move in valid_move:
                    x = move[1][0]
                    y = move[1][1]
                    new_curr = copy.deepcopy(curr)
                    new_curr[x][y] = color
                    if (x,y) in capture_dict:
                        for cap_move in capture_dict[(x,y)]:
                            new_curr[cap_move[0]][cap_move[1]] = '0'
                    valid_move_last, capture_dict_last = check_valid_move(curr, new_curr, '2', [x,y])
                    min = 12
                    if len(valid_move_last) == 0:
                        if diff(new_curr,my_color) < min:
                            min = diff(new_curr,my_color)
                    for little_move in valid_move_last:
                        x_1 = little_move[1][0]
                        y_1 = little_move[1][1]
                        if (x_1,y_1) not in capture_dict_last:
                            cur_min = diff(new_curr,my_color) - 1
                            if cur_min < min:
                                min = cur_min
                        else:
                            cur_min = diff(new_curr,my_color) - 1 - len(capture_dict_last[(x_1,y_1)])
                            if cur_min < min:
                                min = cur_min
                    if min > max:
                        max = min
                return max

            else:
                max = -12
                eye_score = 0
                for move in valid_move:
                    x = move[1][0]
                    y = move[1][1]
                    if (x,y) not in capture_dict:
                        curr_max = 0
                        if early_move >= 12:
                            curr_max = diff(curr,my_color) + 1
                        else:
                            new_curr = copy.deepcopy(curr)
                            new_curr[x][y] = color
                            curr_max = diff(curr,my_color) + 1 + find_eye(new_curr,my_color)
                        if curr_max > max:
                            max = curr_max
                    else:
                        curr_max = 0
                        if early_move >= 12:
                            curr_max = diff(curr,my_color) + 1 + len(capture_dict[(x,y)])
                        else:
                            new_curr = copy.deepcopy(curr)
                            new_curr[x][y] = color
                            for cap_move in capture_dict[(x,y)]:
                                new_curr[cap_move[0]][cap_move[1]] = '0'
                            curr_max = diff(curr,my_color) + 1 + len(capture_dict[(x,y)]) + find_eye(new_curr,my_color)
                        if curr_max > max:
                            max = curr_max
                return max

    elif depth == 5:
        max_loc = []
        max = -12
        cur_max = max

        if color == '1':
            limit = 4
        else:
            limit = 3

        if early_move != -1 and early_move <= limit:
            valid_move, capture_dict = check_valid_move(prev,curr,color,new_move, True)
        else:
            valid_move, capture_dict = check_valid_move(prev,curr,color,new_move)
        if len(valid_move) >= 5:
            valid_move = heapq.nlargest(5,valid_move)
        if early_move == 12:
            if len(valid_move) == 0:
                return []
            else:
                if color == '2':
                    max_cap_move = 0
                    cur_ret = []
                    for move in valid_move:
                        if (move[1][0],move[1][1]) in capture_dict:
                            if len(capture_dict[(move[1][0],move[1][1])]) > max_cap_move:
                                max_cap_move = len(capture_dict[(move[1][0],move[1][1])])
                                cur_ret = [move[1][0],move[1][1]]
                    if cur_ret == []:
                        return [valid_move[0][1][0],valid_move[0][1][1]]
                    else:
                        return cur_ret
                else:
                    max = -12
                    max_move = []
                    for move in valid_move:
                        x = move[1][0]
                        y = move[1][1]
                        new_curr = copy.deepcopy(curr)
                        new_curr[x][y] = color
                        if (x,y) in capture_dict:
                            for cap_move in capture_dict[(x,y)]:
                                new_curr[cap_move[0]][cap_move[1]] = '0'
                        valid_move_last, capture_dict_last = check_valid_move(curr, new_curr, '2', [x,y])
                        min = 12
                        if len(valid_move_last) == 0:
                            if diff(new_curr,my_color) < min:
                                min = diff(new_curr,my_color)
                        for little_move in valid_move_last:
                            x_1 = little_move[1][0]
                            y_1 = little_move[1][1]
                            if (x_1,y_1) not in capture_dict_last:
                                cur_min = diff(new_curr,my_color) - 1
                                if cur_min < min:
                                    min = cur_min
                            else:
                                cur_min = diff(new_curr,my_color) - 1 - len(capture_dict_last[(x_1,y_1)])
                                if cur_min < min:
                                    min = cur_min
                        if min > max:
                            max = min
                            max_move = [x,y]
                    return max_move


        if early_move!= -1:
            early_move += 1
        for move in valid_move:
            x = move[1][0]
            y = move[1][1]
            punish = 0
            if x == 0 or x == 4:
                punish -= 0.25
            if y == 0 or y == 4:
                punish -= 0.25
            if (x,y) not in capture_dict:
                new_curr = copy.deepcopy(curr)
                new_past = copy.deepcopy(curr)
                new_curr[x][y] = str(0 + int(color))
                if color == '1':
                    cur_max = find_best_move(new_past, new_curr, '2', [x,y],depth - 1,my_color,early_move)
                else:
                    cur_max = find_best_move(new_past,new_curr,'1',[x,y],depth - 1,my_color,early_move)
            else:
                new_curr = copy.deepcopy(curr)
                new_past = copy.deepcopy(curr)
                new_curr[x][y] = color
                for loc in capture_dict[(x,y)]:
                    new_curr[loc[0]][loc[1]] = '0'
                if color == '1':
                    cur_max = find_best_move(new_past, new_curr, '2', [x,y],depth - 1,my_color,early_move)
                else:
                    cur_max = find_best_move(new_past,new_curr,'1',[x,y],depth - 1,my_color,early_move)
            cur_max += punish
            if cur_max >= max:
                max = cur_max
                max_loc = [x,y]
        if early_move >= 10:
            if color == '1':
                cur_max = find_best_move(copy.deepcopy(curr), copy.deepcopy(curr), '2', [],depth - 1,my_color,early_move)
            else:
                cur_max = find_best_move(copy.deepcopy(curr), copy.deepcopy(curr), '1', [],depth - 1,my_color,early_move)
            if cur_max >= max:
                max = cur_max
                max_loc = []
        return max_loc
    else:
        if color == my_color:
            max = -12
            cur_max= max

            if color == '1':
                limit = 4
            else:
                limit = 3
            if early_move != -1 and early_move <= limit:
                valid_move, capture_dict = check_valid_move(prev,curr,color,new_move, True)
            else:
                valid_move, capture_dict = check_valid_move(prev,curr,color,new_move)
            if len(valid_move) >= 8:
                valid_move = heapq.nlargest(8,valid_move)
            if early_move == 12:
                if len(valid_move) == 0:
                    return diff(curr, my_color)
                if color == '2':
                    max = -12
                    for move in valid_move:
                        x = move[1][0]
                        y = move[1][1]
                        if (x,y) not in capture_dict:
                            curr_max = diff(curr,my_color) + 1
                            if curr_max > max:
                                max = curr_max
                        else:
                            curr_max = diff(curr,my_color) + 1 + len(capture_dict[(x,y)])
                            if curr_max > max:
                                max = curr_max
                    return max
                else:
                    max = -12
                    for move in valid_move:
                        x = move[1][0]
                        y = move[1][1]
                        new_curr = copy.deepcopy(curr)
                        new_curr[x][y] = color
                        if (x,y) in capture_dict:
                            for cap_move in capture_dict[(x,y)]:
                                new_curr[cap_move[0]][cap_move[1]] = '0'
                        valid_move_last, capture_dict_last = check_valid_move(curr, new_curr, '2', [x,y])
                        min = 12
                        if len(valid_move_last) == 0:
                            if diff(new_curr,my_color) < min:
                                min = diff(new_curr,my_color)
                        for little_move in valid_move_last:
                            x_1 = little_move[1][0]
                            y_1 = little_move[1][1]
                            if (x_1,y_1) not in capture_dict_last:
                                cur_min = diff(new_curr,my_color) - 1
                                if cur_min < min:
                                    min = cur_min
                            else:
                                cur_min = diff(new_curr,my_color) - 1 - len(capture_dict_last[(x_1,y_1)])
                                if cur_min < min:
                                    min = cur_min
                        if min > max:
                            max = min
                    return max


            if early_move!= -1:
                early_move += 1
            for move in valid_move:
                x = move[1][0]
                y = move[1][1]
                if (x,y) not in capture_dict:
                    new_curr = copy.deepcopy(curr)
                    new_past = copy.deepcopy(curr)
                    new_curr[x][y] = color
                    if color == '1':
                        cur_max = find_best_move(new_past, new_curr, '2', [x,y],depth - 1,my_color,early_move)
                    else:
                        cur_max = find_best_move(new_past,new_curr,'1',[x,y],depth - 1,my_color,early_move)
                else:
                    new_curr = copy.deepcopy(curr)
                    new_past = copy.deepcopy(curr)
                    new_curr[x][y] = color
                    for loc in capture_dict[(x,y)]:
                        new_curr[loc[0]][loc[1]] = '0'
                    if color == '1':
                        cur_max = find_best_move(new_past, new_curr, '2', [x,y],depth - 1,my_color,early_move)
                    else:
                        cur_max = find_best_move(new_past,new_curr,'1',[x,y],depth - 1,my_color,early_move)
                if cur_max > max:
                    max = cur_max
            if early_move >= 11:
                if color == '1':
                    cur_max = find_best_move(copy.deepcopy(curr), copy.deepcopy(curr), '2', [],depth - 1,my_color,early_move)
                else:
                    cur_max = find_best_move(copy.deepcopy(curr), copy.deepcopy(curr), '1', [],depth - 1,my_color,early_move)
                if cur_max >= max:
                    max = cur_max
            return max
        else:
            min = 25
            cur_min = min

            if color == '1':
                limit = 4
            else:
                limit = 3
            if early_move <= limit and early_move != -1:
                valid_move, capture_dict = check_valid_move(prev,curr,color,new_move, True)
            else:
                valid_move, capture_dict = check_valid_move(prev,curr,color,new_move)
            if len(valid_move) >= 7:
                valid_move = heapq.nlargest(7,valid_move)
            for move in valid_move:
                x = move[1][0]
                y = move[1][1]
                if (x,y) not in capture_dict:
                    new_curr = copy.deepcopy(curr)
                    new_past = copy.deepcopy(curr)
                    new_curr[x][y] = color
                    if color == '1':
                        cur_min = find_best_move(new_past, new_curr, '2', [x,y],depth - 1,my_color,early_move)
                    else:
                        cur_min = find_best_move(new_past,new_curr,'1',[x,y],depth - 1,my_color,early_move)
                else:
                    new_curr = copy.deepcopy(curr)
                    new_past = copy.deepcopy(curr)
                    new_curr[x][y] = color
                    for loc in capture_dict[(x,y)]:
                        new_curr[loc[0]][loc[1]] = '0'
                    if color == '1':
                        cur_min = find_best_move(new_past, new_curr, '2', [x,y],depth - 1,my_color,early_move)
                    else:
                        cur_min = find_best_move(new_past,new_curr,'1',[x,y],depth - 1,my_color,early_move)
                if cur_min < min:
                    min = cur_min
            if early_move >= 11:
                if color == '1':
                    cur_min = find_best_move(copy.deepcopy(curr), copy.deepcopy(curr), '2', [],depth - 1,my_color,early_move)
                else:
                    cur_min = find_best_move(copy.deepcopy(curr), copy.deepcopy(curr), '1', [],depth - 1,my_color,early_move)
                if cur_min < min:
                    min = cur_min
            return min


#white moves
def find_best_move_1(prev, curr, color, new_move, depth, my_color, early_move = -1):
    #base case
    if depth == 1:
        if early_move != -1 and early_move <= 3:
            valid_move, capture_dict = check_valid_move(prev,curr,color,new_move, True)
        else:
            valid_move, capture_dict = check_valid_move(prev,curr,color,new_move)
        if len(valid_move) >= 7:
            valid_move = heapq.nlargest(7,valid_move)
        if len(valid_move) == 0:
            return diff(curr, my_color)
        else:
            if color == '1' and early_move == 12:
                max = -12
                for move in valid_move:
                    x = move[1][0]
                    y = move[1][1]
                    new_curr = copy.deepcopy(curr)
                    new_curr[x][y] = color
                    if (x,y) in capture_dict:
                        for cap_move in capture_dict[(x,y)]:
                            new_curr[cap_move[0]][cap_move[1]] = '0'
                    valid_move_last, capture_dict_last = check_valid_move(curr, new_curr, '2', [x,y])
                    min = 12
                    if len(valid_move_last) == 0:
                        if diff(new_curr,my_color) < min:
                            min = diff(new_curr,my_color)
                    for little_move in valid_move_last:
                        x_1 = little_move[1][0]
                        y_1 = little_move[1][1]
                        if (x_1,y_1) not in capture_dict_last:
                            cur_min = diff(new_curr,my_color) - 1
                            if cur_min < min:
                                min = cur_min
                        else:
                            cur_min = diff(new_curr,my_color) - 1 - len(capture_dict_last[(x_1,y_1)])
                            if cur_min < min:
                                min = cur_min
                    if min > max:
                        max = min
                return max

            else:
                max = -12
                eye_score = 0
                for move in valid_move:
                    x = move[1][0]
                    y = move[1][1]
                    if (x,y) not in capture_dict:
                        curr_max = 0
                        if early_move >= 12:
                            curr_max = diff(curr,my_color) + 1
                        else:
                            new_curr = copy.deepcopy(curr)
                            new_curr[x][y] = color
                            curr_max = diff(curr,my_color) + 1 + find_eye(new_curr,my_color)
                        if curr_max > max:
                            max = curr_max
                    else:
                        curr_max = 0
                        if early_move >= 12:
                            curr_max = diff(curr,my_color) + 1 + len(capture_dict[(x,y)])
                        else:
                            new_curr = copy.deepcopy(curr)
                            new_curr[x][y] = color
                            for cap_move in capture_dict[(x,y)]:
                                new_curr[cap_move[0]][cap_move[1]] = '0'
                            curr_max = diff(curr,my_color) + 1 + len(capture_dict[(x,y)]) + find_eye(new_curr,my_color)
                        if curr_max > max:
                            max = curr_max
                return max

    elif depth == 5:
        max_loc = []
        max = -12
        cur_max = max
        if early_move != -1 and early_move <= 3:
            valid_move, capture_dict = check_valid_move(prev,curr,color,new_move, True)
        else:
            valid_move, capture_dict = check_valid_move(prev,curr,color,new_move)
        if len(valid_move) >= 8:
            valid_move = heapq.nlargest(8,valid_move)
#         print(valid_move)
        if early_move == 12:
            if len(valid_move) == 0:
                return []
            else:
                if color == '2':
                    max_cap_move = 0
                    cur_ret = []
                    for move in valid_move:
                        if (move[1][0],move[1][1]) in capture_dict:
                            if len(capture_dict[(move[1][0],move[1][1])]) > max_cap_move:
                                max_cap_move = len(capture_dict[(move[1][0],move[1][1])])
                                cur_ret = [move[1][0],move[1][1]]
                    if cur_ret == []:
                        return [valid_move[0][1][0],valid_move[0][1][1]]
                    else:
                        return cur_ret
                else:
                    max = -12
                    max_move = []
                    for move in valid_move:
                        x = move[1][0]
                        y = move[1][1]
                        new_curr = copy.deepcopy(curr)
                        new_curr[x][y] = color
                        if (x,y) in capture_dict:
                            for cap_move in capture_dict[(x,y)]:
                                new_curr[cap_move[0]][cap_move[1]] = '0'
                        valid_move_last, capture_dict_last = check_valid_move(curr, new_curr, '2', [x,y])
                        min = 12
                        if len(valid_move_last) == 0:
                            if diff(new_curr,my_color) < min:
                                min = diff(new_curr,my_color)
                        for little_move in valid_move_last:
                            x_1 = little_move[1][0]
                            y_1 = little_move[1][1]
                            if (x_1,y_1) not in capture_dict_last:
                                cur_min = diff(new_curr,my_color) - 1
                                if cur_min < min:
                                    min = cur_min
                            else:
                                cur_min = diff(new_curr,my_color) - 1 - len(capture_dict_last[(x_1,y_1)])
                                if cur_min < min:
                                    min = cur_min
                        if min > max:
                            max = min
                            max_move = [x,y]
                    return max_move


        if early_move!= -1:
            early_move += 1
        for move in valid_move:
            x = move[1][0]
            y = move[1][1]
            punish = 0
            if x == 0 or x == 4:
                punish -= 0.25
            if y == 0 or y == 4:
                punish -= 0.25
            if (x,y) not in capture_dict:
                new_curr = copy.deepcopy(curr)
                new_past = copy.deepcopy(curr)
                new_curr[x][y] = str(0 + int(color))
                if color == '1':
                    cur_max = find_best_move_1(new_past, new_curr, '2', [x,y],depth - 1,my_color,early_move)
                else:
                    cur_max = find_best_move_1(new_past,new_curr,'1',[x,y],depth - 1,my_color,early_move)
            else:
                new_curr = copy.deepcopy(curr)
                new_past = copy.deepcopy(curr)
                new_curr[x][y] = color
                for loc in capture_dict[(x,y)]:
                    new_curr[loc[0]][loc[1]] = '0'
                if color == '1':
                    cur_max = find_best_move_1(new_past, new_curr, '2', [x,y],depth - 1,my_color,early_move)
                else:
                    cur_max = find_best_move_1(new_past,new_curr,'1',[x,y],depth - 1,my_color,early_move)
            cur_max += punish
            if cur_max >= max:
                max = cur_max
                max_loc = [x,y]
        if early_move >= 10:
            if color == '1':
                cur_max = find_best_move_1(copy.deepcopy(curr), copy.deepcopy(curr), '2', [],depth - 1,my_color,early_move)
            else:
                cur_max = find_best_move_1(copy.deepcopy(curr), copy.deepcopy(curr), '1', [],depth - 1,my_color,early_move)
            if cur_max >= max:
                max = cur_max
                max_loc = []
        return max_loc
    else:
        if color == my_color:
            max = -12
            cur_max= max
            if early_move != -1 and early_move <= 3:
                valid_move, capture_dict = check_valid_move(prev,curr,color,new_move, True)
            else:
                valid_move, capture_dict = check_valid_move(prev,curr,color,new_move)
            if len(valid_move) >= 7:
                valid_move = heapq.nlargest(7,valid_move)
            if early_move == 12:
                if len(valid_move) == 0:
                    return diff(curr, my_color)
                if color == '2':
                    max = -12
                    for move in valid_move:
                        x = move[1][0]
                        y = move[1][1]
                        if (x,y) not in capture_dict:
                            curr_max = diff(curr,my_color) + 1
                            if curr_max > max:
                                max = curr_max
                        else:
                            curr_max = diff(curr,my_color) + 1 + len(capture_dict[(x,y)])
                            if curr_max > max:
                                max = curr_max
                    return max
                else:
                    max = -12
                    for move in valid_move:
                        x = move[1][0]
                        y = move[1][1]
                        new_curr = copy.deepcopy(curr)
                        new_curr[x][y] = color
                        if (x,y) in capture_dict:
                            for cap_move in capture_dict[(x,y)]:
                                new_curr[cap_move[0]][cap_move[1]] = '0'
                        valid_move_last, capture_dict_last = check_valid_move(curr, new_curr, '2', [x,y])
                        min = 12
                        if len(valid_move_last) == 0:
                            if diff(new_curr,my_color) < min:
                                min = diff(new_curr,my_color)
                        for little_move in valid_move_last:
                            x_1 = little_move[1][0]
                            y_1 = little_move[1][1]
                            if (x_1,y_1) not in capture_dict_last:
                                cur_min = diff(new_curr,my_color) - 1
                                if cur_min < min:
                                    min = cur_min
                            else:
                                cur_min = diff(new_curr,my_color) - 1 - len(capture_dict_last[(x_1,y_1)])
                                if cur_min < min:
                                    min = cur_min
                        if min > max:
                            max = min
                    return max


            if early_move!= -1:
                early_move += 1
            for move in valid_move:
                x = move[1][0]
                y = move[1][1]
                if (x,y) not in capture_dict:
                    new_curr = copy.deepcopy(curr)
                    new_past = copy.deepcopy(curr)
                    new_curr[x][y] = color
                    if color == '1':
                        cur_max = find_best_move_1(new_past, new_curr, '2', [x,y],depth - 1,my_color,early_move)
                    else:
                        cur_max = find_best_move_1(new_past,new_curr,'1',[x,y],depth - 1,my_color,early_move)
                else:
                    new_curr = copy.deepcopy(curr)
                    new_past = copy.deepcopy(curr)
                    new_curr[x][y] = color
                    for loc in capture_dict[(x,y)]:
                        new_curr[loc[0]][loc[1]] = '0'
                    if color == '1':
                        cur_max = find_best_move_1(new_past, new_curr, '2', [x,y],depth - 1,my_color,early_move)
                    else:
                        cur_max = find_best_move_1(new_past,new_curr,'1',[x,y],depth - 1,my_color,early_move)
                if cur_max > max:
                    max = cur_max
            if early_move >= 11:
                if color == '1':
                    cur_max = find_best_move_1(copy.deepcopy(curr), copy.deepcopy(curr), '2', [],depth - 1,my_color,early_move)
                else:
                    cur_max = find_best_move_1(copy.deepcopy(curr), copy.deepcopy(curr), '1', [],depth - 1,my_color,early_move)
                if cur_max >= max:
                    max = cur_max
            return max
        else:
            min = 25
            cur_min = min
            if early_move <= 3 and early_move != -1:
                valid_move, capture_dict = check_valid_move(prev,curr,color,new_move, True)
            else:
                valid_move, capture_dict = check_valid_move(prev,curr,color,new_move)
            if len(valid_move) >= 7:
                valid_move = heapq.nlargest(7,valid_move)
            for move in valid_move:
                x = move[1][0]
                y = move[1][1]
                if (x,y) not in capture_dict:
                    new_curr = copy.deepcopy(curr)
                    new_past = copy.deepcopy(curr)
                    new_curr[x][y] = color
                    if color == '1':
                        cur_min = find_best_move_1(new_past, new_curr, '2', [x,y],depth - 1,my_color,early_move)
                    else:
                        cur_min = find_best_move_1(new_past,new_curr,'1',[x,y],depth - 1,my_color,early_move)
                else:
                    new_curr = copy.deepcopy(curr)
                    new_past = copy.deepcopy(curr)
                    new_curr[x][y] = color
                    for loc in capture_dict[(x,y)]:
                        new_curr[loc[0]][loc[1]] = '0'
                    if color == '1':
                        cur_min = find_best_move_1(new_past, new_curr, '2', [x,y],depth - 1,my_color,early_move)
                    else:
                        cur_min = find_best_move_1(new_past,new_curr,'1',[x,y],depth - 1,my_color,early_move)
                if cur_min < min:
                    min = cur_min
            if early_move >= 11:
                if color == '1':
                    cur_min = find_best_move_1(copy.deepcopy(curr), copy.deepcopy(curr), '2', [],depth - 1,my_color,early_move)
                else:
                    cur_min = find_best_move_1(copy.deepcopy(curr), copy.deepcopy(curr), '1', [],depth - 1,my_color,early_move)
                if cur_min < min:
                    min = cur_min
            return min



#valid playing moves
def check_valid_move(prev, curr, color,new_move, Is_Early = False):
    valid_moves = []
    check_captrued_dict = {}  #don't check same loc twice
    cur_move = []

    #return
    capture_opponents_moves = {}
    score = {}
    lost_moves = []
    check_ko = False
    KO = False

    # heapq.heappush(valid_move, (,))
    for i in range(5):
        for j in range(5):
            if curr[i][j] == '0' and prev[i][j] == color:
                lost_moves.append([i,j])

    if len(lost_moves) == 1:
        check_ko = True


    for i in range(5):
        for j in range(5):
            if curr[i][j] != color and curr[i][j] != "0":
                #  need!!!!!!!!!!!!!!!!!!!!! change
                capture_moves, num_cap = get_capture_moves(curr, [i,j], capture_opponents_moves)
                #detect KO
                if check_ko:
                    if len(new_move) != 0:
                        if i == new_move[0] and j == new_move[1]:
                            if len(capture_moves) == 1:
                                if prev[capture_moves[0][0]][capture_moves[0][1]] == color and curr[capture_moves[0][0]][capture_moves[0][1]] != color:
                                    KO = True
                                    for a, b in ( (new_move[0],new_move[1]+1),(new_move[0]+1,new_move[1]),(new_move[0],new_move[1]-1),(new_move[0]-1,new_move[1])):
                                        if 0<= a < 5 and 0 <= b < 5:
                                            if a == lost_moves[0][0] and b == lost_moves[0][1]:
                                                continue
                                            else:
                                                if curr[a][b] != color:
                                                    KO = False
                if len(capture_moves) == 1:
                    if (capture_moves[0][0],capture_moves[0][1]) in capture_opponents_moves:
                        capture_opponents_moves[(capture_moves[0][0],capture_moves[0][1])] += num_cap
                    else:
                        capture_opponents_moves[(capture_moves[0][0],capture_moves[0][1])] = num_cap

                for k in range(len(capture_moves)):
                    if (capture_moves[k][0],capture_moves[k][1]) in score:
                        score[(capture_moves[k][0],capture_moves[k][1])] += len(num_cap)/len(capture_moves)
                    else:
                        score[(capture_moves[k][0],capture_moves[k][1])] = len(num_cap)/len(capture_moves)

    if Is_Early:
        for i in range(1,4):
            for j in range(1,4):
                if KO and i == lost_moves[0][0] and j == lost_moves[0][1]:
                    continue
                elif curr[i][j] == "0":
                    if check_captured(curr, [i,j],check_captrued_dict, color) == False:
                        if (i,j) in score:
                            heapq.heappush(valid_moves, (score[(i,j)],[i,j]))
                        else:
                            heapq.heappush(valid_moves, (random.uniform(0, 0.25), [i,j]))
                    else:
                        if (i,j) in capture_opponents_moves:
                            heapq.heappush(valid_moves, (score[(i,j)],[i,j]))
    else:
        for i in range(5):
            for j in range(5):
                if KO and i == lost_moves[0][0] and j == lost_moves[0][1]:
                    continue
                elif curr[i][j] == "0":
                    if check_captured(curr, [i,j],check_captrued_dict, color) == False:
                        if (i,j) in score:
                            heapq.heappush(valid_moves, (score[(i,j)],[i,j]))
                        else:
                            heapq.heappush(valid_moves, (random.uniform(0, 0.25), [i,j]))
                    else:
                        if (i,j) in capture_opponents_moves:
                            heapq.heappush(valid_moves, (score[(i,j)],[i,j]))
    return valid_moves, capture_opponents_moves

def check_captured(board, root,check_dict,oppo_color):
    if (root[0],root[1]) in check_dict:
        return check_dict[(root[0],root[1])]
    total = []
    total.append((root[0],root[1]))
    queue = []
    queue.append(root)
    visited = {}

    while len(queue) != 0:
        cur = queue.pop()
        x = cur[0]
        y = cur[1]
        if (x,y) in visited:
            continue
        else:
            visited[(x,y)] = 1
        if (x,y) in check_dict:
            for loc in total:
                check_dict[loc] = check_dict[(x,y)]
            return check_dict[(x,y)]
        for a,b in ((x+1, y),(x-1,y), (x, y+1), (x, y-1)):
            if 0 <= a < 5 and 0 <= b < 5 and (a,b) not in visited:
                if board[a][b] == "0":
                    for loc in total:
                        check_dict[loc] = False
                    return False
                elif board[a][b] == oppo_color:
                    queue.append([a,b])
                    total.append((root[0],root[1]))
    for loc in total:
        check_dict[loc] = True
    return True


def get_capture_moves(curr, root, capture_opponents_moves):
    if (root[0],root[1]) in capture_opponents_moves:
        return [], []
    cur_color = curr[root[0]][root[1]]
    # count = 0
    total = []
    ret = []
    ret_dict = {}
    queue = []
    queue.append(root)
    visited = {}
    while len(queue) != 0:
        cur = queue.pop()
        x = cur[0]
        y = cur[1]
        if (x,y) in visited:
            continue
        else:
            visited[(x,y)] = 1
        total.append([x,y])
        capture_opponents_moves[(x,y)] = 1
        for a,b in ((x+1, y),(x-1,y), (x, y+1), (x, y-1)):
            if 0 <= a < 5 and 0 <= b < 5:
                if curr[a][b] == "0":
                    if (a,b) not in ret_dict:
                        ret_dict[(a,b)] = 1
                        ret.append([a,b])
                    else:
                        continue
                elif curr[a][b] == cur_color:
                    queue.append([a,b])
    return ret, total


if __name__ == "__main__":
    little_go()
