from tokens import  *
class Data:
    def __init__(self):
        self.variables = {
        }
        self.functions ={
        }

    def read_var(self, id):
        return self.variables[id]
    def read_all_var(self):
        print(self.variables)
        return self.variables
    def write_var(self, variable, expression):
        variable_name = variable.value
        self.variables[variable_name] = expression


    def exec_func(self, id):
        return self.functions[id]
    def create_func(self, funcN, expression):
        func_name = funcN.value
        self.functions[func_name] = expression