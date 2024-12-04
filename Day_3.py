# %% [markdown]
# # --- Day 3: Mull It Over ---
# 
# "Our computers are having issues, so I have no idea if we have any Chief Historians in stock! You're welcome to check the warehouse, though," says the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop. The Historians head out to take a look.
# 
# The shopkeeper turns to you. "Any chance you can see why our computers are having issues again?"
# 
# The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted. All of the instructions have been jumbled up!
# 
# It seems like the goal of the program is just to multiply some numbers. It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. Similarly, mul(123,4) would multiply 123 by 4.
# 
# However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored, even if they look like part of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.
# 
# For example, consider the following section of corrupted memory:
# Tapered and 6-Step Faucet Seat Wrenches
# xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
# 
# Only the four highlighted sections are real mul instructions. Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).
# 
# Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?
# 

# %% [markdown]
# # Examples, Thoughts, and Notes
# 
# the matched patern is `mul(%3d,%3d)`
# 
# For this the trick is that if there is non `mul(` then we know we can skip to the next 4 charactors. We can also validate that the next set of charactors is 1-3 digets + `,` + 1-3 digets + `)` the min is then `mul(0,0)` -> 0 and the max is `c` ->  998001
# 
# The total tojen length is between 12 and 8 so we can always grab chunks of 8 and 12. but the first section is always `mul(` with a length of 4 and the rest min is `0,0)` with length to `999,999)`
# 
# so lets chunk this into a set of a charctor is `m` and if the next 4 and its `mul(` then we need to test the input.
# 

# %%
import logging
import re 

logger = logging.getLogger()
# fhandler = logging.FileHandler(filename='mylog.log', mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger.setFormatter(formatter)
# logger.addHandler(fhandler)
logger.setLevel(logging.DEBUG)


def test(f):
    assert( f("mul(44,46)") == 2024)
    assert( f("mul(123,4)") == (123*4) )
    assert( f("mul(4*") == None) 
    assert( f("mul(6,9!") == None)
    assert( f("?(12,34)") == None)
    assert( f("mul ( 2 , 4 )") == None)
    assert( f("xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))") == 161)

def test_do(f):
    assert(f('''xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))''') == 48)
    assert(f('''doxmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))''') == 48)
    assert(f('''n'txmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))''') == 48)
    assert(f('''n't()xmul(2,4)n't()()&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))''') == 48)


def mul(x,y):
    return x*y

def scan_text(text):
    i = 0
    text_len = len(text)
    acc = 0
    max_text=12
    min_len = 8
    ## we need to look at every leter as there might be issues with situations like '...mmul(' where the fist m does not match but it would miss if it was moved forward so we are not going to chunk it but just go 1 letter at a time to reduce the liklyhood of misses
    for i in range(text_len-min_len):
        logger.debug(f'{i},{text[i]},{text[i:i+max_text]},{acc}')

        m = re.match(r'^mul\(([0-9]{1,3}),([0-9]{1,3})\)',text[i:i+max_text])
        if (m is None) or (len(m.groups()) != 2):
            continue
        logger.debug(f'{m},{str(m.groups())}')
        acc += mul(int(m.group(1)),int(m.group(2)))

    if acc ==0: return None
    else: return acc 

def scann_text_input_do_dont(text):
    text_len = len(text)
    acc = 0
    max_text=12
    min_len = 8
    do_set = True
    dont_offset = len("n't()")
    do_offset = len('()')

    segments = text.split('do')
    
    ## we need to look at every leter as there might be issues with situations like '...mmul(' where the fist m does not match but it would miss if it was moved forward so we are not going to chunk it but just go 1 letter at a time to reduce the liklyhood of misses
    for seg, i in zip(segments, range(len(segments))):
        logger.debug(f'{seg},{i}')
        if i == 0:
            pass # inital base case is that its set
        elif seg[0:dont_offset] == "n't()":
            do_set = False
        elif seg[0:do_offset] == '()':
            do_set = True
        
        # should we be do'ing things or not?
        if do_set:
            res = scan_text(seg)
            if res is None:
                res = 0
            acc = acc + res


    if acc ==0 : return None
    else: return acc 


if __name__ == "__main__":
    import sys
    text_in = sys.argv[1]
    scann_text_input_do_dont(text_in)