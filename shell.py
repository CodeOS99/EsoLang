from lexer import Lexer
from parse import Parser
from interpreter import Interpreter
from data import Data
from save import Save

base = Data()
save = Save()
#ToDo   UPDATE PARSER FOR codeCoin(amount);
#ToDo   REMEMBER THERE MAY EXIST ARITHMETIC, NUMBERS, VARIABLES, AND THEM COMBINED
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
    print(text)
    tokenizer = Lexer(text,save)
    tokens = tokenizer.tokenize()
    print(tokens)
    parser = []
    tree = []
    for each in tokens:
        parser.append(Parser(each)) #make a = 1; make b = 1; if is END and printer lmao n logic lol
        #make a = 0;WHILE a<5 DO make a = a + 1 PRINT a END;
    for each in parser:
        tree.append(each.parse())
    print(tree)
    interpreter = []
    result = []
    for each in tree:
        interpreter.append(Interpreter(each, base))
    for each in interpreter:
        result.append(each.interpret())

#https://www.chess.com/analysis/game/live/94719569341?tab=review&move=45

