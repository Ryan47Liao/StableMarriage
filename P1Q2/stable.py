'''
# Submitter: bliao2 (Liao, Bowen)
# Partner: boiv (Vo, Boi Loc) 
We certify that we worked cooperatively on this programming assignment, 
according to the rules for pair programming 
'''
import prompt
from copy import copy
import goody
from envs.py36.Lib.pickle import NONE

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
    name_ordered = sorted(d,key=key, reverse=reverse)
    for name in name_ordered:
        STR += "  " + str(name) + " -> " + str(d[name]) + "\n"
    print(STR)
    return STR

def who_prefer(order : [str], p1 : str, p2 : str) -> str:
    return order[int(min(order.index(p1),order.index(p2)))]


def extract_matches(men : {str:[str,[str]]}) -> {(str,str)}:
    return { (m,men.get(m)[0]) for m in men}


def make_match(men : {str:[str,[str]]}, women : {str:[str,[str]]}, trace : bool = False) -> {(str,str)}:
    to_be_paired = copy(men)
    unmatched  = set(men) 
    if trace:
        print("\nWomen preference (unchanging)")
        dict_as_str(women)
        
        
    while len(unmatched) != 0:
        if trace:
            print("Men Preferences (current)")
            dict_as_str(to_be_paired)
            print(f"unmatched men = {unmatched}\n")
        next_guy_name = unmatched.pop()
        most_prefered_woman_name = to_be_paired.get(next_guy_name)[1].pop(0)#Get the most prefered woman poped 
        if women.get(most_prefered_woman_name)[0] is None:#If she is NOT paired
            to_be_paired[next_guy_name][0] = most_prefered_woman_name
            women[most_prefered_woman_name][0] = next_guy_name
            if trace:
                print(f"{next_guy_name} propose to {most_prefered_woman_name} (an unmatched women); so she accepts the proposal\n")
        else:
            current_partner_name = women[most_prefered_woman_name][0]
            prefered_one = who_prefer(women[most_prefered_woman_name][1],current_partner_name,next_guy_name)
            if prefered_one == next_guy_name:
                to_be_paired[next_guy_name][0] = most_prefered_woman_name
                women[most_prefered_woman_name][0] = next_guy_name
                unmatched.add(current_partner_name) 
                if trace:
                    print(f"{next_guy_name} propose to {most_prefered_woman_name} (a matched woman); she prefers her new match, so she accepts the proposal\n")
            else:
                unmatched.add(next_guy_name) 
                if trace: 
                    print(f"{next_guy_name} propose to {most_prefered_woman_name} (a matched woman); she prefers her current match, so she rejects the proposal\n")
    
    OUT = extract_matches(to_be_paired)
    if trace:
        print("Tracing option finished: final matches = ",str(OUT))
    return  OUT
        
  
    
if __name__ == '__main__':
    # Write script here
    m,w = None,None
    while m is None or w is None:
        try:
            m,w = (open(input("Input the file name detailing the preferences for men:")),
                   open(input("Input the file name detailing the preferences for women:")))
        except:
            print("Error Finding file")
    m = read_match_preferences(m)
    w = read_match_preferences(w)
    dict_as_str(m)
    dict_as_str(w)
    trace = prompt.for_bool("Input tracing algorithm option", True, "Enter False to disable tracing")
    print("The final matches = ",make_match(men=m, women=w, trace= trace))
    import driver
    driver.default_file_name = "bsc2.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
