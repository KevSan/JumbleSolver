Note: This code was written in python3 and has only been tested within the Ubuntu OS enviornment.
Running the code with other OSes may lead to complications.


How to run code:
1) Open your ubuntu terminal and change the directory so that you're in the root of this file.

2) In your terminal, run the command "pip3 install -r requirements.txt"

3) Now run "cd Tests" in order to change the directory to the Tests folder.

4) Once here, one can choose to type in "python3 TestJumboleSolver.py" to get the results
for the first puzzle, or edit the script in order to run one of the other 5 puzzles.


Data Type of input:
In order to solve a jumble puzzle, one needs to import the JumbleSolver module and call on the
solve_jumble_puzzle() function.

This function takes in list of length 2 as it's parameter.

The first index of this parameter list is a dictionary. The keys of this dictionary are the
the scrambled words given by the puzzle. The value of each key is a list of the indices that
are circled.

The second index of this paramter list is another list. This list is a list of numbers, where
each number is the length of the blank words at the bottom of the puzzle.

Below is an example of how puzzle1.jpg would be represented as an input for this function:

    puzzle_1 = [{
     "nagld": [1, 3, 4],
     "ramoj": [2, 3],
     "camble": [0, 1, 3],
     "wraley": [0, 2, 4]
    },
        [3,4,4]
    ]