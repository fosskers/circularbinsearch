# file:    circ_bs.py
# author:  Colin Woodbury
# contact: colingw@gmail.com
# about:   A python script demonstrating circular bin search.

"""
 **************************
 * Circular Binary Search *
 **************************

 This is a binary search algorithm that works on a list
 of data that is sorted, but not linearly. That is,
 one end of the data, for whatever reason, has been
 cut off and appended to the other side.
 Example:
    [1, 2, 3, 4, 5, 6, 7, 8] becomes
    [6, 7, 8, 1, 2, 3, 4, 5]

 We refer then to the connection of 8 and 1 in the list
 above as "the link". The position of the link 
 relative to the "mid" becomes important in the search.

 *********
 * Logic *
 *********

 At first we proceed through the logic mostly as normal,
 except that instead of testing for general "less than/
 greater than" the mid point, we must test for specific 
 inclusion in the sets as follows:
   lower <= value < mid
   mid < value <= upper
 If these fail, we must move to a logic step unique to 
 circular bin search. (Marker 1)

 Here, we must determine where the "link" is
 relative to the mid point. 
 This is not difficult. (Marker 2)
 If the lower value is greater than the mid
 value, (in a normally sorted list this would
 never happen) then we know the link to be to 
 the left of mid. Otherwise, it's on the right.
 Fortunately, the target value will *always*
 be on the same side of mid as the "link".

 *********
 * Notes *
 *********

 1. This circular binary search also
 works as a normal binary search. A perfectly
 sorted list would simply never activate the
 extended logic, and things would proceed 
 as normal. 
 2. Q: 'Why not just sort the list and then search?'
    A: This isn't always possible. Take for instance searching a 50 gig
       log file for entries: sorting that isn't an option.
"""

from time import time

def circ_bs(list, target):
    '''Finds a value in a given list using a 
    circular binary search.
    Returns -1 if the value was not found.
    '''
    size = len(list)
    lower = 0
    upper = size - 1
    pos = -1  # The return value. Assume failure.
    found = False
    if size == 0:
        # Nice try.
        found = True
    while not found and lower <= upper:
        mid = (upper + lower) // 2
        if list[mid] == target:
            pos = mid
            found = True
        elif target >= list[lower] and target < list[mid]:
            upper = mid - 1
        elif target > list[mid] and target <= list[upper]:
            lower = mid + 1 
        else:  # MARKER 1
            # Standard binary search logic has failed.
            if list[lower] > list[mid]:  # MARKER 2
                upper = mid - 1
            else:
                lower = mid + 1
    return pos

def print_list(list, name):
    '''Print a given list in an easy-to-read fashion.'''
    print(name)
    print(list[0:10])
    print('... stuff in between ...')
    print(list[-10:])

def manage_search(list):
    '''Runs and times circulary bin search on a given list.'''
    start = time()
    print("Beginning search for all values in the list...")
    for each in list:
        pos = circ_bs(list, each)
        if pos == -1:
            print("{0} NOT FOUND!".format(each))
            break
    end = time()
    print("Done!")
    print("Found {0} values in {1} secs.".format(len(list), end - start))
    print()


if __name__ == '__main__':
    # Set up and search the normal list.
    list = [x for x in range(0, 1000)]
    print_list(list, "Normal list:")
    manage_search(list)

    # Split the list and re-search.
    list = list[-200:] + list[0:800]
    print_list(list, "Circular list:")
    manage_search(list)

    print("Test for len 1 list...")
    print(circ_bs([1], 1))

    print("Test for len 0 list...")
    print(circ_bs([], 1))

    print("Test for values that aren't in the list...")
    nots = [x for x in range(-1, -10, -1)]
    for each in nots:
        print("{0} -> {1}".format(each, circ_bs(list, each)))
