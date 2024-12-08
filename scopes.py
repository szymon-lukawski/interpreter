from AST import *


class Scopes:

    class Symbol:
        def __init__(self, type_: str, is_mutable: bool, value):
            self.type = type_
            self.is_mutable = is_mutable
            self.value = value

            # self.value = value -> self.build_up_symbol_structure then self.set_value
            # Build up symbol structure then compare this structure with `value` structure and update it accordingly
            # Type cycle ->   A : struct begin b : B; end B: struct begin a: A; end
            # Type should take into account its position -> self.push_counter as a second identifier (type_name, self.push_counter)

        def set_value(self, address: list[str], new_value):
            # check structure with coresponding value structure
            if not self.is_mutable and self.value is not None:
                raise RuntimeError("Trying to reassign value to non mutable variable")
            self._set_value(address, new_value)

        def get_value(self, address: list[str]):
            raise NotImplementedError

        def __eq__(self, value):
            return (
                self.type == value.type
                and self.is_mutable == value.is_mutable
                and self.value == value.value
            )

    class BuiltInSymbol(Symbol):
        def __init__(self, type_, is_mutable, value):
            super().__init__(type_, is_mutable, value)

        def accept(self, visitor):
            return visitor.visit_built_in_instance(self)

        def _set_value(self, address: list[str], new_value):
            self.value = new_value.value

        def get_value(self, address: list[str]):
            if len(address) > 0:
                raise RuntimeError("Trying to address simple types")
            return self.value

    class StructSymbol(Symbol):
        def __init__(self, type_, is_mutable, value: dict):
            super().__init__(type_, is_mutable, value)

        def accept(self, visitor):
            return visitor.visit_struct_instance(self)

        def _set_value(self, address: list[str], new_value):
            if len(address) == 0:
                self.value = new_value.value  # TODO Add checking
                return
            first_address = address[0]
            rest_address = address[1:]
            if rv := self.value.get(first_address):
                return rv.set_value(rest_address, new_value)
            raise RuntimeError(
                f"Attribute '{first_address}' not found in type '{self.type}'"
            )

        def get_value(self, address: list[str]):
            if len(address) == 0:
                return self
            first_address = address[0]
            rest_address = address[1:]
            if rv := self.value.get(first_address):
                return rv.get_value(rest_address)
            raise RuntimeError(
                f"Attribute '{first_address}' not found in type '{self.type}'"
            )

        def attrs(self):
            return self.value.keys()

    class VariantSymbol(Symbol):
        def __init__(self, type_, is_mutable, value):
            super().__init__(type_, is_mutable, value)
            self.curr_active: str = None

        def accept(self, visitor):
            return visitor.visit_variant_instance(self)

        def _set_value(self, address: list[str], new_value):
            if len(address) == 0:
                self.curr_active = new_value.type
                self.value[new_value.type] = new_value.value  # TODO Add checking
                return
            first_address = address[0]
            rest_address = address[1:]
            if rv := self.value[self.curr_active].get(first_address):
                return rv.set_value(rest_address, new_value)
            raise RuntimeError(
                f"Attribute '{first_address}' not found in type '{self.type}'"
            )

        def get_value(self, address: list[str]):
            if len(address) == 0:
                return self.value[self.curr_active]
            first_address = address[0]
            rest_address = address[1:]
            if rv := self.value[self.curr_active].get(first_address):
                return rv.get_value(rest_address)
            raise RuntimeError(
                f"Attribute '{first_address}' not found in type '{self.value[self.curr_active].type}'"
            )

    def __init__(self):
        self.built_in_type_names = {"int", "float", "str", "null_type"}
        self.variable_stack = [{}]
        self.function_stack = [{}]
        self.struct_stack = [{}]
        self.variant_stack = [{}]  # ?
        self.curr_scope = 0

    def push_scope(self):
        self.variable_stack.append({})
        self.function_stack.append({})
        self.struct_stack.append({})
        self.variant_stack.append({})
        self.curr_scope += 1

    def pop_scope(self):
        if len(self.variable_stack) > 1:
            self.variable_stack.pop()
            self.function_stack.pop()
            self.struct_stack.pop()
            self.variant_stack.pop()
            self.curr_scope -= 1
        else:
            raise RuntimeError("Cannot pop the global scope")

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

    def create_symbol(self, type_, is_mutable):
        if self.is_built_in_type_(type_):
            return self.create_built_in_symbol(type_, is_mutable)
        elif self.is_struct_type_(type_):
            return self.create_struct_symbol(type_, is_mutable)
        elif self.is_variant_type_(type_):
            return self.create_variant_symbol(type_, is_mutable)
        raise RuntimeError(f"Type '{type_}' not found in any scope")

    def create_built_in_symbol(self, type_, is_mutable):
        return Scopes.BuiltInSymbol(type_, is_mutable, None)

    def create_struct_symbol(self, type_, is_mutable):
        attrs_dict: dict[str, Scopes.Symbol] = dict()
        var_defs = self.get_var_defs_for_(type_)
        for var_def in var_defs:
            attrs_dict[var_def.name] = self.create_symbol(
                var_def.type, var_def.is_mutable
            )
        return Scopes.StructSymbol(type_, is_mutable, attrs_dict)

    def create_variant_symbol(self, type_, is_mutable):
        variant_dict: dict[str, Scopes.Symbol] = dict()
        named_types = self.get_named_types_for_(type_)
        for named_type in named_types:
            variant_dict[named_type.name] = self.create_symbol(
                named_type.type, True
            )  # Variant is always mutable?
        return Scopes.VariantSymbol(type_, is_mutable, variant_dict)

    def add_variable(self, name, type_, is_mutable, init_value):
        if name in self.variable_stack[self.curr_scope]:
            raise RuntimeError(
                f"Variable '{name}' already declared in the current scope"
            )
        symbol = self.create_symbol(type_, is_mutable)
        if init_value is not None:
            if self.is_literal(init_value):
                init_value = self.convert_literal_to_symbol(init_value)
            symbol.set_value([], init_value)
        self.variable_stack[self.curr_scope][name] = symbol

    def variable_exists_in_current_scope(self, name):
        return name in self.variable_stack[self.curr_scope]

    def get_symbol(self, name):
        for scope in reversed(self.variable_stack[: self.curr_scope + 1]):
            if name in scope:
                symbol = scope[name]
                return symbol
        raise RuntimeError(f"Variable '{name}' not found in any scope")

    def set_variable_value(self, name_chain, value):
        name = name_chain[0]
        for scope in reversed(self.variable_stack[: self.curr_scope + 1]):
            if name in scope:
                symbol: Scopes.Symbol = scope[name]
                if self.is_literal(value):
                    value = self.convert_literal_to_symbol(value)
                symbol.set_value(name_chain[1:], value)
                return
        raise RuntimeError(f"Variable '{name}' not found in any scope")
    
    def is_literal(self, value):
        return isinstance(value, int) or isinstance(value, float) or isinstance(value, str)

    def convert_literal_to_symbol(self, literal):
        if isinstance(literal, int):
            return Scopes.BuiltInSymbol("int", False, literal)
        if isinstance(literal, float):
            return Scopes.BuiltInSymbol("float", False, literal)
        if isinstance(literal, str):
            return Scopes.BuiltInSymbol("str", False, literal)
        raise NotImplementedError
        

    def add_function(self, func_def: FuncDef):
        name = func_def.name
        if name in self.function_stack[self.curr_scope]:
            raise RuntimeError(
                f"Function '{name}' already declared in the current scope"
            )
        self.function_stack[self.curr_scope][name] = func_def

    def get_function_definition(self, name):
        for scope in reversed(self.function_stack[: self.curr_scope + 1]):
            if name in scope:
                return scope[name]
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

    def get_variant_definition(self, name):
        for scope in reversed(self.variant_stack[: self.curr_scope + 1]):
            if name in scope:
                return scope[name]
        raise RuntimeError(f"Variant '{name}' not found in any scope")
