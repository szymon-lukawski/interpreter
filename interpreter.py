from copy import deepcopy
from typing import Dict, Callable
from AST import *
from visitor import Visitor

RelativeOperator = str
BuiltInType = str
DIGITS = set(list("0123456789"))
INT_FRACTION_SEPARATOR = '.'

class Converter:
    def __init__(self) -> None:
        self.supported_types = ["null_type", "int", "float", "str"]
        self.supported_conversions: Dict[tuple[BuiltInType, BuiltInType], Callable] ={
            ("nulltype", "str") : self._null_to_str,
            ("str", "int") : None,
            ("str", "float") : None,
            ("int", "str") : self._int_to_str,
            ("int", "float"): self._int_to_float,
            ("float", "int") : self._float_to_int,
            ("float", "str"): self._float_to_str,
        }

    def _null_to_str(self, _ : NullLiteral = None) -> StrLiteral:
        return StrLiteral('null')
    
    def _int_to_str(self, int_expr : IntLiteral) -> StrLiteral:
        return StrLiteral(str(int_expr.value))
    
    def _float_to_str(self, float_expr : FloatLiteral) -> StrLiteral:
        return StrLiteral(f"{float_expr:.7f}")
    
    def _int_to_float(self, int_expr : IntLiteral) -> FloatLiteral:
        return FloatLiteral(float(int_expr.value))
    
    def _float_to_int(self, float_expr : FloatLiteral) -> IntLiteral:
        # TODO if in int limits
        return IntLiteral(int(float_expr.value))
    
    def _str_to_int(self, str_expr : StrLiteral) -> IntLiteral:
        # all chars are digits, unless it has one comma. 
        # if it has one comma then convert to float and then convert to int
        # TODO check length, Add special Error classes. Imporve errors, display what con not be converted
        # if len(str_expr.value) == 0:
        #     raise TypeError("Can not convert empty string to int")
        # is_float = False
        # for char in str_expr.value:
        #     if not char in DIGITS:
        #         if is_float:
        #             raise TypeError("Can not convert to int")
        #         if char == INT_FRACTION_SEPARATOR:
        #             is_float = True
        #         else:
        #             raise TypeError("Can not convert to int")
        # if is_float:
        #     return self._float_to_int(self._str_to_float(str_expr))
        # int_value = 0
        # for digit in str_expr.value:
        #     int_value = int_value * 10 + int(digit)
        return IntLiteral(int(float(str_expr.value)))



    def _str_to_float(self, str_expr: StrLiteral) -> FloatLiteral:
        # all chars are digits, unless it has one comma. 
        # TODO check length, Add special Error classes. Imporve errors, display what con not be converted
        # if len(str_expr.value) == 0:
        #     raise TypeError("Can not convert empty string to float")
        # for char in str_expr.value:
        #     if not char in DIGITS:
        #         if is_float:
        #             raise TypeError("Can not convert to int")
        #         if char == INT_FRACTION_SEPARATOR:
        #             is_float = True
        #         else:
        #             raise TypeError("Can not convert to int")
        # fractional_digits = 0
        # int_value = 0
        # fraction_part = 0
        # pos = 0
        # char = str_expr.value[pos]
        
        # while char != INT_FRACTION_SEPARATOR and pos < len(str_expr.value):

            
        # return IntLiteral(int_value)
        return IntLiteral(int(str_expr.value))
            

