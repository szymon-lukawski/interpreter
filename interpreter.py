from copy import deepcopy
from typing import Dict, Callable
from AST import *
from visitor import Visitor
from scopes import Scopes
from interpreter_types import Variable, Value, StructValue, VariantValue, BuiltInValue
from multipledispatch import dispatch
from operations import *


class Interpreter(Visitor):

    def __init__(self, max_recursion_depth: int = 100):
        self.scopes = Scopes()
        self._max_recursion_depth = max_recursion_depth
        self.curr_recursion = 1

    def visit_program(self, program):
        for statement in program.children:
            rv = statement.accept(self)
            if rv:
                return rv

    def simple_assignment(self, name, target_type, expr):
        value = self._convert_to_(target_type, expr.accept(self))
        self.scopes.set_(name, value)
        return

    def is_simple_assignment(self, name_chain):
        return len(name_chain) == 1

    def complex_assignment(
        self, variable: Variable, rest_addres: list[str], expr: Expr
    ):
        for attr_name in rest_addres:
            variable = self.get_inner_variable(variable, attr_name)
        variable.value = self._convert_to_(variable.type, expr.accept(self))

    def find_matching_named_type_with_(
        self, attr_name: str, named_types: list[NamedType], variant_type: str
    ):
        for named_type in named_types:
            if self.scopes.is_struct_type_(
                named_type.type
            ) and self.check_attr_name_in_struct_type(attr_name, named_type.type):
                return named_type
        raise RuntimeError(
            f"No matching struct type with attribute '{attr_name}' in variant '{variant_type}'"
        )

    def initialise_empty_complex_variable(self, variable: Variable, attr_name: str):
        if self.scopes.is_built_in_type_(variable.type):
            raise RuntimeError("Simple types do not have attributes!")
        if self.scopes.is_struct_type_(variable.type):
            variable.value = StructValue(variable.type, dict())
            return
        elif self.scopes.is_variant_type_(variable.type):
            named_types = self.scopes.get_named_types_for_(variable.type)
            matched_named_type = self.find_matching_named_type_with_(
                attr_name, named_types, variable.type
            )
            variable.value = VariantValue(
                variable.type,
                StructValue(matched_named_type.type, dict()),
                matched_named_type.name,
            )
            return

        raise RuntimeError(f"Type '{variable.type}' not found")

    def get_inner_variable(self, variable: Variable, attr_name: str):
        if not variable.can_variable_be_updated():
            raise RuntimeError("Trying to reassign value to a non-mutable attribute.")
        if not variable.is_initialised():
            self.initialise_empty_complex_variable(variable, attr_name)

        if self.variable_needs_extending(variable, attr_name):
            self.extend_(variable, attr_name)

        if self.scopes.is_struct_type_(variable.type):
            variable = variable.value.value[attr_name]
        elif self.scopes.is_variant_type_(variable.type):
            variable = variable.value.value.value[attr_name]
        return variable

    def visit_assignment(self, assignment: AssignmentStatement):
        name_chain = assignment.obj_access.name_chain
        name = name_chain[0]
        variable = self.scopes.get_variable(name)
        if self.is_simple_assignment(name_chain):
            self.simple_assignment(name, variable.type, assignment.expr)
            return
        self.complex_assignment(variable, name_chain[1:], assignment.expr)

    def check_attr_name_in_struct_type(self, attr_name: str, struct_type: str):
        if self.scopes.is_struct_type_(struct_type):
            attr_defs = self.scopes.get_var_defs_for_(struct_type)
            for attr_def in attr_defs:
                if attr_name == attr_def.name:
                    return attr_def
        return False

    def variable_needs_extending(self, variable: Variable, attr_name: str):
        if self.scopes.is_struct_type_(variable.type):
            return attr_name not in variable.value.value.keys()
        elif self.scopes.is_variant_type_(variable.type):
            return attr_name not in variable.value.value.value.keys()
        raise NotImplementedError

    def extend_(self, variable: Variable, attr_name):
        attr_def = None
        if self.scopes.is_struct_type_(variable.type):
            attr_def = self.get_attr_def_from_type_(attr_name, variable.type)
        elif self.scopes.is_variant_type_(variable.type):
            attr_def = self.get_attr_def_from_type_(attr_name, variable.value.value.type)
        variable.value.add_attr(
            attr_def.name, Variable(attr_def.type, attr_def.is_mutable, None)
        )

    def get_attr_def_from_type_(self, attr_name, type_):
        var_defs: List[VariableDeclaration] = self.scopes.get_var_defs_for_(type_)
        for var_def in var_defs:
            if attr_name == var_def.name:
                return var_def

    def check_attr_name_in_(self, type_, attr_name):
        var_defs: List[VariableDeclaration] = self.scopes.get_var_defs_for_(type_)
        for var_def in var_defs:
            if attr_name == var_def.name:
                return True
        raise RuntimeError(f"Attribute '{attr_name}' not found in type '{type_}'")

    def visit_param(self, param: Param):
        return super().visit_param(param)

    def visit_visit(self, visit_statement: VisitStatement):
        variant_value = visit_statement.obj.accept(self)
        # validate variant_value is of type variant
        for cs in visit_statement.case_sections:
            if cs.type == variant_value.name:
                self.scopes.push_scope()
                self.scopes.add_variable(
                    variant_value.name, variant_value.type, False, variant_value.value
                )
                rv = cs.program.accept(self)
                self.scopes.pop_scope()
                return rv
        raise NotImplementedError

    def visit_while(self, while_stmt: WhileStatement):
        rv = None
        while (
            rv is None and while_stmt.cond.accept(self).value
        ):  # evalued_condition = self._convert_to_int(evaled_condition)
            self.scopes.push_scope()
            rv = while_stmt.prog.accept(self)
            self.scopes.pop_scope()
        return rv

    def visit_if(self, if_stmt):
        evaled_condition = if_stmt.cond.accept(self)
        # evalued_condition = self._convert_to_int(evaled_condition)
        rv = None
        if evaled_condition.value:
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
        func_def, func_scope_idx = (
            self.scopes.get_function_definition_and_its_scope_idx(func_call.name)
        )
        self.scopes.curr_scope = func_scope_idx
        self.scopes.push_scope()
        for param, arg in zip(func_def.params, args):
            self.scopes.add_variable(
                param.name,
                param.type,
                param.is_mutable,
                self._convert_to_(param.type, arg),
            )
        self.curr_recursion += 1
        if self.curr_recursion > self._max_recursion_depth:
            raise RuntimeError("Maximal recursion depth reached!")
        rv = func_def.prog.accept(self)
        self.curr_recursion -= 1
        self.scopes.pop_scope()
        self.scopes.curr_scope = curr_scope
        return rv

    def visit_obj_access(self, obj_access: ObjectAccess):
        # Gets value of symbol, it needs to return VariantSymbol not The currently active on for visit_visit
        value: Value = None
        obj_name = obj_access.name_chain[0]
        if isinstance(obj_name, str):
            variable = self.scopes.get_variable(obj_name)
            value = variable.value
        elif isinstance(obj_access.name_chain[0], FunctionCall):
            value = obj_name.accept(self)
        rest_address = obj_access.name_chain[1:]
        if value is None:
            raise RuntimeError(f"Variable '{obj_name}' has no value")
        for attr_name in rest_address:
            value = value[attr_name]
            if value is None:
                raise RuntimeError(
                    f"Variable '{".".join(obj_access.name_chain)}' has no value"
                )
        return deepcopy(value)  # deepcopy when getting the value of struct or variant

    def visit_var_dec(self, var_dec: VariableDeclaration):
        name: str = var_dec.name
        type_: str = var_dec.type
        is_mutable: bool = var_dec.is_mutable
        value: ASTNode = var_dec.default_value
        self.scopes.reserve_place_for_(
            name, type_, is_mutable
        )  # raises Error if the same var name has been in current scope
        default_value = self._get_default_value(
            type_, value
        )  # raises error when error in var_dec attributes
        converted = self._convert_to_(
            type_, default_value
        )  # raises error when value has been of not compatible types
        self.scopes.set_(name, converted)

    def _convert_to_(self, target_type: str, value: Value):
        # if value of Built in Types and target is {int, float, str} then easy
        # if value of Struct Type and target is {int, float, str} then raise error
        # if value of Variant Type and target is {int, float, str} then
        if value is None:
            return None
        if self.scopes.is_variant_type_(target_type):
            named_types = self.scopes.get_named_types_for_(target_type)
            for named_type in named_types:
                if value.type == named_type.type:
                    return VariantValue(named_type.type, value, named_type.name)
        return value

    def _get_default_value(self, type_: str, value: ASTNode):
        if value is not None:
            return value.accept(self)
        return self._get_default_value_for_(type_)

    def _get_default_value_for_(self, type_: str):
        if self.scopes.is_built_in_type_(type_):
            return None
        if self.scopes.is_struct_type_(type_):
            return self._get_default_value_for_struct_(type_)
        if self.scopes.is_variant_type_(type_):
            return self._get_default_value_for_variant_(type_)
        raise RuntimeError(f"Type '{type_}' not found in any scope")

    def _get_default_value_for_struct_(self, type_: str):
        """Struct value is not None when at least one of its attributes have non none value"""
        var_defs: List[VariableDeclaration] = self.scopes.get_var_defs_for_(type_)
        attr_dict: Dict[str, Variable] = dict()
        not_none = False
        for var_def in var_defs:
            default_value = self._get_default_value(var_def.type, var_def.default_value)
            if default_value:
                not_none = True
            attr_dict[var_def.name] = Variable(
                var_def.type, var_def.is_mutable, default_value
            )
        if not_none:
            return StructValue(type_, attr_dict)
        return None

    def _get_default_value_for_variant_(self, type_: str):
        """Variant value is the first named type to have it. If none of the them have it then varaint has no value."""
        return None
        # named_types: List[NamedType] = self.scopes.get_named_types_for_(type_)
        # for named_type in named_types:
        #     default_value = self._get_default_value(named_type.type, None)
        #     if default_value:
        #         return VariantValue(type_, default_value)
        # return None

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
        match rel_expr.operator:
            case "==":
                return eq(left, right)
            case "!=":
                return ieq(left, right)
            case "<":
                return lt(left, right)
            case ">":
                return gt(left, right)
            case "<=":
                return lteq(left, right)
            case ">=":
                return gteq(left, right)

    def visit_add(self, add_expr):
        result = add_expr.children[0].accept(self)
        for i, op in enumerate(add_expr.operations):
            if op == "+":
                result = add(result, add_expr.children[i + 1].accept(self))
            elif op == "-":
                result = sub(result, add_expr.children[i + 1].accept(self))
        return result

    def visit_multi(self, multi_expr):
        result = multi_expr.children[0].accept(self)
        for i, op in enumerate(multi_expr.operations):
            if op == "*":
                result = mul(result, multi_expr.children[i + 1].accept(self))
            elif op == "/":
                right = multi_expr.children[i + 1].accept(self)
                if right.value == 0:
                    raise RuntimeError("Dzielenie przez  0 kwiatuszku!")
                result = div(result, multi_expr.children[i + 1].accept(self))
        return result

    def visit_unary(self, unary_expr):
        value = unary_expr.negated.accept(self)
        if isinstance(value, bool):
            return not value
        return -value

    def visit_null_literal(self, null_literal):
        return None

    def visit_int_literal(self, int_literal):
        return BuiltInValue("int", int_literal.value)

    def visit_float_literal(self, float_literal):
        return BuiltInValue("float", float_literal.value)

    def visit_str_literal(self, str_literal):
        return BuiltInValue("str", str_literal.value)
