import os
import heapq

def func():
    try:
        os.remove("output.txt")
    except OSError:
        pass
    f = open("input.txt", "r")
    action = -1
    count  = 0
    jump_dict = {}
    year_dict = {}
    weight_dict = {}
    
    for line in f:
        line = line.strip()
        if count == 0:
            if line == "BFS":
                action = 0
            elif line == "UCS":
                action = 1
            else:
                action = 2
            count += 1
        elif count == 1:
            x_size, y_size = line.split(" ")
            x_size = int(x_size)
            y_size = int(y_size)
            count += 1
        elif count == 2:
            start_loc =  line.split()
            start_loc[0] = int(start_loc[0])
            start_loc[1] = int(start_loc[1])
            start_loc[2] = int(start_loc[2])    
            count += 1
        elif count == 3:
            end_loc = line.split()
            end_loc[0] = int(end_loc[0])
            end_loc[1] = int(end_loc[1])
            end_loc[2] = int(end_loc[2])
            count += 1
        elif count == 4:
            count += 1
            continue
        else:
            a, b, c, d = line.split()
            a,b,c,d = int(a),int(b),int(c),int(d)
            
            if b < 0 or b >= x_size or c < 0 or c >= y_size:
                continue
                
            if (a,b,c) in jump_dict:
                jump_dict[(a,b,c)].append([d,b,c])
            else:
                jump_dict[(a,b,c)]  = [[d,b,c]]
            if (d,b,c) in jump_dict:
                jump_dict[(d,b,c)].append([a,b,c])
            else:
                jump_dict[(d,b,c)] = [[a,b,c]]

            if action == 2:
                t = end_loc
                if (a,b,c) not in weight_dict:
                    weight_dict[(a,b,c)] = 10 * abs(abs(t[1] - b) - abs(t[2]- c)) + 14 * min(abs(t[1] - b), abs(t[2]- c)) + abs(a - t[0])
                if (d,b,c) not in weight_dict:
                    weight_dict[(d,b,c)] = 10 * abs(abs(t[1] - b) - abs(t[2]- c)) + 14 * min(abs(t[1] - b), abs(t[2]- c)) + abs(d - t[0])
                
    if action == 0:
        ifs, steps = bfs(start_loc, end_loc,jump_dict, x_size, y_size)
        f = open("output.txt", "w")
        if ifs == -1:
            f.write("FAIL")
            f.close()
        else:
            cost = len(steps)
            temp_cost = str(cost - 1)
            cost = str(cost)
            f.write(temp_cost + '\n')
            f.write(cost + '\n')
            first_time = 0
            for st in steps:
                for number in st:
                    number = str(number)
                    f.write(number + " ")
                if first_time == 0:
                    f.write('0')
                    first_time = 1
                else:
                    f.write('1')
                f.write('\n')
            f.close()
    if action == 1:
        ifs, steps = ucs(start_loc, end_loc,jump_dict, x_size, y_size)
        f = open("output.txt", "w")
        if ifs == -1:
            f.write("FAIL")
            f.close()
        else:
            ifs = str(ifs)
            f.write(ifs + '\n')
            temp_num_step = str(len(steps))
            f.write(temp_num_step + '\n')
            for st in steps:
                for number in st:
                    number = str(number)
                    f.write(number + " ")
                f.write('\n')
            f.close()
    if action == 2:
        ifs, steps = astar(start_loc, end_loc, jump_dict, x_size, y_size, weight_dict)
        f = open("output.txt", "w")
        if ifs == -1:
            f.write("FAIL")
            f.close()
        else:
            ifs = str(ifs)
            f.write(ifs + '\n')
            temp_num_step = str(len(steps))
            f.write(temp_num_step + '\n')
            for st in steps:
                for number in st:
                    number = str(number)
                    f.write(number + " ")
                f.write('\n')
            f.close()


