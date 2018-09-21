Note: This code was written in python3 via the PyCharm IDE. The code has only been tested within
the Ubuntu OS enviornment. Running the code with other OSes or with any other IDE
may lead to complications.


How to run code:
1) Make sure that python3.6, pip, jdk8 and PyCharm have been installed
    a) In the terminal type "sudo apt-get-repository ppa:deadsnakes/ppa",
       "sudo apt-get update", then type in "sudo apt-get install python3.6"
    b) In the terminal type "sudo apt install python3-pip"
    c) In the terminal, type "sudo apt install openjdk-8-jre-headless"
    d) Follow the link to download PyCharm: https://www.jetbrains.com/pycharm/download/#section=linux
        Once downloaded, there is a file with instructions on how to install PyCharm. Follow that guide.

2) Open project with the PyCharm IDE

3) You'll be prompted to configure the Python interpreter. Either click on the pop up link,
or manually go to File -> Settings -> Project: JumbleSolver -> Project Interpreter

4) On the top right, click on the wheel icon then click "Add". From There, click on "System Interpreter",
then from the drop down menu, select python3.6. Click "OK", then click on "Apply". Exit out of Settings

5) After completing it's downloading process, the IDE will prompt you to "Install requirements".
Click on the "Install requirements" button, then click "Install Anyway", then click "Install"

6) Once all the dependencies are installed, open the 'TestJumbleSolver.py' file. Running this file
will output the solution for puzzle number 1. To solve the other default puzzles, scroll to the bottom
of the file to the print statement where the 'solve_jumble_puzzle' function is, and change it's parameter
to one of any of the 5 variables already provided in the file.


Data Type of input:
In order to solve a jumble puzzle, one needs to import the JumbleSolver module and call on the
solve_jumble_puzzle() function.

This function takes in list of length 2 as it's parameter.

The first index of this list is a dictionary. The keys of this dictionary are the
the scrambled words given by the puzzle. The value of each key is a list. This is a list
of the indices of the circled characters in the unscrambled word.

The second index of this list is another list. This list is a list of numbers, where
each number is the length of each blank word that makes up the final solution.

Below is an example of how puzzle1.jpg would be represented as an input for this function:

    puzzle_1 = [
    {
     "nagld": [1, 3, 4], # the second, fourth, and 5th characters are circled
     "ramoj": [2, 3],
     "camble": [0, 1, 3],
     "wraley": [0, 2, 4]
    },
        [3,4,4]  # The final solution is a three word phrase. The first word is 3 letters long,
                 # the second word is 4 letters long, and the final word is 4 letters long
    ]