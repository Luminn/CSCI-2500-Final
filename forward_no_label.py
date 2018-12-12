import input
import sys
import mint
def check_branch(register_list,ins):
    '''
    A function that determine if the branch is taken
    '''  

    branchType = ""

    register_dict = {"$s0": 0, "$s1": 1, "$s2": 2, "$s3": 3, "$s4": 4, "$s5": 5,
                     "$s6": 6, "$s7": 7, "$t0": 8,
                     "$t1": 9, "$t2": 10, "$t3": 11, "$t4": 12, "$t5": 13,
                     "$t6": 14, "$t7": 15, "$t8": 16, "$t9": 17, "$zero": -1
                     }
    temp=ins.split()
    if(len(temp)<2):
        pass
    else:
        branchType=temp[0]
        temp=temp[1].split(',')
        temp[0]=temp[0].strip("$")
        temp[1]=temp[1].strip("$")
        
      
        a=register_list[temp[0]]
        b=register_list[temp[1]]
        
        if branchType == "beq":
            return a==b
        elif branchType == "bne":
            return a!=b

    return False

def get_label_num():
    '''
    A function that get number of label
    '''  
    argv=sys.argv
    tran_dict = input.parse_file(argv[2])[1]
    label_num = len(tran_dict)
    return label_num

def label_position():
    '''
    A function that get label position
    '''
    file_name = str(sys.argv[2])
    a=input.list_labels(input.parse_file(file_name)[0])
    
    return (a[0][1],a[0][0])

def print_cycle(cycle, cycle_num, ins_num, ins_list): 
    '''
    A function that do the print cycle
    '''
    print("-"*82)
    print("CPU Cycles ===>     1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16") 
    line_num = 0 #row num of cycle
    while((line_num < cycle_num) and (line_num < ins_num)): 
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
        
def print_register(register_list): 
    '''
    A function that do the print register
    '''
    print(register_list)
    
def get_ins():
    '''
    A function that get all the instrction, and store in a list
    '''

    ins_list,tran_dict = input.parse_file("test.txt")
    for x in range(len(ins_list)):
        if(ins_list[x][0] == "bne") or (ins_list[x][0] == "beq" ):
            ins_list[x][3]= tran_dict[int(ins_list[x][3])]
    
    res=[]
    
    for x in ins_list:
        res.append(input.instruction_to_string(x))
    return res

def get_register(register_list,ins):    
    '''
    A function that update the register, and store in a list
    '''
    mint.apply_instruction(ins,register_list)



def forward_no_label(): 
    '''
    A function that do the forwarding with no label
    '''    
    register_list=mint.menv()
    ins_list = get_ins() #get ins
    ins_num = len(ins_list) #num of ins
    cycle = [] #main double list
    finished_ins = 0 #num of finished ins
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
                    get_register(register_list,instruction_split(ins_list[j])) #get register updated
                                     
        print_cycle(cycle, cycle_num, ins_num, ins_list) #print cycle
        print_register(register_list) #print register
        cycle_num += 1 #increment for cycle
    print("-"*82)
    print("END OF SIMULATION")

def instruction_split(ins):
    res=[0,0,0,0]
    temp=ins.split()
    res[0]=temp[0]
    temp=temp[1].split(",")
    res[1]=temp[0].strip("$")
    res[2]=temp[1].strip("$")
    res[3]=temp[2].strip("$")
    
    return res

