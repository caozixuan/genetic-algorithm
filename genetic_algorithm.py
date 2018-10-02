#encode:utf-8
import numpy as np
import random

target_points = [[6, 16], [6, 17], [7, 16], [7, 17], [8, 16], [8, 17]]

# 读取推箱子地图
def read_to_matrix():
    matrix = []
    f = open("test.txt")
    line = f.readline()
    while line:
        matrix_line = []
        for char in line:
            matrix_line.append(char)
        matrix.append(matrix_line)
        line = f.readline()
    np.array(matrix)
    f.close()
    return matrix


# 寻找玩家位置
def find_person(matrix):
    for i in range(0, 11):
        for j in range(0, 19):
            if matrix[i][j] == '@':
                return i, j
    return -1, -1


# 计算箱子到目标点的最近曼哈顿距离
def calculate_points(matrix):
    points = 0
    for i in range(0, 11):
        for j in range(0, 19):
            if matrix[i][j] == '$':
                distances = []
                for point in target_points:
                    distance = abs(i - point[0]) + abs(j - point[1])
                    distances.append(distance)
                points = points + min(distances)
    return points


# 移动
def move(matrix, direction):
    if direction == 0:
        if up(matrix):
            return True
        return False
    elif direction == 1:
        if down(matrix):
            return True
        return False
    elif direction == 2:
        if left(matrix):
            return True
        return False
    elif direction == 3:
        if right(matrix):
            return True
        return False


def up(matrix):
    i, j = find_person(matrix)
    if i > 0:
        up_i = i - 1
        if matrix[up_i][j] == '-' or matrix[up_i][j] == '.':
            matrix[i][j] = '-'
            matrix[up_i][j] = '@'
            return True
        elif matrix[up_i][j] == '#':
            return False
        elif matrix[up_i][j] == '$':
            if up_i > 0:
                box_up = up_i - 1
                if matrix[box_up][j] == '-' or matrix[box_up][j] == '.':
                    matrix[i][j] = '-'
                    matrix[up_i][j] = '@'
                    matrix[box_up][j] = '$'
                    return True
                else:
                    return False
            else:
                return False
    else:
        return False


def down(matrix):
    i, j = find_person(matrix)
    if i < 10:
        down_i = i + 1
        if matrix[down_i][j] == '-' or matrix[down_i][j] == '.':
            matrix[i][j] = '-'
            matrix[down_i][j] = '@'
            return True
        elif matrix[down_i][j] == '#':
            return False
        elif matrix[down_i][j] == '$':
            if down_i < 10:
                box_down = down_i - 1
                if matrix[box_down][j] == '-' or matrix[box_down][j] == '.':
                    matrix[i][j] = '-'
                    matrix[down_i][j] = '@'
                    matrix[box_down][j] = '$'
                    return True
                else:
                    return False
            else:
                return False
    else:
        return False


def left(matrix):
    i, j = find_person(matrix)
    if j > 0:
        left_j = j - 1
        if matrix[i][left_j] == '-' or matrix[i][left_j] == '.':
            matrix[i][j] = '-'
            matrix[i][left_j] = '@'
            return True
        elif matrix[i][left_j] == '#':
            return False
        elif matrix[i][left_j] == '$':
            if left_j > 0:
                box_left = left_j - 1
                if matrix[i][box_left] == '-' or matrix[i][box_left] == '.':
                    matrix[i][j] = '-'
                    matrix[i][left_j] = '@'
                    matrix[i][box_left] = '$'
                    return True
                else:
                    return False
            else:
                return False
    else:
        return False


def right(matrix):
    i, j = find_person(matrix)
    if j < 18:
        right_j = j + 1
        if matrix[i][right_j] == '-' or matrix[i][right_j] == '.':
            matrix[i][j] = '-'
            matrix[i][right_j] = '@'
            return True
        elif matrix[i][right_j] == '#':
            return False
        elif matrix[i][right_j] == '$':
            if right_j < 18:
                box_left = right_j + 1
                if matrix[i][box_left] == '-' or matrix[i][box_left] == '.':
                    matrix[i][j] = '-'
                    matrix[i][right_j] = '@'
                    matrix[i][box_left] = '$'
                    return True
                else:
                    return False
            else:
                return False
    else:
        return False


#根据数组移动
def sequence_move(move_array, matrix):
    for direction in move_array:
        if move(matrix, direction):
            continue
        else:
            move_array.remove(direction)
    return calculate_points(matrix)


# up:0 down:1 left:2 right:3


class Animal:
    def __init__(self, move_array, points):
        self.move_array = move_array
        self.points = points


# 变异
def variation(animals):
    for animal in animals:
        if animal.points!=0:
            for m in range(0,len(animal.move_array)):
                ret = random.random()
                if ret<change_rate:
                    animal.move_array[m] = random.randint(0,3)
                elif ret<2*change_rate and len(animal.move_array)<max_length:
                    animal.move_array.insert(m,random.randint(0,3))
    return animals


def hybridize(parents):
    child = []
    father = parents[0]
    mather = parents[1]
    i = 0
    while i < len(father.move_array)-mix_length and i < len(mather.move_array)-mix_length:
        flag =  random.randint(0,1)
        if flag == 0:
            for j in range(0,mix_length):
                child.append(father.move_array[i+j])
        else:
            for j in range(0,mix_length):
                child.append(mather.move_array[i+j])
        i = i+mix_length
    if len(child)<max_length:
        for k in range(0,add_step):
            child.append(random.randint(0,3))
    return child


change_rate = 0.05        #变异率
expel_rate = 0.5          #淘汰率
initial_length = 10       #初始移动步数
max_length = 50           #最大移动步数
add_step = 10             #每次增加的步长
max_epoch = 1000          #最大迭代次数
sample = 100              #种群数量
mix_length = 3            #基因混合长度
animals = []

#初始化种群
for i in range(0,100):
    change_matrix = read_to_matrix()
    move_array = []
    for j in range(0,initial_length):
        move_array.append(random.randint(0,3))
    points = sequence_move(move_array,change_matrix )
    animals.append(Animal(move_array,points))
animals.sort(key=lambda x:x.points,reverse=False)
print(animals[0].points)


#种群迭代
for k in range(0,max_epoch):
    animals = animals[0:50]
    animals = variation(animals)    #变异
    for n in range(0,50):
        change_matrix = read_to_matrix()
        # 交配增殖
        parents = random.sample(animals, 2)
        child_array = hybridize(parents=parents)
        points = sequence_move(child_array,change_matrix)
        animals.append(Animal(child_array,points))
    animals.sort(key=lambda x: x.points,reverse=False)
    print(animals[0].points)
    if animals[0].points==0:
        print(animals[0].move_array)
        break
#0123