class Comparator:
    """Class for comparing"""

    def __init__(self) -> None:
        self.supported_relation_operators = ["<", "<=", "==", "!=", ">=", ">"]
        self.supported_types = ["int", "float", "str", "null_type"]
        self.handling_dict: Dict[RelativeOperator, Dict[BuiltInType, Callable]] = {
            rel_op: {
                (type1, type2): None
                for type1, type2 in zip(self.supported_types, self.supported_types)
            }
            for rel_op in self.supported_relation_operators
        }
        self._populate_handling_dict_less_than()

    def _populate_handling_dict_less_than(self):
        self.handling_dict["<"]["null_type", "null_type"] = Comparator._return_false
        self.handling_dict["<"][
            "null_type", "int"
        ] = Comparator._comparing_null_type_and_non_null_type
        self.handling_dict["<"][
            "null_type", "float"
        ] = Comparator._comparing_null_type_and_non_null_type
        self.handling_dict["<"][
            "null_type", "string"
        ] = Comparator._comparing_null_type_and_non_null_type
        self.handling_dict["<"][
            "int", "null_type"
        ] = Comparator._comparing_non_null_type_and_null_type
        self.handling_dict["<"]["int", "int"] = Comparator._compare_less_than_int_int
        self.handling_dict["<"][
            "int", "float"
        ] = Comparator._compare_less_than_int_float
        self.handling_dict["<"]["int", "str"] = Comparator._compare_less_than_int_str

    def _compare_less_than_int_str(self, left, right):
        pass

    def _compare_less_than_int_float(self, left, right):
        return self._compare_numbers(left, right)

    def _compare_less_than_int_int(self, left, right):
        return self._compare_numbers(left, right)

    def _compare_numbers(self, left, right):
        return bool(left < right)

    def _return_false(self, _, __):
        return False

    def _return_True(self, _, __):
        return True

    @staticmethod
    def _comparing_null_type_and_non_null_type(_, __):
        raise TypeError("Can not compare nulltype with non nulltype")

    @staticmethod
    def _comparing_non_null_type_and_null_type(_, __):
        raise TypeError("Can not compare non null type with null type")


