
def print_cycle(cycle, cycle_num, ins_num, ins_list): 
    '''
    A function that do the print cycle
    '''
    print("----------------------------------------------------------------------------------")
    print("CPU Cycles ===>     1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16") 
    line_num = 0 
    while((line_num < cycle_num) and (line_num < ins_num)): 
        ins_place = 0 
        
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
            elif(cycle[line_num][ins_place] == 6): 
                line += "  *" 
            else: 
                line+= " ???" 
            ins_place += 1 
        print(line)
        line_num += 1 
        
def print_register(register_list): 
    '''
    A function that  do the print register
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

def get_register():    
    '''
    A function that update the register, and store in a list
    '''
    #TODO
    return_list = [0]*18 
    return return_list

def forward_no_label(): 
    '''
    A function that fo the forwarding with no label
    '''    
    ins_list = get_ins() #get ins
    ins_num = len(ins_list) #num of ins
    cycle = [] #main double list
    finished_ins = 0 #num of finished ins
    #build the main double list
    for i in range(16): 
        each_ins = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
        cycle.append(each_ins)
    #start with cycle 1 and IF    
    cycle_num = 1 
    cycle[0][0] = 1 
    
    #main loop
    while ((cycle_num < 16) and (finished_ins != ins_num)): 
        for j in range(ins_num): 
            if((cycle_num - j) >= 0)and((cycle_num - j) <= 5): 
                cycle[j][cycle_num - 1] = cycle_num - j 
                if(cycle_num - j == 5): #WB finished this ins 
                    finished_ins += 1
                    
        register_list = get_register()   #get register updated          
        print_cycle(cycle, cycle_num, ins_num, ins_list) #print cycle
        print_register(register_list) #print register
        cycle_num += 1 #increment for cycle
        
if __name__ == "__main__": 
    forward_no_label()
