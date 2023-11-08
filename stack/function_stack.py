

class FunctionStack:

    def __init__(self):
        self.func_stack = []

    def add_to_stack(self, func, **kwargs):
        new_func = (func, kwargs)
        self.func_stack.append(new_func)