def forward_with_one_label(): 
    '''
    A function that do the forwarding with label
    '''    
    register_list=mint.menv()
    ins_list = get_ins() #get ins
    ins_num = len(ins_list) #num of ins
    cycle = [] #main double list
    finished_ins = 0 #num of finished ins
    label_from,label_to=label_position()
    #build the main double list
    for i in range(16): 
        each_ins = [0]*16 
        cycle.append(each_ins)
    print("START OF SIMULATION (forwarding)")
    #start with cycle 1    
    cycle_num = 1 
    #main loop
    while ((cycle_num <= 16) and (finished_ins != ins_num)): 
        if(cycle_num < (label_to + 5)) :
            for j in range(ins_num):
                # for the instruction before label
                if ((cycle_num - j) >= 0)and((cycle_num - j) <= 5):
                    cycle[j][cycle_num - 1] = cycle_num - j 
                    if(cycle_num - j == 5): #WB finished this ins 
                        finished_ins += 1
                        get_register(register_list,instruction_split(ins_list[j])) #get register updated
        elif(cycle_num == label_to + 5): 
            taken = check_branch(register_list,ins_list[label_to])
            #taken = True
            if not taken:#if branch is not taken
                for j in range(ins_num):
                    if((cycle_num - j) >= 0)and((cycle_num - j) <= 5):
                        cycle[j][cycle_num - 1] = cycle_num - j 
                        if(cycle_num - j == 5): #WB finished this ins 
                            finished_ins += 1
                            get_register(register_list,instruction_split(ins_list[j])) #get register updated
            else:#if branch is taken
                insert_index = label_from
                insert_to_index = cycle_num - 1
                while insert_index <= ins_num:
                    ins_list.insert(insert_to_index,ins_list[insert_index])
                    insert_index += 1
                    insert_to_index +=1
                ins_num += (ins_num - label_from)
                for j in range(ins_num):
                    if((cycle_num - j) >= 0)and((cycle_num - j) <= 5):
                        if(cycle_num - j == 5):
                            cycle[j][cycle_num - 1] = 5
                            finished_ins += 1
                            get_register(register_list,ins_list[j])
                        elif(cycle_num - j == 1):
                            cycle[j][cycle_num - 1] = 1
                        elif(cycle_num - j == 0):
                            cycle[j][cycle_num - 1] = 0                        
                        else:
                            cycle[j][cycle_num - 1] = -1

        elif(cycle_num > label_to + 5)and(not taken):
            #if branch is not taken
            for j in range(ins_num):
                if ((cycle_num - j) >= 0)and((cycle_num - j) <= 5):
                    cycle[j][cycle_num - 1] = cycle_num - j 
                    if(cycle_num - j == 5): #WB finished this ins 
                        finished_ins += 1
                        get_register(register_list,instruction_split(ins_list[j])) #get register updated
        elif(cycle_num > label_to + 5)and(taken):
            if(cycle_num == label_to + 5 + 4 + label_to - label_from): 
                taken = check_branch(register_list,ins_list[label_to])
                #taken = True                
                if not taken:#if branch is not taken
                    for j in range(ins_num):
                        if((cycle_num - j) >= 0)and((cycle_num - j) <= 5):
                            cycle[j][cycle_num - 1] = cycle_num - j 
                            if(cycle_num - j == 5): #WB finished this ins 
                                finished_ins += 1
                                get_register(register_list,instruction_split(ins_list[j])) #get register updated
                else:#if branch is taken
                    insert_index = label_from
                    insert_to_index = cycle_num - 1
                    while insert_index <= ins_num:
                        ins_list.insert(insert_to_index,ins_list[insert_index])
                        insert_index += 1
                        insert_to_index +=1
                    ins_num += (ins_num - label_from)
                    for j in range(min(16,ins_num)):
                        if((cycle_num - j) >= 0)and((cycle_num - j) <= 5 and (cycle_num<=16)):
                            if(cycle_num - j == 5):
                                cycle[j][cycle_num - 1] = 5
                                finished_ins += 1
                                get_register(register_list,ins_list[j])
                            elif(cycle_num - j == 1):
                                cycle[j][cycle_num - 1] = 1
                            elif(cycle_num - j == 0):
                                cycle[j][cycle_num - 1] = 0                        
                            else:
                                cycle[j][cycle_num - 1] = -1            
            else:
                #if branch is taken
                for j in range(ins_num):
                    if ((cycle_num - j) >= 0)and((cycle_num - j) <= 5):
                        if cycle[j][cycle_num - 2] == -1:
                            cycle[j][cycle_num - 1] = -1
                        else:
                            cycle[j][cycle_num - 1] = cycle_num - j
                            if(cycle_num - j == 5): #WB finished this ins 
                                finished_ins += 1
                                get_register(register_list,instruction_split(ins_list[j])) #get register updated
                    
                        
                                     
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