def bfs(s, t, jump, x_size, y_size):
    cur_node = s
    visited = {}
    queue = []
    queue.append(cur_node)
    success = 0
    while len(queue)!= 0:
        cur_node = queue.pop(0)
        cur_year = cur_node[0]
        x = cur_node[1]
        y = cur_node[2]   
        
        if cur_node == t:
            success = 1
            break

        for a,b in ((x-1,y-1), (x-1, y), (x-1, y+1), (x,y-1), (x,y+1),(x+1, y-1),(x+1,y),(x+1,y+1)):
            if 0 <= a < x_size and 0 <= b < y_size:
                if (cur_year, a, b) not in visited:
                    visited[(cur_year, a, b)] = [cur_year,x,y]
                    queue.append([cur_year,a,b])
        
        if (cur_year, x, y) in jump:
            year_list = jump[(cur_year, x, y)]
            for temp in year_list:
                if (temp[0],x,y) not in visited:
                    visited[(temp[0],x,y)] = [cur_year,x,y]
                    queue.append([temp[0],x,y])
    result = []
    if success == 1:
        while cur_node != s:
            result.append(cur_node)
            cur_node = visited[(cur_node[0],cur_node[1],cur_node[2])]
        result.append(s)
        return 0, result[::-1]  
    return -1 , []                


def ucs(s, t, jump, x_size, y_size, defaultCost = 0):
    cur_node = list(s)
    cur_node.append(defaultCost) #current cost
    visited = {}
    queue = []
    heapq.heappush(queue, (defaultCost, cur_node))
    success = 0
    cost_in_total = 0
    count = 0 
    
    while len(queue)!= 0:
        count += 1
        total_cost, cur_node = heapq.heappop(queue)
        cur_year = cur_node[0]
        x = cur_node[1]
        y = cur_node[2]
        last_cost = cur_node[3]
        
        if cur_node[:3] == t:
            success = 1
            cost_in_total = total_cost
            break
        
        #diagonal
        for a,b in ((x-1, y), (x,y-1), (x,y+1),(x+1,y)):
            if 0 <= a < x_size and 0 <= b < y_size:
                if (cur_year, a, b) not in visited:
                    visited[(cur_year,a,b)] = [cur_year,x,y,last_cost]
                    heapq.heappush(queue, (10 + total_cost, [cur_year, a, b, 10]))
                
        #nswe 
        for a,b in ((x-1,y-1),(x-1, y+1),(x+1, y-1),(x+1,y+1)):
            if 0 <= a < x_size and 0 <= b < y_size:
                if (cur_year, a, b) not in visited:
                    visited[(cur_year,a,b)] = [cur_year,x,y,last_cost]
                    heapq.heappush(queue,(14+total_cost, [cur_year, a, b, 14]))

        if (cur_year, x, y) in jump:
            year_list = jump[(cur_year, x, y)]
            for temp in year_list:
                temp = list(temp)
                if (temp[0], x, y) not in visited:
                    visited[(temp[0],x,y)] = [cur_year,x,y,last_cost]
                    cur_cost = abs(temp[0] - cur_year)
                    temp.append(cur_cost)
                    heapq.heappush(queue, (cur_cost + total_cost, temp))
    
    result = []
    print(count)
    if success == 1:
        while cur_node[:3] != s:
            result.append(cur_node[:4])
            cur_node = visited[(cur_node[0],cur_node[1],cur_node[2])]
        result.append(cur_node[:4])
        return cost_in_total, result[::-1]
    return -1 , []        
            
