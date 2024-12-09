from AST import *
from interpreter_types import Variable, Value

class Scopes:
    def __init__(self):
        self.built_in_type_names = {"int", "float", "str", "null_type"}
        self.variable_stack = [{}]
        self.function_stack = [{}]
        self.struct_stack = [{}]
        self.variant_stack = [{}]  # ?
        self.curr_scope = 0

    def push_scope(self):

        self.curr_scope += 1
        self.variable_stack.insert(self.curr_scope, {})
        self.function_stack.insert(self.curr_scope, {})
        self.struct_stack.insert(self.curr_scope, {})
        self.variant_stack.insert(self.curr_scope, {})

    def pop_scope(self):
        if len(self.variable_stack) > 1:
            self.variable_stack.pop(self.curr_scope)
            self.function_stack.pop(self.curr_scope)
            self.struct_stack.pop(self.curr_scope)
            self.variant_stack.pop(self.curr_scope)
            self.curr_scope -= 1
        else:
            raise RuntimeError("Cannot pop the global scope")

    def reserve_place_for_(self, name : str, type_: str, is_mutable: bool):
        if name not in self.variable_stack[self.curr_scope].keys():
            self.variable_stack[self.curr_scope][name] = Variable(type_, is_mutable, None)
            return 
        raise RuntimeError(f"Variable '{name}' already declared in the current scope")
    
    def set_(self, name : str, value):
        for scope in reversed(self.variable_stack[: self.curr_scope + 1]):
            if name in scope:
                if scope[name].is_mutable or scope[name].value is None:
                    scope[name].value = value
                else:
                    raise RuntimeError("Trying to reassign value to non mutable variable")
                return
        raise RuntimeError(f"Variable '{name}' not found in any scope")
    
    def add_variable(self, name, type_, is_mutable, value):
        self.reserve_place_for_(name, type_, is_mutable)
        self.set_(name, value)

    
    def get_variable(self, name) -> Variable:
        for scope in reversed(self.variable_stack[: self.curr_scope + 1]):
            if name in scope:
                return scope[name]
        raise RuntimeError(f"Variable '{name}' not found in any scope")



    def get_var_defs_for_(self, type_: str) -> list[VariableDeclaration]:
        for scope in reversed(self.struct_stack[: self.curr_scope + 1]):
            if type_ in scope:
                return scope[type_]

        raise RuntimeError(f"Type '{type_}' not found in any scope")

    def get_named_types_for_(self, type_: str) -> list[NamedType]:
        for scope in reversed(self.variant_stack[: self.curr_scope + 1]):
            if type_ in scope:
                return scope[type_]

        raise RuntimeError(f"Type '{type_}' not found in any scope")

    def set_active_scope_to_(self, scope_idx: int):
        self.curr_scope = scope_idx  # TODO add value checking if within correct range

    def is_built_in_type_(self, type_):
        return type_ in self.built_in_type_names

    def is_type_in_stack(self, type_, stack):
        for i in range(self.curr_scope, -1, -1):
            if type_ in stack[i]:
                return True
        return False

    def is_struct_type_(self, type_):
        return self.is_type_in_stack(type_, self.struct_stack)

    def is_variant_type_(self, type_):
        return self.is_type_in_stack(type_, self.variant_stack)


    def add_function(self, func_def: FuncDef):
        name = func_def.name
        if name in self.function_stack[self.curr_scope]:
            raise RuntimeError(
                f"Function '{name}' already declared in the current scope"
            )
        self.function_stack[self.curr_scope][name] = func_def

    def get_function_definition_and_its_scope_idx(self, name):
        for idx, scope in enumerate(
            reversed(self.function_stack[: self.curr_scope + 1])
        ):
            if name in scope:
                return scope[name], len(self.function_stack) - idx - 1
        raise RuntimeError(f"Function '{name}' not found in any scope")

    def add_struct_type(self, name, attrs: List[VariableDeclaration]):
        if name in self.struct_stack[self.curr_scope]:
            raise RuntimeError(f"Type '{name}' already declared in the current scope")
        self.struct_stack[self.curr_scope][name] = attrs

    def type_exists_in_all_scopes(self, name):
        return any(name in scope for scope in self.struct_stack[: self.curr_scope + 1])

    def add_variant_type(self, name, named_types: List[NamedType]):
        if name in self.variant_stack[self.curr_scope]:
            raise RuntimeError(
                f"Variant '{name}' already declared in the current scope"
            )
        self.variant_stack[self.curr_scope][name] = named_types
