from lexer import Lexer
from parse import Parser
from interpreter import Interpreter
from data import Data

base = Data()
#ToDo   MULTILINER FUNCTIONS, ALSO GJ ON FUNCTIONS :D
while True:
    text = input('''
  ______           _____           _       _   
 |  ____|         / ____|         (_)     | |  
 | |__   ___  ___| (___   ___ _ __ _ _ __ | |_ 
 |  __| / __|/ _ \\\\___ \ / __| '__| | '_ \| __|
 | |____\__ \ (_) |___) | (__| |  | | |_) | |_ 
 |______|___/\___/_____/ \___|_|  |_| .__/ \__|
                                    | |        
                                    |_|        
'''
)
    tokenizer = Lexer(text)
    tokens = tokenizer.tokenize()
    print(tokens)
    parser = []
    tree = []
    for each in tokens:
        parser.append(Parser(each)) #make a = 1; make b = 1; if is END and printer lmao n logic lol
        #WHILE a<5 DO make a = a + 1; PRINT a; END
    for each in parser:
        tree.append(each.parse())
    print(tree)
    interpreter = []
    result = []
    for each in tree:
        interpreter.append(Interpreter(each, base))
    for each in interpreter:
        result.append(each.interpret())

#https://www.chess.com/analysis/game/live/94117956907?tab=review&move=107

