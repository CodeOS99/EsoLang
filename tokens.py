class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type
    def __repr__(self):
        return str(self.value)


class Integer(Token):
    def __init__(self, value):
        super().__init__(value, "INT")


class Float(Token):
    def __init__(self, value):
        super().__init__(value, "FLT")


class Operation(Token):
    def __init__(self, value):
        super().__init__(value, "OP")

class Declarations(Token):
    def __init__(self, value):
        super().__init__(value, "DECL")

class Variable(Token):
    def __init__(self, value):
        super().__init__(value, "VAR(?)")

class Boolean(Token):
    def __init__(self, value):
        super().__init__(value, "BOOL")

class Comparison(Token):
    def __init__(self, value):
        super().__init__(value, "COMP")
class Reserved(Token):
    def __init__(self, value):
        super().__init__(value, "RSV")
class Stringy(Token):
    def __init__(self, value):
        super().__init__(value, "STR")

class Func(Token):
    def __init__(self, value):
        super().__init__(value, "DEF")