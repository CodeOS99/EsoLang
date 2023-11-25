from tokens import *


class Lexer:
    operations = "+-/*()="
    digits = "0123456789"
    stopWords = [" "]
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.!@$%^&*[],:|~"
    declarations = ["make"]
    boolean = ["and", "or", "not"]
    comparisons = [">", "<", ">=", "<=", "?=", "!="]
    specialChar = "!<>?="
    reserved = ["IF", "ELSE", "ELIF", "DO", "WHILE", "PRINT", "END", "RUN", "DEF", "|", "~", "INPUT"]
    comments = "#"
    endLine = ";"
    strings = "\""

    def __init__(self, text):
        self.text = text
        self.idx = 0
        self.tokens = []
        self.char = self.text[self.idx]
        self.token = None
        self.statements = []

    def tokenize(self):
        while self.idx < len(self.text):
            lineEnd = False
            if self.char in self.digits:
                self.token = self.extractNum()
            elif self.char in self.operations:
                self.token = Operation(self.char)
                self.move()
            elif self.char in self.stopWords:
                self.move()
                continue
            elif self.char in self.letters:
                word = self.extractWord()

                if word in Lexer.declarations:
                    self.token = Declarations(word)
                elif word in Lexer.boolean:
                    self.token = Boolean(word)
                elif word in Lexer.reserved:
                    self.token = Reserved(word)

                else:
                    self.move()
                    if self.char == "|":
                        self.token = Func(word)
                    elif self.token.type == " ":
                        self.move()
                        if self.char == "|":
                            self.token = Func(word)
                        elif self.token.type == " ":
                            self.move()
                        else:
                            self.token = Func(word)
                    else:
                        self.token = Variable(word)
            elif self.char in Lexer.specialChar:
                comparisonOp = ""
                while self.char in self.specialChar and self.idx < len(self.text):
                    comparisonOp += self.char
                    self.move()
                self.token = Comparison(comparisonOp)
            elif self.char in self.endLine:
                self.statements.append(self.tokens)
                self.tokens = []
                lineEnd = True
                self.move()
            elif self.char in self.strings:
                self.move()
                self.token = (self.extractStr())
                self.move()
                self.token = Stringy(self.token)
            """elif self.char in Lexer.comments:
                self.move()
                while self.char not in Lexer.comments:
                    self.move()
                if self.char in Lexer.comments:
                    return"""
            if not lineEnd:
                self.tokens.append(self.token)
            elif lineEnd:
                pass

        if self.char == ";" and self.statements == []:
            self.statements.append(self.tokens)
            self.tokens = []
        return self.statements

    def extractWord(self):
        word = ""
        while (self.char in Lexer.letters and self.idx < len(self.text)):
            word += self.char
            self.move()
        return word

    def extractStr(self):
        word = ""
        while ((self.char in Lexer.letters or self.char == " ") and self.idx < len(self.text) and self.char != "\""):
            word += self.char
            self.move()
        return word

    def extractNum(self):
        number = ""
        isFloat = False

        while (self.char in Lexer.digits or self.char == ".") and (self.idx < len(self.text)):
            if self.char == ".":
                isFloat = True
            number += self.char
            self.move()
        return Integer(number) if not isFloat else Float(number)

    def move(self):
        self.idx += 1
        if self.idx < len(self.text):
            self.char = self.text[self.idx]


