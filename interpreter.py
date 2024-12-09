from copy import deepcopy
from typing import Dict, Callable
from AST import *
from visitor import Visitor
from scopes import Scopes
from interpreter_types import Variable, Value

class Interpreter(Visitor):

    def __init__(self, max_recursion_depth: int = 100):
        self.scopes = Scopes(self)
        self._max_recursion_depth = max_recursion_depth
        self.curr_recursion = 1

    def visit_program(self, program):
        for statement in program.children:
            rv = statement.accept(self)
            if rv:
                return rv

    def visit_assignment(self, assignment: AssignmentStatement):
        # 1 bez .
        # sprawdz czy jest i ew zwróć referencję do struktury opisującej tą nazwę.
        # sprawdz czy reszta dostępu (reszta object_accessu) pasuje do zwróconej struktury i zwróć referencję do pola które nalezy przypisać.
        #
        # sprawdz czy zmienna jest niemutowalna i nie ma wartości.
        value = assignment.expr.accept(self)
        # porównaj typy. Jesli sa zgodne lub kompatybilne to przypisz wartość
        self.scopes.set_variable_value(assignment.obj_access.name_chain, value)

    def visit_assignment_2(self, assignment: AssignmentStatement):
        name_chain = assignment.obj_access.name_chain
        name = name_chain[0]
        variable = self.scopes.get_variable(name)
        if len(name_chain) == 1:
            value = self._convert_to_(variable.type, assignment.expr.accept(self))
            self.scopes.set_(name, value)
            return 
        value : Value | None = variable.value # Caution: value might be None
        for attr_name in name_chain[1:-1]:
            # if value is None: raise Attribute Error
            value = value[attr_name] # value.get_attr(attr_name)
        value = self._convert_to_(value[name_chain[-1]].type, assignment.expr.accept(self))

        # value.set_attr(name_chain[-1], value)
        value[name_chain[-1]] = value

    def visit_param(self, param: Param):
        return super().visit_param(param)

    def visit_visit(self, visit_statement: VisitStatement):
        return super().visit_visit(visit_statement)

    def visit_while(self, while_stmt: WhileStatement):
        rv = None
        while rv is None and while_stmt.cond.accept(self): # evalued_condition = self._convert_to_int(evaled_condition)
            self.scopes.push_scope()
            rv = while_stmt.prog.accept(self)
            self.scopes.pop_scope()
        return rv

    def visit_if(self, if_stmt):
        evaled_condition = if_stmt.cond.accept(self)
        # evalued_condition = self._convert_to_int(evaled_condition)
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

    def visit_case_section(self, case_section: CaseSection):
        return {
            "type": case_section.type,
            "program": case_section.program,
        }

    def visit_func_call(self, func_call: FunctionCall):
        curr_scope = self.scopes.curr_scope
        args = [arg.accept(self) for arg in func_call.args]
        func_def, func_scope_idx = self.scopes.get_function_definition_and_its_scope_idx(func_call.name)
        self.scopes.curr_scope = func_scope_idx
        self.scopes.push_scope()
        for param, arg in zip(func_def.params, args):
            self.scopes.add_variable(param.name, param.type, param.is_mutable, arg)
        self.curr_recursion += 1
        if self.curr_recursion > self._max_recursion_depth:
            raise RuntimeError("Maximal recursion depth reached!")
        rv = func_def.prog.accept(self)
        self.curr_recursion -= 1
        self.scopes.pop_scope()
        self.scopes.curr_scope = curr_scope
        return rv

    def visit_obj_access(self, obj_access: ObjectAccess):
        symbol: Scopes.Symbol = None
        obj_name = obj_access.name_chain[0]
        rest_address = obj_access.name_chain[1:]
        if isinstance(obj_name, str):
            symbol = self.scopes.get_symbol(obj_access.name_chain[0])
        elif isinstance(obj_access.name_chain[0], FunctionCall):
            symbol = obj_access.name_chain[0].accept(self)
            if len(rest_address) == 0:
                return deepcopy(symbol)
        else:
            raise RuntimeError(
                "Object access class should inly have str or func call in name chain"
            )

        # is simple type then return its value
        # is struct type then return copy of entire struct
        # is variant type then return copy of entire variant
        rv = symbol.get_value(rest_address)
        if rv is None:
            raise RuntimeError(
                f"Variable '{".".join(obj_access.name_chain)}' has no value"
            )
        return deepcopy(rv)
    
    def visit_obj_access_2(self, obj_access: ObjectAccess):
        # Gets value of symbol, it needs to return VariantSymbol not The currently active on for visit_visit
        symbol: Scopes.Symbol = None
        obj_name = obj_access.name_chain[0]
        if isinstance(obj_name, str):
            symbol = self.scopes.get_symbol(obj_name)
        elif isinstance(obj_access.name_chain[0], FunctionCall):
            symbol = obj_name.accept(self)
        rest_address = obj_access.name_chain[1:]
        for attr_name in rest_address:
            symbol = symbol[attr_name] # This should raise NotInitialised error if None 
        return deepcopy(symbol) # deepcopy when getting the value of struct or variant

    def visit_var_dec(self, var_dec):
        self.scopes.add_variable(
            var_dec.name,
            var_dec.type,
            var_dec.is_mutable,
            (
                var_dec.default_value.accept(self)
                if var_dec.default_value is not None
                else None
            ),
        )

    def visit_var_dec_2(self, var_dec : VariableDeclaration):
        name = var_dec.name
        type_ = var_dec.type
        value = var_dec.default_value
        self.scopes.reserve_place_for_(name) # raises Error if the same var name has been in current scope
        default_value = self._get_default_value(type_, value) # raises error when error in var_dec attributes
        converted = self._convert_to_(type_, default_value) # raises error when value has been of not compatible types
        self.scopes.set_(name, converted)


    def _convert_to_(self, target_type : str, value : Scopes.Symbol):
        # if value of Built in Types and target is {int, float, str} then easy
        # if value of Struct Type and target is {int, float, str} then raise error
        # if value of Variant Type and target is {int, float, str} then 
        return value

    def _get_default_value(self, type_ : str, value : ASTNode):
        if value is not None:
            return value.accept(self)
        return self._get_default_value_for_(type_)
    
    def _get_default_value_for_(self, type_ : str):
        pass



    def _get_default_value_for_struct_(self, type_ : str):
        var_defs : List[VariableDeclaration] = self.scopes.get_var_defs_for_(type_)
        attr_dict : Dict[str, Variable] = dict()
        for var_def in var_defs:
            default_value = self._get_default_value(var_def.type, var_def.default_value)
            attr_dict[var_def.name] = Variable(var_def.type, var_def.is_mutable, default_value)
        return Scopes.StructSymbol(type_, None, attr_dict)
    


    def visit_struct_def(self, struct_def: StructDef):
        self.scopes.add_struct_type(struct_def.name, struct_def.attributes)

    def visit_variant_def(self, variant_def: VariantDef):
        self.scopes.add_variant_type(variant_def.name, variant_def.named_types)

    def visit_named_type(self, named_type):
        pass

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
