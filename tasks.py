HARD_TASKS = [
    {
        "task_id": "HumanEval/51",
        "prompt": """
def below_threshold(l: list, t: int):
    \"\"\" Return True if all numbers in the list l are below threshold t.
    >>> below_threshold([1, 2, 4, 10], 100)
    True
    >>> below_threshold([1, 20, 4, 10], 5)
    False
    \"\"\"
""",
        "entry_point": "below_threshold",
        "test_code": """
def check(candidate):
    assert candidate([1, 2, 4, 10], 100) == True
    assert candidate([1, 20, 4, 10], 5) == False
    assert candidate([1, 2, 3, 4], 5) == True
    assert candidate([1, 2, 3, 4], 3) == False
"""
    },
    {
        "task_id": "HumanEval/63",
        "prompt": """
def fibfib(n: int):
    \"\"\" The FibFib number sequence is a sequence similar to the Fibbonacci sequnece that's defined as follows:
    fibfib(0) == 0
    fibfib(1) == 0
    fibfib(2) == 1
    fibfib(n) == fibfib(n-1) + fibfib(n-2) + fibfib(n-3).
    Please write a function to efficiently compute the n-th element of the fibfib number sequence.
    >>> fibfib(1)
    0
    >>> fibfib(5)
    4
    >>> fibfib(8)
    24
    \"\"\"
""",
        "entry_point": "fibfib",
        "test_code": """
def check(candidate):
    assert candidate(1) == 0
    assert candidate(5) == 4
    assert candidate(8) == 24
    assert candidate(10) == 81
    assert candidate(12) == 274
    assert candidate(14) == 927
"""
    },
    {
        "task_id": "HumanEval/72",
        "prompt": """
def will_it_fly(q, w):
    '''
    Write a function that returns True if the object q will fly, and False otherwise.
    The object q will fly if it's balanced (it is a palindromic list) and the sum of its elements is less than or equal to the maximum possible weight w.

    Example:
    will_it_fly([1, 2], 5) ➞ False 
    # 1+2 is less than 5, but it's not palindromic.

    will_it_fly([3, 2, 3], 1) ➞ False
    # it's palindromic, but 3+2+3 is more than 1.

    will_it_fly([3, 2, 3], 9) ➞ True
    # 3+2+3 is less than 9, and it's palindromic.

    will_it_fly([3], 5) ➞ True
    # 3 is less than 5, and it's palindromic.
    '''
""",
        "entry_point": "will_it_fly",
        "test_code": """
def check(candidate):
    assert candidate([1, 2], 5) == False
    assert candidate([3, 2, 3], 1) == False
    assert candidate([3, 2, 3], 9) == True
    assert candidate([3], 5) == True
    assert candidate([1, 2, 3], 6) == False
    assert candidate([1, 2, 1], 4) == True
"""
    },
    {
        "task_id": "HumanEval/85",
        "prompt": """
def add(lst):
    \"\"\" Given a non-empty list of integers lst. add the odd elements that are at even indices.
    >>> add([4, 2, 6, 7])
    7
    >>> add([1, 2, 3, 4, 5])
    4
    \"\"\"
""",
        "entry_point": "add",
        "test_code": """
def check(candidate):
    assert candidate([4, 2, 6, 7]) == 7
    assert candidate([1, 2, 3, 4, 5]) == 4
    assert candidate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 16
    assert candidate([0, 1, 2, 3, 5, 6]) == 5
"""
    },
    {
        "task_id": "HumanEval/99",
        "prompt": """
def sort_array(arr):
    \"\"\"
    In this Kata, you have to sort an array of non-negative integers according to
    number of ones in their binary representation in ascending order.
    For similar number of ones, sort based on decimal value.

    It must be implemented like this:
    >>> sort_array([1, 5, 2, 3, 4]) == [1, 2, 3, 4, 5]
    >>> sort_array([-2, -3, -4, -5, -6]) == [-6, -5, -4, -3, -2]
    >>> sort_array([1, 0, 2, 3, 4]) [0, 1, 2, 3, 4]
    \"\"\"
""",
        "entry_point": "sort_array",
        "test_code": """
def check(candidate):
    assert candidate([1, 5, 2, 3, 4]) == [1, 2, 3, 4, 5]
    assert candidate([-2, -3, -4, -5, -6]) == [-6, -5, -4, -3, -2]
    assert candidate([1, 0, 2, 3, 4]) == [0, 1, 2, 3, 4]
    assert candidate([]) == []
    assert candidate([2, 5, 77, 4, 5, 3, 5, 7, 2, 3, 4]) == [2, 2, 4, 4, 3, 3, 5, 5, 5, 7, 77]
"""
    },
    {
        "task_id": "HumanEval/105",
        "prompt": """
def by_length(arr):
    \"\"\"
    Given an array of integers, sort the integers that are between 1 and 9 inclusive,
    reverse the resulting array, and then replace each digit by its corresponding name from
    "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine".

    For example:
      arr = [2, 1, 1, 4, 5, 8, 2, 3]   
            -> sort arr -> [1, 1, 2, 2, 3, 4, 5, 8] 
            -> reverse -> [8, 5, 4, 3, 2, 2, 1, 1]
      return ["Eight", "Five", "Four", "Three", "Two", "Two", "One", "One"]
    
      If the array is empty, return an empty array:
      arr = []
      return []
    
      If the array has any strange number ignore it:
      arr = [1, -1 , 55] 
            -> sort arr -> [-1, 1, 55]
            -> reverse -> [55, 1, -1]
      return = ['One']
    \"\"\"
""",
        "entry_point": "by_length",
        "test_code": """
def check(candidate):
    assert candidate([2, 1, 1, 4, 5, 8, 2, 3]) == ["Eight", "Five", "Four", "Three", "Two", "Two", "One", "One"]
    assert candidate([]) == []
    assert candidate([1, -1 , 55]) == ['One']
    assert candidate([1, 2, 3, 4, 5, 6, 7, 8, 9]) == ['Nine', 'Eight', 'Seven', 'Six', 'Five', 'Four', 'Three', 'Two', 'One']
"""
    },
    {
        "task_id": "HumanEval/112",
        "prompt": """
def reverse_delete(s,c):
    \"\"\"
    Task
    We are given two strings s and c, you have to deleted all the characters in s that are equal to any character in c then check if the result string is palindrome.
    A string is called palindrome if it reads the same backward as forward.
    You should return a tuple containing the result string and True/False for the check.
    Example
    reverse_delete("abcde","ae") should return ('bcd',False)
    reverse_delete("abcdef", "b")  should return ('acdef',False)
    reverse_delete("abcdedcba","ab") should return ('cdedc',True)
    \"\"\"
""",
        "entry_point": "reverse_delete",
        "test_code": """
def check(candidate):
    assert candidate("abcde","ae") == ('bcd',False)
    assert candidate("abcdef", "b") == ('acdef',False)
    assert candidate("abcdedcba","ab") == ('cdedc',True)
    assert candidate("dwik","w") == ('dik',False)
    assert candidate("a","a") == ('',True)
    assert candidate("abcdedcba","") == ('abcdedcba',True)
"""
    },
    {
        "task_id": "HumanEval/124",
        "prompt": """
def valid_date(date):
    \"\"\"
    You have to write a function which validates a given date string and
    returns True if the date is valid otherwise False.
    The date is valid if all of the following rules are satisfied:
    1. The date string is not empty.
    2. The number of days is not less than 1 or higher than 31 days for months 1,3,5,7,8,10,12. And the number of days is not less than 1 or higher than 30 days for months 4,6,9,11. And, the number of days is not less than 1 or higher than 29 for the month 2.
    3. The months should not be less than 1 or higher than 12.
    4. The date should be in the format: mm-dd-yyyy

    for example: 
    valid_date('03-11-2000') => True

    valid_date('15-01-2012') => False

    valid_date('04-0-2040') => False

    valid_date('06-04-2020') => True

    valid_date('06/04/2020') => False
    \"\"\"
""",
        "entry_point": "valid_date",
        "test_code": """
def check(candidate):
    assert candidate('03-11-2000') == True
    assert candidate('15-01-2012') == False
    assert candidate('04-0-2040') == False
    assert candidate('06-04-2020') == True
    assert candidate('06/04/2020') == False
    assert candidate('02-29-2001') == False
    assert candidate('02-29-2004') == True
"""
    },
    {
        "task_id": "HumanEval/138",
        "prompt": """
def is_equal_to_sum_even(n):
    \"\"\"
    Evaluate whether the given number n can be written as the sum of exactly 4 positive even numbers.
    Example
    is_equal_to_sum_even(4) == False
    is_equal_to_sum_even(6) == False
    is_equal_to_sum_even(8) == True
    \"\"\"
""",
        "entry_point": "is_equal_to_sum_even",
        "test_code": """
def check(candidate):
    assert candidate(4) == False
    assert candidate(6) == False
    assert candidate(8) == True
    assert candidate(10) == True
    assert candidate(11) == False
    assert candidate(12) == True
    assert candidate(14) == True
    assert candidate(16) == True
    assert candidate(18) == True
    assert candidate(20) == True
"""
    },
    {
        "task_id": "HumanEval/150",
        "prompt": """
def x_or_y(n, x, y):
    \"\"\"A simple program which should return the value of x if n is 
    a prime number and should return the value of y otherwise.

    Examples:
    for x_or_y(7, 34, 12) == 34
    for x_or_y(15, 8, 5) == 5
    
    \"\"\"
""",
        "entry_point": "x_or_y",
        "test_code": """
def check(candidate):
    assert candidate(7, 34, 12) == 34
    assert candidate(15, 8, 5) == 5
    assert candidate(3, 33, 5212) == 33
    assert candidate(1259, 3, 52) == 3
    assert candidate(7919, -1, 12) == -1
    assert candidate(3609, 1245, 583) == 583
    assert candidate(91, 56, 129) == 129
    assert candidate(6, 34, 1234) == 1234
"""
    }
]