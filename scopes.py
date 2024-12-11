from AST import *
from interpreter_types import Variable, Value
from interpreter_errors import InterpreterError


class PrintProg:
    def accept(self, interpreter):
        text = interpreter.scopes.get_variable("text", (1,1)).value.value
        print(f"interpreter  >>> {text}")


class Scopes:
    def __init__(self):
        self.built_in_type_names = {"int", "float", "str", "null_type"}
        self.variable_stack = [{}]
        self.function_stack = [
            {
                "print": FuncDef(
                    "print", [Param("text", "str", False)], "null_type", PrintProg()
                )
            }
        ]
        self.struct_stack = [{}]
        self.variant_stack = [{}]  # ?
        self.curr_scope = 0

    def push_scope(self):

        self.curr_scope += 1
        self.variable_stack.insert(self.curr_scope, {})
        self.function_stack.insert(self.curr_scope, {})
        self.struct_stack.insert(self.curr_scope, {})
        self.variant_stack.insert(self.curr_scope, {})

    def pop_scope(self, pos):
        if len(self.variable_stack) > 1:
            self.variable_stack.pop(self.curr_scope)
            self.function_stack.pop(self.curr_scope)
            self.struct_stack.pop(self.curr_scope)
            self.variant_stack.pop(self.curr_scope)
            self.curr_scope -= 1
        else:
            raise InterpreterError(pos, "Cannot pop the global scope")

    def reserve_place_for_(self, name: str, type_: str, is_mutable: bool, pos):
        if name not in self.variable_stack[self.curr_scope].keys():
            self.variable_stack[self.curr_scope][name] = Variable(
                type_, is_mutable, None
            )
            return
        raise InterpreterError(
            pos, f"Variable '{name}' already declared in the current scope"
        )

    def set_(self, name: str, value, pos):
        for scope in reversed(self.variable_stack[: self.curr_scope + 1]):
            if name in scope:
                if scope[name].can_variable_be_updated():
                    scope[name].value = value
                else:
                    raise InterpreterError(
                        pos, "Trying to reassign value to non mutable variable"
                    )
                return
        raise InterpreterError(
            pos, f"Trying to assign value to not defined variable '{name}'"
        )

    def add_variable(self, name, type_, is_mutable, value, pos):
        self.reserve_place_for_(name, type_, is_mutable, pos)
        self.set_(name, value, pos)

    def get_variable(self, name, pos) -> Variable:
        for scope in reversed(self.variable_stack[: self.curr_scope + 1]):
            if name in scope:
                return scope[name]
        raise InterpreterError(pos, f"Variable '{name}' not found in any scope")

    def get_var_defs_for_(self, type_: str, pos) -> list[VariableDeclaration]:
        for scope in reversed(self.struct_stack[: self.curr_scope + 1]):
            if type_ in scope:
                return scope[type_]

        raise InterpreterError(pos, f"Type '{type_}' not found in any scope")

    def get_named_types_for_(self, type_: str, pos) -> list[NamedType]:
        for scope in reversed(self.variant_stack[: self.curr_scope + 1]):
            if type_ in scope:
                return scope[type_]

        raise InterpreterError(pos, f"Type '{type_}' not found in any scope")

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
        self.validate_type_name(func_def.type, func_def.pos)
        if name in self.function_stack[self.curr_scope]:
            raise InterpreterError(
                func_def.pos, f"Function '{name}' already declared in the current scope"
            )
        self.function_stack[self.curr_scope][name] = func_def

    def get_function_definition_and_its_scope_idx(self, name, pos):
        for idx, scope in enumerate(
            reversed(self.function_stack[: self.curr_scope + 1])
        ):
            if name in scope:
                return scope[name], len(self.function_stack) - idx - 1
        raise InterpreterError(pos, f"Function '{name}' not found in any scope")

    def add_struct_type(self, name, attrs: List[VariableDeclaration], pos):
        if name in self.struct_stack[self.curr_scope]:
            raise InterpreterError(
                pos, f"Type '{name}' already declared in the current scope"
            )
        self.struct_stack[self.curr_scope][name] = attrs

    def type_exists_in_all_scopes(self, name):
        return any(name in scope for scope in self.struct_stack[: self.curr_scope + 1])

    def add_variant_type(self, name, named_types: List[NamedType], pos):
        if name in self.variant_stack[self.curr_scope]:
            raise InterpreterError(
                pos, f"Variant '{name}' already declared in the current scope"
            )
        self.variant_stack[self.curr_scope][name] = named_types


    def validate_type_name(self, type_name :str, pos):
        if not self.is_built_in_type_(type_name) and not self.is_struct_type_(type_name) and not self.is_variant_type_(type_name):
            raise InterpreterError(pos, f"Type '{type_name}' not found")
        return True