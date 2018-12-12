'''
def print_cycle():
    print("CPU Cycles ==>\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\t16\n")


file = "ex02.s"
f = open(file, "r")
i = 0

if f.mode == 'r':
    content = f.read()
    print(content)
    
ins = content.split("\n")
for i in ins:
    if i == '':
        ins.remove(i)
'''

def execute(j):
    pass





def print_cycle(cycle, cycle_num, ins_num, ins_list): 
    '''
    A function that do the print cycle
    '''
    #print(cycle)
    print("-"*82)
    print("CPU Cycles ===>     1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16") 
    line_num = 0 #row num of cycle
    while((line_num < cycle_num+1) and (line_num < ins_num)): 
        ins_place = 0 #column num of cycle
        #print(len(ins_list),line_num)
        line = ins_list[line_num] + " " * (20 - len(ins_list[line_num]))
        while (ins_place < 16): 
            if(cycle[line_num][ins_place] == 0): 
                line += ".   " 
            elif(cycle[line_num][ins_place] == 1): 
                line += "IF  " 
            elif(cycle[line_num][ins_place] == 2): 
                line += "ID  " 
            elif(cycle[line_num][ins_place] == 3): 
                line += "EX  " 
            elif(cycle[line_num][ins_place] == 4): 
                line += "MEM " 
            elif(cycle[line_num][ins_place] == 5): 
                line += "WB  " 
            elif(cycle[line_num][ins_place] == -1): 
                line += "*   " 
            else: 
                line+= "????" 
            ins_place += 1 #increrment for column
        
        line_num += 1 #increrment for row
        print(line.rstrip())
    print()

def readdata(filename):
    f = open(filename, "r")
    content = f.read()
    data = content.split("\n")
    return data



# -1 stand for *
# 0 stand for .
# 1 stand for IF
# 2 stand for ID
# 3 stand for EX
# 4 stand for MEM
# 5 stand for WB

# (int)num_inst is the number of total instrustion(i.e. 3)
# f_l is a list containing the first regrister e.g. [5, 3, 4, ...] t = +0, s = +10
# s_l is a list containing the second and third regrister e.g. [[1, 2], [3, -1]] t = +0, s = +10, $zero or immediate value = -1

def no_forward(filename, _list):

    original_data = readdata(filename)
    num_inst = len(_list)
    #create a total_list(num_inst * 16)
    i = 0
    total_list = []
    while i<num_inst:
        new_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        total_list.append(new_list)
        i+=1
    #create a checklist (if use, 0 -> 1)
    check_list = []
    nop = []
    real_nop = []
    w = []
    i = 0
    while i < num_inst:
        i+=1
        check_list.append(0)
        nop.append(0)
        real_nop.append(0)
        w.append(0)

    #calculate nop[]
    f_l = []
    s_l = []
    for i in _list:
        f_l.append(i[1])
        l = []
        l.append(i[2])
        l.append(i[3])
        s_l.append(l)


    for k in range(len(s_l)):
        for j in range(len(f_l)):
            if j < k and j>k-3 and (f_l[j] == s_l[k][0] or f_l[j] == s_l[k][1]):
                if (nop[k] < k - j):
                    nop[k] = k - j
    
    temp = 0
    i_f = 0

    #fill in the instruction as the program run
    i = 0
    while i < 16:

        if (temp!=0 and i - temp == 3):
            t = total_list[temp].index(1)
            total_list[temp][t+real_nop[temp]+2] = 3

        if (temp!=0 and i - temp == 4):
            t = total_list[temp].index(1)
            total_list[temp][t+real_nop[temp]+3] = 4

        if (temp!=0 and i - temp == 5):
            t = total_list[temp].index(1)
            total_list[temp][t+real_nop[temp]+4] = 5

        if (i_f!=0 and i - i_f == 2):
            t = total_list[i_f].index(1)
            total_list[i_f][t+real_nop[i_f-1]+1] = 2

        if (i_f!=0 and i - i_f == 3):
            t = total_list[i_f].index(1)
            total_list[i_f][t+real_nop[i_f-1]+2] = 3

        if (i_f!=0 and i - i_f == 4):
            t = total_list[i_f].index(1)
            total_list[i_f][t+real_nop[i_f-1]+3] = 4

        if (i_f!=0 and i - i_f == 5):
            t = total_list[i_f].index(1)
            total_list[i_f][t+real_nop[i_f-1]+4] = 5
        

        #WB
        #if empty, fill in
        #else, find the next empty place.
        #if (i>=4 and len(real_nop) > i-3 and real_nop[i-4] == 0):
        if i >= 4 and i<num_inst+4 and total_list[i-4][i] == 0:
            total_list[i-4][i] = 5
            '''
        elif i >= 4 and i < num_inst+4:
            j = i
            while j < 16:
                if total_list[i-4][j] == 0:
                    total_list[i-4][j] = 5
                    break
                j+=1
                '''
        #MEM
        #if empty, fill in
        #else, find the next empty place.
        #if (i>=3 and len(real_nop) > i-3 and real_nop[i-3] == 0):
        if i >= 3 and i<num_inst+3 and total_list[i-3][i] == 0:
            total_list[i-3][i] = 4

            '''
        elif i >= 3 and i < num_inst+3:
            j = i
            while j < 16:
                if total_list[i-3][j] == 0:
                    total_list[i-3][j] = 4
                    break
                j+=1
'''


        #EX
        #if empty, fill in
        #else, find the next empty place.
        if i>=2 and i<num_inst+2 and total_list[i-2][i] == 0:
            if nop[i-2] == 0 or check_list[i-2-nop[i-2]] == 1:
                total_list[i-2][i] = 3
            else:
                #find the num of nop
                real_nop[i-2] = 5 - total_list[i-2-nop[i-2]][i] + 1
                total_list[i-2][i] = 2
                temp = i - 2

        '''
        elif (i>=2 and i<num_inst+2):
            j = i
            while j < 16:
                if total_list[i-2][j] == 0:
                    total_list[i-2][j] = 3
                    break
                j+=1    
                '''    
        #if ID block(in the previous instruction), print IF
        if i>=1 and i<num_inst+1 and total_list[i-1][i] == 0 and total_list[i-2][i] == 2:
            total_list[i-1][i] = 1
            print(i_f)
            i_f = i - 1

        #ID
        #if empty, fill in
        #else, find the next empty place.
        if i>=1 and i<num_inst+1 and total_list[i-1][i] == 0:
            total_list[i-1][i] = 2
            '''
        elif (i>=1 and i<num_inst+1):
            j = i
            while j < 16:
                if total_list[i-1][j] == 0:
                    total_list[i-1][j] = 2
                    break
                j+=1
'''


        #IF
        #if empty, fill in
        #else, find the next empty place.
        if (i >= 0 and i<num_inst and total_list[i][i] == 0):
            total_list[i][i] = 1
            '''
        elif (i >= 0 and i < num_inst):
            j = i
            while j < 16:
                if total_list[i][j] == 0:
                    total_list[i][j] = 1
                    break
                j+=1
'''

        
        

        print_cycle(total_list, i, num_inst,original_data)
                
        #determine end of instruction
        j = 0
        while j < num_inst:
            for ins in total_list[j]:
                if ins == 5 and check_list[j] == 0:
                    #execute should change when using in the main procedure
                    execute(j)
                    check_list[j] = 1
            j+=1


        #determine end of program
        for ins in total_list[num_inst-1]:
            if ins == 5:
                return total_list

        i+=1


        



    return total_list
