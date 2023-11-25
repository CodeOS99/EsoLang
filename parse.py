from tokens import *
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
        self.token = self.tokens[self.idx]

    def factor(self):
        if self.token.type == "STR":
            return self.token
        elif self.token.type == "INT" or self.token.type == "FLT":
            return self.token
        elif self.token.value == "(":
            self.move()
            expression = self.boolean_expression()
            return expression
        elif self.token.value == "not":
            operator = self.token
            self.move()
            return [operator, self.boolean_expression()]
        elif self.token.type.startswith("VAR"):
            return self.token
        elif self.token.value == "+" or self.token.value == "-":
            operator = self.token.value
            self.move()
            operand = self.boolean_expression()

            return [operator, operand]

    def term(self):
        left_node = self.factor()
        self.move()
        output = left_node
        while self.token.value == "*" or self.token.value == "/":
            operation = self.token
            self.move()
            right_node = self.factor()
            self.move()
            left_node = [left_node, operation, right_node]
        return left_node

    def comp_expression(self):
        left_node = self.expression()
        while self.token.type == "COMP":
            operation = self.token
            self.move()
            right_node = self.comp_expression()
            left_node = [left_node, operation, right_node]
        return left_node
    def boolean_expression(self):
        left_node = self.comp_expression()
        while self.token.type == "BOOL":
            operation = self.token
            self.move()
            right_node = self.expression()
            left_node = [left_node, operation, right_node]
        return left_node
    def expression(self):
        left_node = self.term()
        while self.token.value == "+" or self.token.value == "-":
            operation = self.token
            self.move()
            right_node = self.term()
            left_node = [left_node, operation, right_node]
        return left_node
    def if_statement(self):
        self.move()
        condition = self.boolean_expression()

        if self.token.value == "DO":
            self.move()
            action = self.statement()

            return condition, action
        elif self.tokens[self.idx - 1].value == "DO":
            action = self.statement()
            return condition, action
    def if_statements(self):
        conditions = []
        actions = []
        if_statement = self.if_statement() # !! NO S, IF STATMENTS AND IF STATEMENT IS DIFFERENT !!
        conditions.append(if_statement[0])
        actions.append(if_statement[1])
        while self.token.value == "elif":
            if_statement = self.if_statement()
            conditions.append(if_statement[0])
            actions.append(if_statement[1])
        if self.token.value == "else":
            self.move()
            self.move()
            else_action = self.statement()
            return [conditions, actions, else_action]
        return [conditions, actions]
    def while_statement(self, loopN=1):
        self.move()
        condition = (self.boolean_expression())
        actions = []
        if self.token.value == "DO":
            self.move()
            n = 0
            while self.token.value != "END":
                action = self.statement(loopN + 1)
                actions.append(action)
                if self.token.type == "DECL" or self.token.type == "RSV":  # works only for ONE NESTED LOOP(ie, 2nd loop, not first!!!!)
                    pass
                else:
                    self.move()
                n += 1
            if self.token.value == "END":
                self.move()
            return [condition, actions]
        elif self.tokens[self.idx-1].value == "DO":
            n = 0
            while self.token.value != "END":
                action = self.statement(loopN + 1)
                actions.append(action)
                if self.token.type == "DECL" or self.token.type == "RSV":  # works only for ONE NESTED LOOP(ie, 2nd loop, not first!!!!)
                    pass
                else:
                    self.move()
                n += 1

    def printer(self):
        args = []
        self.move()
        while self.idx<(len(self.tokens)):
            if self.token.type!="DECL" and self.token.type!="RSV":
                args.append(self.token)
                self.move()
            else:
                break
        return args
    def statement(self, loopN=1):
        if self.token.type == "STR":
            return self.token
        elif self.token.type == "DECL":
            self.move()
            left_node = self.variable()
            self.move()
            if self.token.value == "=":
                operation = self.token
                self.move()
                right_node = self.statement()

                return [left_node, operation, right_node]
        elif (
            self.token.type == "INT"
            or self.token.type == "FLT"
            or self.token.type == "OP"
            or self.token.type == "not"
        ):
            return self.boolean_expression()
        elif self.token.value == "IF":
            return [self.token, self.if_statements()]
        elif self.token.value == "WHILE":
            return [self.token, self.while_statement(loopN)]
        elif isinstance(self.token, list):
            self.statement()
        elif self.token.value == "PRINT":
            return [self.token, self.printer()]
        elif self.token.type == "STR":
            return self.token
        elif self.token.value == "RUN":
            return self.run()
        elif self.token.value == "DEF":
            return [self.token, self.defFunc()]
        elif self.token.type == "DEF" and self.token.value != "DEF":
            return [self.token, self.runFunc()]
        elif self.token.value == "INPUT":
            return[self.token, self.runInput()]

    def runInput(self):
        args = []
        self.move()
        while self.idx < (len(self.tokens)):
            if self.token.type != "DECL" and self.token.type != "RSV":
                args.append(self.token)
                self.move()
            else:
                break
        return args
    def runFunc(self):
        name = self.token.value
        self.move()
        args = []
        if self.token.value == "|":
            self.move()
            while self.token.value != "|":
                args.append(self.parse())
        return args
    def defFunc(self):
        self.move()
        name = Func(self.token.value)
        self.move()
        args = []
        """
        """
        if self.token.value == "|":
            self.move()
            while self.token.value != "|":
                args.append((self.token))
                self.move()
        actions = []
        self.move()
        if self.token.value == "~":
            self.move()
            n = 0
            while self.token.value != "END":
                action = self.statement()
                actions.append(action)
                if self.token.type == "DECL" or self.token.type == "RSV":  # works only for ONE NESTED LOOP(ie, 2nd loop, not first!!!!)
                    pass
                else:
                    self.move()
                n += 1
            if self.token.value == "END":
                self.move()
            return [name, args, actions]
        elif self.tokens[self.idx - 1].value == "~":
            n = 0
            while self.token.value != "END":
                action = self.statement()
                actions.append(action)
                if self.token.type == "DECL" or self.token.type == "RSV":  # works only for ONE NESTED LOOP(ie, 2nd loop, not first!!!!)
                    pass
                else:
                    self.move()
                n += 1
            return [name, args, actions]
    def run(self):
        self.move()
        fileName = self.token.value
        f = open(fileName, "r")
        return [Reserved("RUN"), f.read()]

    def variable(self):
        if self.token.type.startswith("VAR"):
            return self.token

    def parse(self):
        return self.statement()

    def move(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.token = self.tokens[self.idx]
    def get(self, offset):
        return self.token[self.idx+offset]