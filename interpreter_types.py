class Variable:
    def __init__(self, type_, is_mutable, value):
        self.type = type_
        self.is_mutable = is_mutable
        self.value = value

    def is_initialised(self):
        return self.value is not None

    def can_variable_be_updated(self):
        return not self.is_initialised() or self.is_mutable

    def update_value(self, new_value):
        self.value = new_value


class Value:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value


class BuiltInValue(Value):
    pass


class StructValue(Value):
    """Holds only initialised attributes"""

    def __init__(self, type_: str, value: dict[str, Variable]):
        super().__init__(type_, value)

    def __getitem__(self, attr_name):
        return self.value[attr_name].value

    def update_value_of_attr(self, attr_name, new_value):
        self.value[attr_name].value = new_value

    def add_attr(self, attr_name, variable):
        self.value[attr_name] = variable

    
    def get_inner_variable(self, attr_name):
        return self.value[attr_name]
    
    def is_attr_in_(self, attr_name):
        return attr_name in self.value.keys()
    
    def get_concrete_type(self):
        return self.type


class VariantValue(Value):
    def __init__(self, type_: str, value, name):
        super().__init__(type_, value)
        self.name = name

    def __getitem__(self, attr_name):
        return self.value.value[attr_name]
    
    def add_attr(self, attr_name, variable):
        self.value.value[attr_name] = variable

    def get_inner_variable(self, attr_name):
        return self.value.get_inner_variable(attr_name)
    
    def is_attr_in_(self, attr_name):
        return self.value.is_attr_in_(attr_name)

    def get_concrete_type(self):
        return self.value.get_concrete_type()