def astar(s, t, jump, x_size, y_size, weight_dict):
    cur_node = list(s)
    cur_node.append(0) #past cost
    cur_node.append(0) #total cost
    cur_node.append([])
    visited = {}
    queue = []
    heapq.heappush(queue, (0, cur_node))
    success = 0
    while len(queue) != 0:
        es_cost, cur_node = heapq.heappop(queue)
        cur_year = cur_node[0]
        x = cur_node[1]
        y = cur_node[2]
        last_cost = cur_node[3]
        total_cost = cur_node[4]
        if (cur_year,x,y) in visited:
            if total_cost != visited[(cur_year,x,y)][4]:
                continue
            
            
            
            
        if cur_node[:3] == t:
            success = 1
            cost_in_total = total_cost
            break

        #diagonal
        for a,b in ((x-1, y), (x,y-1), (x,y+1),(x+1,y)):
            if 0 <= a < x_size and 0 <= b < y_size:
                if (cur_year,a,b) not in visited:
                    cost_temp = 14 * min(abs(t[1] - a) , abs(t[2] - b)) + 10 * abs(abs(t[1] - a) - abs(t[2] - b)) + abs(t[0] - cur_year)
                    visited[(cur_year,a,b)] = [cur_year,x,y,last_cost, total_cost + 10, cost_temp]
                    heapq.heappush(queue, (10 + total_cost + cost_temp , [cur_year, a, b, 10, total_cost + 10]))
                else:
                    past_cost_diff = visited[(cur_year,a,b)][4] - (total_cost + 10) 
                    if past_cost_diff > 0:
                        visited[(cur_year,a,b)] = [cur_year,x,y,last_cost, total_cost + 10, visited[(cur_year,a,b)][5]]
                        heapq.heappush(queue, (10 + total_cost + visited[(cur_year,a,b)][5], [cur_year, a, b, 10, total_cost + 10]))
        #nswe 
        for a,b in ((x-1,y-1),(x-1, y+1),(x+1, y-1),(x+1,y+1)):
            if 0 <= a < x_size and 0 <= b < y_size:
                if (cur_year,a,b) not in visited:
                    cost_temp = 14 * min(abs(t[1] - a) , abs(t[2] - b)) + 10 * abs(abs(t[1] - a) - abs(t[2] - b)) + abs(t[0] - cur_year)
                    visited[(cur_year,a,b)] = [cur_year,x,y,last_cost, total_cost + 14, cost_temp]
                    heapq.heappush(queue, (14 + total_cost + cost_temp, [cur_year, a, b, 14, total_cost + 14]))
                else:
                    past_cost_diff = visited[(cur_year,a,b)][4] - (total_cost + 14)
                    if past_cost_diff > 0:
                        visited[(cur_year,a,b)] = [cur_year,x,y,last_cost,total_cost + 14, visited[(cur_year,a,b)][5]]
                        heapq.heappush(queue, (14 + total_cost + visited[(cur_year,a,b)][5], [cur_year, a, b, 14, total_cost + 14]))

        if (cur_year, x, y) in jump:
            year_list = jump[(cur_year, x, y)]
            for temp in year_list:
                temp = list(temp)
                cur_cost = abs(temp[0] - cur_year)
                if (temp[0], x, y) not in visited:
                    visited[(temp[0],x,y)] = [cur_year,x,y,last_cost, cur_cost+total_cost,weight_dict[(temp[0], x, y)]]                    
                    temp.append(cur_cost)
                    temp.append(cur_cost + total_cost)
                    heapq.heappush(queue, (cur_cost + total_cost + weight_dict[(temp[0], x, y)], temp))
                else:
                    past_cost_diff = visited[(temp[0],x,y)][4] - (total_cost + cur_cost)
                    if past_cost_diff > 0:
                        visited[(temp[0],x,y)] = [temp[0],x,y,cur_cost, total_cost + cur_cost, weight_dict[(temp[0], x, y)]]
                        heapq.heappush(queue, (cur_cost + total_cost + weight_dict[(temp[0], x, y)], [temp[0],x,y,cur_cost, cur_cost + total_cost]))
                    
    result = []
    
    if success == 1:
        while cur_node[:3] != s:
            result.append(cur_node[:4])
            cur_node = visited[(cur_node[0],cur_node[1],cur_node[2])]
        result.append(cur_node[:4])
        return cost_in_total, result[::-1]
    return -1 , []        