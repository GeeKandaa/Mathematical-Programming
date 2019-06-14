# -*- coding: utf-8 -*-
"""
authors: James Lamb, Pawel Manikowski

Coursework 1

Q2 Strings handling
-------------------

Create a class called StringContainer, initialised it with a string containing only
spaces and alpha-numerical characters.

"alphanumeric characters are those comprised by the combined set of the 26 alphabetic characters, 
A to Z, and the 10 Arabic numerals, 0 to 9. " (https://whatis.techtarget.com/definition/alphanumeric-alphameric)
Therefore, all other characters will be treated as exeption.
Assumption has been made that at least one space character and one alphnumeric character were used.
A code [all(x.isalnum() or x.isspace() for x in self.text)] was copied from:
https://stackoverflow.com/questions/29460405/checking-if-string-is-only-letters-and-spaces-python    

For this exercise we used the following funcions:
    - for the split method we used split() function.
    - for the check_occurance method and get_frequancy method we used count() function
    - for the replace method we used replace() function
    - for the mirror method we used [::-1] function
"""

class StringContainer:
    def __init__(self,text):
        self.text = text
        self.n = len(text)
        if all(x.isalnum() or x.isspace() for x in self.text):
           print("String contains alphanumerical characters and spaces.")
        else:
           raise Exception("String does not contain alphanumerical characters and spaces.")         
    
    def __len__(self):
        return len(self.data)
    
    def split(self):
        print("---------------------------------SPLIT METHOD-----------------------------------")
        print(" The string: \n",self.text," \n contains the following words: \n")
        print(self.text.split())
        print("--------------------------------------------------------------------------------")
    
    def check_occurance(self,string):
        self.string = string
        print("-----------------------------CHECK OCCURANCE METHOD-----------------------------")
        print("Checking occurances for the word: ",self.string)
        if self.text.count(self.string) > 0:
            print("True") # for print purpose
            return True
        else:
            print("False") # for print purpose
            return False
        print("--------------------------------------------------------------------------------")
    
    def get_frequancy(self,string):
        print("---------------------------FREQUENCY METHOD-------------------------------------")
        self.string = string
        print("Number of occurences of the word: ",self.string," :",self.text.count(self.string))
        print("--------------------------------------------------------------------------------")
    
    def replace(self,old,new):
        self.old = old
        self.new = new
        print("-----------------------------REPLACE METHOD-------------------------------------")
        print("Old string: ", self.text)
        print(self.old," will be replaced with ", self.new)
        print("New string: ", self.text.replace(self.old, self.new))
        print("--------------------------------------------------------------------------------")
    
    def merge(self,string):
        self.string = string
        print("-----------------------------MERGE METHOD---------------------------------------")
        print(self.text + " " + self.string)
        print("--------------------------------------------------------------------------------")
    
    def mirror(self):
        print("-----------------------------MIRROR METHOD--------------------------------------")
        print("The mirror of the:\n",self.text,"\n is:")
        print(self.text[::-1])
        print("--------------------------------------------------------------------------------")
        
        
example = StringContainer("In the middle of the 1984 I was walking down the street")

example.split()
example.check_occurance("down")
example.check_occurance("up")
example.get_frequancy("the")
example.replace("the","blah")
example.merge("in the valley....")
example.mirror()

"""If you run the example below the program will terminate because '$' 
is neither a space or an alphanumeric character """
#example2 = StringContainer("blah $ blah")


