
def check_branch(register_list,ins):
    '''
    A function that determine if the branch is taken
    '''  

    #ins="bne $s1,$ZERO,gg"
    #{s0 s1 s2 s3 s4 s5 s6 s7 t0 t1 t2}
    branchType = ""

    register_dict = {"$s0": 0, "$s1": 1, "$s2": 2, "$s3": 3, "$s4": 4, "$s5": 5,
                     "$s6": 6, "$s7": 7, "$t0": 8,
                     "$t1": 9, "$t2": 10, "$t3": 11, "$t4": 12, "$t5": 13,
                     "$t6": 14, "$t7": 15, "$t8": 16, "$t9": 17, "$ZERO": -1
                     }




    temp=ins.split()
    if(temp.length()<2):
        pass
    else:
        branchType=temp[0]
        temp=temp.split(',')
    #     temp=["$s1","$t2","gg"]
        index=register_dict[temp[0]]
        if index==-1:
            a=0
        else:
            a=register_list[index]
        index=register_dict[temp[1]]
        if index==-1:
            b=0
        else:
            b=register_list[index]


        if branchType == "beq":
            return a==b
        elif branchType == "bne":
            return a!=b



    return False

def get_label_num():
    '''
    A function that get number of label
    '''   
    label_num = 0
    return label_num

def label_position():
    '''
    A function that get label position
    '''   
    label_from = 1
    label_to = 4
    return (label_from,label_to)

def print_cycle(cycle, cycle_num, ins_num, ins_list): 
    '''
    A function that do the print cycle
    '''
    print("-"*82)
    print("CPU Cycles ===>     1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16") 
    line_num = 0 #row num of cycle
    while((line_num < cycle_num) and (line_num < ins_num)): 
        ins_place = 0 #column num of cycle
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
        print(line)
        
def print_register(register_list): 
    '''
    A function that do the print register
    '''
    print("$s0 = {:<14d}$s1 = {:<14d}$s2 = {:<14d}$s3 = {:<14d}".\
          format(register_list[0],register_list[1],register_list[2],register_list[3]))
    print("$s4 = {:<14d}$s5 = {:<14d}$s6 = {:<14d}$s7 = {:<14d}".\
          format(register_list[4],register_list[5],register_list[6],register_list[7]))
    print("$t0 = {:<14d}$t1 = {:<14d}$t2 = {:<14d}$t3 = {:<14d}".\
          format(register_list[8],register_list[9],register_list[10],register_list[11]))    
    print("$t4 = {:<14d}$t5 = {:<14d}$t6 = {:<14d}$t7 = {}".\
          format(register_list[12],register_list[13],register_list[14],register_list[15]))
    print("$t8 = {:<14d}$t9 = {:<14d}".format(register_list[16],register_list[17]))
    
def get_ins():
    '''
    A function that get all the instrction, and store in a list
    '''
    #TODO
    ins_list = ["$s1,$zero,451", "$t2,$s0,73", "$t4,$s3,$s7"] 
    return ins_list 

def get_register(register_list):    
    '''
    A function that update the register, and store in a list
    '''
    #TODO
    return_list = register_list
    return return_list

def forward_no_label(): 
    '''
    A function that do the forwarding with no label
    '''    
    ins_list = get_ins() #get ins
    ins_num = len(ins_list) #num of ins
    cycle = [] #main double list
    finished_ins = 0 #num of finished ins
    register_list = [0]*18
    #build the main double list
    for i in range(16): 
        each_ins = [0]*16 
        cycle.append(each_ins)
    print("START OF SIMULATION (forwarding)")
    #start with cycle 1    
    cycle_num = 1 
    
    #main loop
    while ((cycle_num < 16) and (finished_ins != ins_num)): 
        for j in range(ins_num): 
            if((cycle_num - j) >= 0)and((cycle_num - j) <= 5): 
                cycle[j][cycle_num - 1] = cycle_num - j 
                if(cycle_num - j == 5): #WB finished this ins 
                    finished_ins += 1
                    register_list = get_register(register_list) #get register updated
                                     
        print_cycle(cycle, cycle_num, ins_num, ins_list) #print cycle
        print_register(register_list) #print register
        cycle_num += 1 #increment for cycle
    print("-"*82)
    print("END OF SIMULATION")

def forward_with_one_label(): 
    '''
    A function that do the forwarding with label
    '''    
    #TODO
    ins_list = get_ins() #get ins
    ins_num = len(ins_list) #num of ins
    cycle = [] #main double list
    finished_ins = 0 #num of finished ins
    register_list = [0]*18
    label_from,label_to=label_position()
    #build the main double list
    for i in range(16): 
        each_ins = [0]*16 
        cycle.append(each_ins)
    print("START OF SIMULATION (forwarding)")
    #start with cycle 1    
    cycle_num = 1 
    #main loop
    while ((cycle_num < 16) and (finished_ins != ins_num)): 
        for j in range(ins_num): 
            if(cycle_num < (label_from + 4)) :
                # for the instruction before label
                if ((cycle_num - j) >= 0)and((cycle_num - j) <= 5):
                    cycle[j][cycle_num - 1] = cycle_num - j 
                    if(cycle_num - j == 5): #WB finished this ins 
                        finished_ins += 1
                        register_list = get_register(register_list) #get register updated
            elif(cycle_num == label_from + 4): 
                taken = check_branch(register_list,ins_num[j])
                if not taken:#if branch is not taken
                    if((cycle_num - j) >= 0)and((cycle_num - j) <= 5):
                        cycle[j][cycle_num - 1] = cycle_num - j 
                        if(cycle_num - j == 5): #WB finished this ins 
                            finished_ins += 1
                            register_list = get_register(register_list) #get register updated
                else:#if branch is taken
                    ins_num += label_to - label_from
                    insert_index = label_from
                    insert_to_index = cycle_num - 1
                    while insert_index <= label_to:
                        ins_list.insert(insert_to_index,ins_list[insert_index])
                        insert_index += 1
                        insert_to_index +=1
                    if((cycle_num - j) >= 0)and((cycle_num - j) <= 5):
                        if(cycle_num - j == 5):
                            cycle[j][cycle_num - 1] = 5
                            finished_ins += 1
                            register_list = get_register(register_list)
                        elif(cycle_num - j == 1):
                            cycle[j][cycle_num - 1] = 1
                        else:
                            cycle[j][cycle_num - 1] = -1
            elif(cycle_num > label_from + 4)and(not taken):
                #if branch is not taken
                if ((cycle_num - j) >= 0)and((cycle_num - j) <= 5):
                    cycle[j][cycle_num - 1] = cycle_num - j 
                    if(cycle_num - j == 5): #WB finished this ins 
                        finished_ins += 1
                        register_list = get_register(register_list) #get register updated
            elif(cycle_num > label_from + 4)and(taken):
                #if branch is taken
                print("not yet")
                
                
                    
                    
                
                
                
                   
                    
                                     
        print_cycle(cycle, cycle_num, ins_num, ins_list) #print cycle
        print_register(register_list) #print register
        cycle_num += 1 #increment for cycle
    print("-"*82)
    print("END OF SIMULATION")
        
if __name__ == "__main__":
    label_num = get_label_num()
    if label_num == 0:
        forward_no_label()
    elif label_num == 1:
        forward_with_one_label()
    else:
        print("got fvcked")
