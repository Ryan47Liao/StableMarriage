'''
# Submitter: bliao2 (Liao, Bowen)
# Partner: boiv (Vo, Boi Loc) 
We certify that we worked cooperatively on this programming assignment, 
according to the rules for pair programming 
'''
import prompt
from copy import copy
import goody

# Use these global variables to index the list associated with each name in the dictionary.
# e.g., if men is a dictionary, men['m1'][match] is the woman who matches man 'm1', and 
# men['m1'][prefs] is the list of preference for man 'm1'.
# It would seems that this list might be better represented as a named tuple, but the
# preference list it contains is mutated, which is not allowed in a named tuple. 

match = 0   # Index 0 of list associate with name is match (str)
prefs = 1   # Index 1 of list associate with name is preferences (list of str)


def read_match_preferences(open_file : open) -> {str:[str,[str]]}:
    Dict = {}
    for line in open_file:
        line = line.rstrip('\n')
        Dict[line.split(';')[0]] = [None, list(line.split(';')[1:])]
    return Dict


def dict_as_str(d : {str:[str,[str]]}, key : callable=None, reverse : bool=False) -> str:
    STR = ''
    for name, preference in sorted(d.items(), key=key, reverse=reverse):
        STR += "  " + str(name) + " -> " + str(preference) + "\n"
    print(STR)
    return STR

def who_prefer(order : [str], p1 : str, p2 : str) -> str:
    return order[int(min(order.index(p1),order.index(p2)))]


def extract_matches(men : {str:[str,[str]]}) -> {(str,str)}:
    return { (men.get(m)[0],m) for m in men}


def make_match(men : {str:[str,[str]]}, women : {str:[str,[str]]}, trace : bool = False) -> {(str,str)}:
    to_be_paired = copy(men)
    unmatched  = set(men) 
    if trace:
        print("Women preference (Unchanging)\n")
        dict_as_str(women)
    while len(unmatched) != 0:
        if trace:
            print("men preference (Unchanging)\n")
            dict_as_str(to_be_paired)
            print("")
        next_guy_name = unmatched.pop()
        most_prefered_woman_name = to_be_paired.get(next_guy_name)[1].pop(0)#Get the most prefered woman poped 
        if women.get(most_prefered_woman_name)[0] is None:#If she is NOT paired
            to_be_paired[next_guy_name][0] = most_prefered_woman_name
            if trace:
                print(f"{next_guy_name} propose to {most_prefered_woman_name} (unmantched women);", end="")
        else:
            current_partner_name = women[most_prefered_woman_name][0]
            prefered_one = who_prefer(women[most_prefered_woman_name][1],current_partner_name,next_guy_name)
            if prefered_one == next_guy_name:
                to_be_paired[next_guy_name][0] = most_prefered_woman_name
                unmatched.add(current_partner_name) 
                if trace:
                    #print(f"{next_guy_name} propose to {most_prefered_woman_name}")
            else:
                unmatched.add(next_guy_name) 
        if trace:
            dict_as_str(to_be_paired)
            print("\n"+str(unmatched))
            

    #Done
    return  extract_matches(to_be_paired)
        
    
    


  
    
if __name__ == '__main__':
    # Write script here
    d = read_match_preferences(open('men0.txt'))
    m = read_match_preferences(open('women0.txt'))
    #print(sorted(d))     
    print(dict_as_str(d))  
    print(who_prefer(['w3','w1','w2'], 'w2', 'w3'))  
    # For running batch self-tests
    print(make_match(men = m, women = d))
    import driver
    #driver.default_file_name = "bsc2.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    #driver.driver()