class Interpreter(Visitor):

    class Struct:
        def __init__(self, attributes) -> None:
            self.attr_dict = {}
            for k in attributes:
                self.attr_dict[k] = None

    class Scopes:
        def __init__(self):
            self.variable_stack = [{}]
            self.function_stack = [{}]
            self.type_stack = [{'int': None, 'float': None, 'str': None, 'null_type': None}]
            self.variant_stack = [{}]  # ?
            self.curr_scope = 0
        
        def is_type_built_in(self, type_name):
            return type_name in {"int", "float", "str", "null_type"}

        def push_scope(self):
            self.variable_stack.append({})
            self.function_stack.append({})
            self.type_stack.append({})
            self.variant_stack.append({})
            self.curr_scope += 1

        def pop_scope(self):
            if len(self.variable_stack) > 1:
                self.variable_stack.pop()
                self.function_stack.pop()
                self.type_stack.pop()
                self.variant_stack.pop()
                self.curr_scope -= 1
            else:
                raise RuntimeError("Cannot pop the global scope")
            
        def set_active_scope_to_(self, scope_idx : int):
            self.curr_scope = scope_idx # TODO add value checking if within correct range


        def add_variable(self, name, var_type, is_mutable: bool = False, value=None):
            if not self.type_exists_in_all_scopes(var_type):
                raise RuntimeError(f"Type '{var_type}' not found in any scope")
            if name in self.variable_stack[self.curr_scope]:
                raise RuntimeError(
                    f"Variable '{name}' already declared in the current scope"
                )
            if self.is_type_built_in(var_type):
                self.variable_stack[self.curr_scope][name] = self.create_built_in_instance(var_type, is_mutable, value)
            else:
                self.variable_stack[self.curr_scope][name] = self.create_struct_type_instance(var_type, is_mutable)

        def create_built_in_instance(self, var_type, is_mutable, value):
            return {"type": var_type, "is_mutable": is_mutable, "value": value}

        def create_struct_type_instance(self, var_type, is_mutable):
            struct_dict = {"type": var_type, "is_mutable": is_mutable, "value": None}
            variable_defs : List[VariableDeclaration] = self.get_type_definition(var_type)
            value_dict = dict()
            for var_def in variable_defs:
                value = None
                if self.is_type_built_in(var_def.type):
                    value = self.create_built_in_instance(var_def.type, var_def.is_mutable, var_def.default_value)
                else:
                    value = self.create_struct_type_instance(var_def.type, var_def.is_mutable)
                value_dict[var_def.name] = value
            struct_dict["value"] = value_dict
            
            return struct_dict

        def variable_exists_in_current_scope(self, name):
            return name in self.variable_stack[self.curr_scope]

        def get_variable_value(self, name):
            for scope in reversed(self.variable_stack[:self.curr_scope+1]):
                if name in scope:
                    value = scope[name]["value"]
                    if value is None:
                        raise RuntimeError(f"Variable '{name}' has no value")
                    return deepcopy(value)
            raise RuntimeError(f"Variable '{name}' not found in any scope")

        def set_variable_value(self, name_chain, value):
            name = name_chain[0]
            for scope in reversed(self.variable_stack[:self.curr_scope+1]):
                if name in scope:
                    if len(name_chain) ==  1:
                        if scope[name]["is_mutable"] or not scope[name]["is_mutable"] and scope[name]["value"] is None:
                            scope[name]["value"] = value
                            return
                        else:
                            raise RuntimeError(f"Trying to reassign value to non mutable variable '{name}'")
                    obj = scope[name]["value"]
                    for name_ in name_chain[1:-1]:
                        obj = obj[name_]["value"]
                    

                    obj[name_chain[-1]]["value"] = value
                    return
            raise RuntimeError(f"Variable '{name}' not found in any scope")

        def add_function(self, func_def: FuncDef):
            name = func_def.name
            if name in self.function_stack[self.curr_scope]:
                raise RuntimeError(
                    f"Function '{name}' already declared in the current scope"
                )
            self.function_stack[self.curr_scope][name] = func_def


        def get_function_definition(self, name):
            for scope in reversed(self.function_stack[:self.curr_scope+1]):
                if name in scope:
                    return scope[name]
            raise RuntimeError(f"Function '{name}' not found in any scope")

        def add_type(self, name, definition):
            if name in self.type_stack[self.curr_scope]:
                raise RuntimeError(
                    f"Type '{name}' already declared in the current scope"
                )
            self.type_stack[self.curr_scope][name] = definition


        def type_exists_in_all_scopes(self, name):
            return any(name in scope for scope in self.type_stack[:self.curr_scope+1])

        def get_type_definition(self, name):
            for scope in reversed(self.type_stack[:self.curr_scope+1]):
                if name in scope:
                    return scope[name]
            raise RuntimeError(f"Type '{name}' not found in any scope")

        def add_variant(self, name, definition):
            if name in self.variant_stack[self.curr_scope]:
                raise RuntimeError(
                    f"Variant '{name}' already declared in the current scope"
                )
            self.variant_stack[self.curr_scope][name] = definition

        def get_variant_definition(self, name):
            for scope in reversed(self.variant_stack[:self.curr_scope+1]):
                if name in scope:
                    return scope[name]
            raise RuntimeError(f"Variant '{name}' not found in any scope")

    def __init__(self):
        self.scopes = self.Scopes()


    def visit_program(self, program):
        for statement in program.children:
            rv = statement.accept(self)
            if rv:
                return rv

    def visit_assignment(self, assignment : AssignmentStatement):
        # 1 bez .
        # sprawdz czy jest i ew zwróć referencję do struktury opisującej tą nazwę.
        # sprawdz czy reszta dostępu (reszta object_accessu) pasuje do zwróconej struktury i zwróć referencję do pola które nalezy przypisać.
        #
        # sprawdz czy zmienna jest niemutowalna i nie ma wartości.
        value = assignment.expr.accept(self)
        # porównaj typy. Jesli sa zgodne lub kompatybilne to przypisz wartość
        self.scopes.set_variable_value(assignment.obj_access.name_chain, value)

    def visit_param(self, param: Param):
        return super().visit_param(param)

    def visit_visit(self, visit_statement: VisitStatement):
        return super().visit_visit(visit_statement)

    def visit_while(self, while_stmt: WhileStatement):
        rv = None 
        while rv is None and while_stmt.cond.accept(self):
            self.scopes.push_scope()
            rv = while_stmt.prog.accept(self)
            self.scopes.pop_scope()
        return rv

    def visit_if(self, if_stmt):
        evaled_condition = if_stmt.cond.accept(self)
        # sprawdz czy wynik condition da się zamienić na wartość
        rv = None
        if evaled_condition:
            self.scopes.push_scope()
            rv = if_stmt.prog.accept(self)
            self.scopes.pop_scope()
        elif if_stmt.else_prog:
            self.scopes.push_scope()
            rv = if_stmt.else_prog.accept(self)
            self.scopes.pop_scope()
        return rv

    def visit_return(self, return_stmt):
        return return_stmt.expr.accept(self)

    def visit_case_section(self, case_section : CaseSection):
        return {
            "type": case_section.type,
            "program": case_section.program,
        }

    def visit_func_call(self, func_call : FunctionCall):
        # curr_scope = self.get_active_scope()
        args = [arg.accept(self) for arg in func_call.args]
        func_def = self.scopes.get_function_definition(func_call.name)
        # self._change_scope_to_(func_def_scope)
        self.scopes.push_scope()
        for param, arg in zip(func_def.params, args):
            self.scopes.add_variable(param.name, param.type, param.is_mutable, arg)
        rv = func_def.prog.accept(self)
        self.scopes.pop_scope()
        # self._change_scope_to(curr_scope)
        return rv
        # TODO ^^^ what if the scope difference is greater than 1


    def visit_obj_access(self, obj_access : ObjectAccess):
        # For now supports only simple types
        obj = None
        if isinstance(obj_access.name_chain[0], str):
            obj = self.scopes.get_variable_value(obj_access.name_chain[0])
        if isinstance(obj_access.name_chain[0], FunctionCall):
            obj =  obj_access.name_chain[0].accept(self)
        for name in obj_access.name_chain[1:]:
            obj = obj[name]["value"]
        return obj

    def visit_var_dec(self, var_dec):
        self.scopes.add_variable(var_dec.name, var_dec.type, var_dec.is_mutable, var_dec.default_value.accept(self) if var_dec.default_value is not None else None)

    def visit_struct_def(self, struct_def : StructDef):
        self.scopes.add_type(struct_def.name, struct_def.attributes)

    def visit_variant_def(self, variant_def : VariantDef):
        self.scopes.add_variant(variant_def.name, variant_def.named_types)

    def visit_named_type(self, named_type):
        return {"name": named_type.name, "type": self.visit(named_type.type)}

    def visit_func_def(self, func_def):
        self.scopes.add_function(func_def)

    def visit_or(self, or_expr):
        for child in or_expr.children:
            if child.accept(self):
                return True
        return False

    def visit_and(self, and_expr):
        for child in and_expr.children:
            if not child.accept(self):
                return False
        return True

    def visit_rel(self, rel_expr):
        left = rel_expr.left.accept(self)
        right = rel_expr.right.accept(self)
        # TODO dodaj sprawdzenie typów kompatybilnych do kazdej z tych operacji porównania
        match rel_expr.operator:
            case "==":
                return bool(left == right)
            case "!=":
                return bool(left != right)
            case "<":
                return bool(left < right)
            case ">":
                return bool(left > right)
            case "<=":
                return bool(left <= right)
            case ">=":
                return bool(left >= right)

    def visit_add(self, add_expr):
        result = add_expr.children[0].accept(self)
        for i, op in enumerate(add_expr.operations):
            if op == "+":
                result += add_expr.children[i + 1].accept(self)
            elif op == "-":
                result -= add_expr.children[i + 1].accept(self)
        return result

    def visit_multi(self, multi_expr):
        result = multi_expr.children[0].accept(self)
        for i, op in enumerate(multi_expr.operations):
            if op == "*":
                result *= multi_expr.children[i + 1].accept(self)
            elif op == "/":
                right = multi_expr.children[i + 1].accept(self)
                if right == 0:
                    raise RuntimeError("Dzielenie przez  0 kwiatuszku!")
                result /= right
        return result

    def visit_unary(self, unary_expr):
        value = unary_expr.negated.accept(self)
        if isinstance(value, bool):
            return not value
        return -value

    def visit_null_literal(self, null_literal):
        return None

    def visit_int_literal(self, int_literal):
        return int_literal.value

    def visit_float_literal(self, float_literal):
        return float_literal.value

    def visit_str_literal(self, str_literal):
        return str_literal.value
