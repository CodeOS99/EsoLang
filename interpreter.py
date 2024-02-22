from tokens import *
from data import Data
from lexer import Lexer
from parse import Parser
from save import Save
class Interpreter():
    def __init__(self, tree, base):
        self.tree = tree
        self.data = base
        self.cond1 = False
        self.base =  Data()
    def read_VAR(self, id):
        variable = self.data.read_var(id.value)
        variable_type = variable.type

        return getattr(self, f"read_var{variable_type}")(variable.value)
    def computeUnary(self, operator, operand):
        operand_type = "VAR" if str(operand.type).startswith("VAR") else str(operand.type)
        operand = getattr(self, f"read_var{operand_type}")(operand.value)
        if operator == "+":
            if isinstance(operand, int):
                return Integer(+operand)
            elif isinstance(operand, float):
                return Float(+operand)
        elif operator == "-":
            if isinstance(operand, int):
                return Integer(-operand)
            elif isinstance(operand, float):
                return Float(-operand)
        elif operator == "not":
            return Integer(1) if not operand else Integer(0)
    def interpret(self, tree=None):
        if tree is None:
            tree = self.tree

        if isinstance(tree, str):
            return Stringy(tree)
        if isinstance(tree, list):
            if isinstance(tree[0], list):
                for i in tree:
                    self.interpret(i)
                return
            if isinstance(tree[0], Reserved) or isinstance(tree[0], Func):
                if tree[0].value == "IF":
                    for idx, condition in enumerate(tree[1][0]):
                        eval = self.interpret(condition)
                        if eval.value == 1:
                            return self.interpret(tree[1][1][idx])
                    if len(tree[1]) == 3:
                        return self.interpret(tree[1][2])
                    else:
                        return
                elif tree[0].value == "WHILE":
                    condition = tree[1][0]
                    conditionVal = self.interpret(condition).value
                    actions = (tree[1][1])
                    while conditionVal == 1:
                        for each in actions:
                            action = self.interpret(each)
                        conditionVal = self.interpret(condition).value
                    return
                elif tree[0].value == "PRINT":
                    i=0
                    if True:
                        x = ""
                        while i < len(tree[1]):
                            if tree[1][i].type.startswith("VAR"):
                                x+=str(self.read_VAR(tree[1][i]))
                            else:
                                x+=tree[1][i].value
                            i+=1
                        x = self.interpret(x)
                        print((x.value))

                    return
                elif tree[0].value == "RUN":
                    query = tree[1]
                    stopWords = {'\n'}
                    resultwords = query.split('\n')
                    x = ""
                    for each in resultwords:
                        if each not in stopWords:
                            x+=each
                        else:
                            for i in range(each):
                                if i <2:
                                    pass
                                else:
                                    x+= each[i]
                        x+=" "
                    tokenizeDeez = Lexer(x, Save())
                    tokens = tokenizeDeez.tokenize()
                    parser = []
                    tree = []
                    for each in tokens:
                        parser.append(Parser(each))  # make a = 1; make b = 1; if is END and printer lmao n logic lol
                        # WHILE a<5 DO make a = a + 1; PRINT a; END
                    for each in parser:
                        tree.append(each.parse())

                    interpreter = []
                    result = []
                    for each in tree:
                        interpreter.append(Interpreter(each, self.base))
                    for each in interpreter:
                        result.append(each.interpret())
                    return
                elif tree[0].type == "DEF":
                    #args setter first because want it to monkr
                    for i in tree[1]:
                        self.interpret(i)
                    self.interpret(self.data.exec_func(tree[0].value))
                    return
                elif tree[0].value == "DEF" and tree[0].type == "RSV":
                    name = tree[1][0]
                    n = []
                    for i in tree[1][1]:
                        if i.type == "DECL":
                            n.append([])
                        else:
                            n[-1].append(i)
                    for i in n:
                        args = self.interpret(i)
                    ToDo = tree[1][2]
                    self.data.create_func(name, ToDo)
                    return
                elif tree[0].value == "INPUT":
                    for i in tree[1]:
                        print(i.value)
                    yes = input()
                    if isinstance(yes, str):
                        return Stringy(yes)
                    elif isinstance(yes, int):
                        return self.interpret(Integer(yes))
                    elif isinstance(yes, float):
                        return self.interpret(Float(yes))

        if isinstance(tree, list) and len(tree) == 2 and not self.cond1:
            expression = tree[1]
            if isinstance(expression, list):
                expression = self.interpret(expression)
            return self.computeUnary(tree[0], expression)
        elif not isinstance(tree, list):
            return tree
        else:
            i = 0
            if tree[0].value == "make":
                i = 1
            else:
                i = 0
            left_node = tree[i]

            if isinstance(left_node, list):
                left_node = self.interpret(left_node)

            right_node = tree[i+2]

            if isinstance(right_node, list):
                right_node = self.interpret(right_node)

            operator = tree[i+1]

            return self.computeBin(left_node, operator, right_node)

    def read_varINT(self, value):
        return int(value)

    def read_varFLT(self, value):
        return float(value)
    def read_varSTR(self, value):
        return str(value)
    def computeBin(self, left, op, right):
        left_type = "VAR" if str(left.type).startswith("VAR") else str(left.type)
        right_type = "VAR" if str(right.type).startswith("VAR") else str(right.type)
        # Make inputs work
        if op.value == "=":
            left.type = f"VAR({right_type})"
            if left.type != "VAR(VAR)":
                self.data.write_var(left, right)
            elif left.type == "VAR(VAR)":
                self.data.write_var(left, self.data.read_var(right.value))
            return self.data.read_all_var()
        if left_type == "VAR":
            left = getattr(self, f"read_VAR")(left)
        else:
            left = getattr(self, f"read_var{left_type}")(left.value)

        if right_type == "VAR":
            right = getattr(self, f"read_VAR")(right)
        else:
            right = getattr(self, f"read_var{right_type}")(right.value)

        match op.value:
            case "+":
                output = left + right
            case "-":
                output = left - right
            case "*":
                output = left * right
            case "/":
                output = left / right
            case ">":
                output = left > right
            case "<":
                output = 1 if left < right else 0
            case "?=":
                output = 1 if left == right else 0
            case "!=":
                output = 1 if left != right else 0
            case "and":
                output = 1 if left and right else 0
            case "or":
                output = 1 if left or right else 0

        if isinstance(left, int):
            return Integer(output)
        elif isinstance(left, float):
            return Integer(output)
        elif isinstance(right, float):
            return Float(output)
        elif isinstance(right, int):
            return Integer(output)

