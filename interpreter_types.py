class Variable:
    def __init__(self, type_, is_mutable, value):
        self.type = type_
        self.is_mutable = is_mutable
        self.value = value




class Value:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
        