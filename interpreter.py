from copy import deepcopy
from typing import Dict, Callable
from AST import *
from visitor import Visitor
from scopes import Scopes
from interpreter_types import Variable, Value, StructValue, VariantValue, BuiltInValue
from multipledispatch import dispatch
from operations import *
from interpreter_errors import InterpreterError, NotSupportedOperation, DivisionByZero, NumberTooBig


class Interpreter(Visitor):

    def __init__(self, max_recursion_depth: int = 100, max_struct_depth: int = 100):
        self.scopes = Scopes()
        self._max_recursion_depth = max_recursion_depth
        self.curr_recursion = 1
        self.max_struct_depth = max_struct_depth
        self.number_limit = 10**9



    def visit_program(self, program):
        for statement in program.children:
            rv = statement.accept(self)
            if rv:
                return rv

    def simple_assignment(self, name, target_type, expr, pos):
        value = self._convert_to_(target_type, expr.accept(self), pos)
        self.scopes.set_(name, value, pos)
        return

    def is_simple_assignment(self, name_chain):
        return len(name_chain) == 1

    def complex_assignment(
        self, variable: Variable, rest_addres: list[str], expr: Expr, pos
    ):
        for attr_name in rest_addres:
            variable = self.get_inner_variable(variable, attr_name, pos)
        variable.value = self._convert_to_(variable.type, expr.accept(self), pos)

    def find_matching_named_type_with_(
        self, attr_name: str, named_types: list[NamedType], variant_type: str, pos
    ):
        for named_type in named_types:
            if self.scopes.is_struct_type_(
                named_type.type
            ) and self.check_attr_name_in_struct_type(attr_name, named_type.type, pos):
                return named_type
        raise InterpreterError(pos,
            f"No matching struct type with attribute '{attr_name}' in variant '{variant_type}'"
        )

    def initialise_empty_complex_variable(self, variable: Variable, attr_name: str, pos):
        if self.scopes.is_built_in_type_(variable.type):
            raise InterpreterError(pos, "Simple types do not have attributes!")
        if self.scopes.is_struct_type_(variable.type):
            variable.value = StructValue(variable.type, dict())
            return
        elif self.scopes.is_variant_type_(variable.type):
            named_types = self.scopes.get_named_types_for_(variable.type, pos)
            matched_named_type = self.find_matching_named_type_with_(
                attr_name, named_types, variable.type, pos
            )
            variable.value = VariantValue(
                variable.type,
                StructValue(matched_named_type.type, dict()),
                matched_named_type.name,
            )
            return

        raise InterpreterError(pos,f"Type '{variable.type}' not found")

    def get_inner_variable(self, variable: Variable, attr_name: str, pos):
        if not variable.can_variable_be_updated():
            raise InterpreterError(pos,"Trying to reassign value to a non-mutable attribute.")
        if not variable.is_initialised():
            self.initialise_empty_complex_variable(variable, attr_name, pos)

        if self.variable_needs_extending(variable, attr_name):
            self.extend_(variable, attr_name, pos)

        variable = variable.value.get_inner_variable(attr_name) # this name might be confusing, it is not recursion
        return variable

    def visit_assignment(self, assignment: AssignmentStatement):
        name_chain = assignment.obj_access.name_chain
        name = name_chain[0]
        pos = assignment.pos
        variable = self.scopes.get_variable(name, pos)
        if self.is_simple_assignment(name_chain):
            self.simple_assignment(name, variable.type, assignment.expr, pos)
            return
        self.complex_assignment(variable, name_chain[1:], assignment.expr, pos)

    def check_attr_name_in_struct_type(self, attr_name: str, struct_type: str, pos):
        if self.scopes.is_struct_type_(struct_type):
            attr_defs = self.scopes.get_var_defs_for_(struct_type, pos)
            for attr_def in attr_defs:
                if attr_name == attr_def.name:
                    return True
        return False

    def variable_needs_extending(self, variable: Variable, attr_name: str):
        return not variable.value.is_attr_in_(attr_name)

    def extend_(self, variable: Variable, attr_name, pos):
        attr_def = self.get_attr_def_from_type_(
            attr_name, variable.value.get_concrete_type(), pos
        )
        variable.value.add_attr(
            attr_def.name, Variable(attr_def.type, attr_def.is_mutable, None)
        )

    def get_attr_def_from_type_(self, attr_name, type_, pos):
        var_defs: List[VariableDeclaration] = self.scopes.get_var_defs_for_(type_, pos)
        for var_def in var_defs:
            if attr_name == var_def.name:
                return var_def

    def check_attr_name_in_(self, type_, attr_name, pos):
        var_defs: List[VariableDeclaration] = self.scopes.get_var_defs_for_(type_, pos)
        for var_def in var_defs:
            if attr_name == var_def.name:
                return True
        raise InterpreterError(pos,f"Attribute '{attr_name}' not found in type '{type_}'")

    def visit_param(self, param: Param):
        pass

    def visit_visit(self, visit_statement: VisitStatement):
        variant_value = visit_statement.obj.accept(self)
        pos = visit_statement.pos
        if not self.scopes.is_variant_type_(variant_value.type):
            raise InterpreterError(pos,"There is no variant type in visit")
        for cs in visit_statement.case_sections:
            if cs.type == variant_value.name:
                self.scopes.push_scope()
                self.scopes.add_variable(
                    variant_value.name, variant_value.type, False, variant_value.value,pos
                )
                rv = cs.program.accept(self)
                self.scopes.pop_scope(pos)
                return rv

    def visit_while(self, while_stmt: WhileStatement):
        rv = None
        pos = while_stmt.pos
        while rv is None and while_stmt.cond.accept(self).bool():
            self.scopes.push_scope()
            rv = while_stmt.prog.accept(self)
            self.scopes.pop_scope(pos)
        return rv

    def visit_if(self, if_stmt):
        evaled_condition = if_stmt.cond.accept(self)
        rv = None
        pos = if_stmt.pos
        if evaled_condition.bool():
            self.scopes.push_scope()
            rv = if_stmt.prog.accept(self)
            self.scopes.pop_scope(pos)
        elif if_stmt.else_prog:
            self.scopes.push_scope()
            rv = if_stmt.else_prog.accept(self)
            self.scopes.pop_scope(pos)
        return rv

    def visit_return(self, return_stmt):
        return return_stmt.expr.accept(self)

    def visit_case_section(self, case_section: CaseSection):
        pass

    def visit_func_call(self, func_call: FunctionCall):
        curr_scope = self.scopes.curr_scope
        pos = func_call.pos
        args = [arg.accept(self) for arg in func_call.args]
        func_def, func_scope_idx = (
            self.scopes.get_function_definition_and_its_scope_idx(func_call.name, pos)
        )
        self.scopes.curr_scope = func_scope_idx
        self.scopes.push_scope()
        for param, arg in zip(func_def.params, args):
            self.scopes.add_variable(
                param.name,
                param.type,
                param.is_mutable,
                self._convert_to_(param.type, arg, param.pos),
                param.pos
            )
        self.curr_recursion += 1
        if self.curr_recursion > self._max_recursion_depth:
            raise InterpreterError(pos,"Maximal recursion depth reached!")
        rv = self._convert_to_(func_def.type, func_def.prog.accept(self), pos)

        self.curr_recursion -= 1
        self.scopes.pop_scope(pos)
        self.scopes.curr_scope = curr_scope
        return rv

    def visit_obj_access(self, obj_access: ObjectAccess):
        value: Value = None
        obj_name = obj_access.name_chain[0]
        pos = obj_access.pos
        if isinstance(obj_name, str):
            variable = self.scopes.get_variable(obj_name, pos)
            value = variable.value
        elif isinstance(obj_name, FunctionCall):
            value = obj_name.accept(self)
        rest_address = obj_access.name_chain[1:]
        if value is None:
            raise InterpreterError(pos, f"Variable '{obj_name}' has no value")
        for attr_name in rest_address:
            value = value[attr_name]
            if value is None:
                raise InterpreterError(pos,
                    f"Variable '{".".join(obj_access.name_chain)}' has no value"
                )
        return deepcopy(value)

    def visit_var_dec(self, var_dec: VariableDeclaration):
        name: str = var_dec.name
        type_: str = var_dec.type
        pos = var_dec.pos
        self.scopes.validate_type_name(type_, pos)
        is_mutable: bool = var_dec.is_mutable
        value: ASTNode = var_dec.default_value

        self.scopes.reserve_place_for_(name, type_, is_mutable, pos)
        if default_value := self._get_default_value(type_, value, depth=0, pos=pos):
            converted = self._convert_to_(type_, default_value, pos)
            self.scopes.set_(name, converted, pos)

    def _convert_to_(self, target_type: str, value: Value, pos):
        if value is None and target_type == "null_type":
            return None
        if value is None:
            raise InterpreterError(pos,"Can not convert no value to something else!")
        if value.type == target_type:
            return value
        if self.scopes.is_variant_type_(value.type):
            return self._convert_to_(target_type, value.value, pos)
        if self.scopes.is_struct_type_(value.type):
            if self.scopes.is_struct_type_(target_type):
                raise InterpreterError(pos,
                    f"Can not convert struct type '{value.type}' to struct type '{target_type}'"
                )
            if self.scopes.is_built_in_type_(target_type):
                raise InterpreterError(pos,
                    f"Can not convert struct type '{value.type}' to builtin type '{target_type}'"
                )
            if self.scopes.is_variant_type_(target_type):
                named_types = self.scopes.get_named_types_for_(target_type, pos)
                for named_type in named_types:
                    if value.type == named_type.type:
                        return VariantValue(target_type, value, named_type.name)
                raise InterpreterError(pos,
                    f"No matching struct variant option while converting from struct '{value.type}' to variant type '{target_type}'"
                )
        if self.scopes.is_built_in_type_(value.type):
            if target_type == "str":
                if value.type == "int":
                    value.value = str(value.value)
                elif value.type == "float":
                    value.value = f"{value.value:.4f}"
                else:
                    raise InterpreterError(pos,
                        f"Hmmm something went wrong when converting from {value.type} into str"
                    )
                value.type = "str"
                return value
            if target_type == "int":
                if value.type == "float":
                    value.value = int(value.value)
                elif value.type == "str":
                    try:
                        value.value = int(float(value.value))
                    except Exception:
                        raise InterpreterError(pos,
                            f"Can not convert '{value.value}' str into int"
                        )
                else:
                    raise InterpreterError(pos,
                        f"Hmmm something went wrong when converting from {value.type} into int"
                    )
                value.type = "int"
                return value
            if target_type == "float":
                if value.type == "int":
                    value.value = float(value.value)
                if value.type == "str":
                    try:
                        value.value = float(value.value)
                    except Exception:
                        raise InterpreterError(pos,
                            f"Can not convert '{value.value}' str into float"
                        )
                value.type = "float"
                return value
            if self.scopes.is_variant_type_(target_type):
                # TODO add compatible types - for example traverse named types second time - if there is no direct type then pick first built in
                named_types = self.scopes.get_named_types_for_(target_type, pos)
                built_in_named_type = None
                for named_type in named_types:
                    if (
                        built_in_named_type is None
                        and self.scopes.is_built_in_type_(named_type.type)
                    ):
                        built_in_named_type = named_type
                    if value.type == named_type.type:
                        return VariantValue(named_type.type, value, named_type.name)
                if built_in_named_type:
                    return VariantValue(
                        built_in_named_type.type,
                        self._convert_to_(built_in_named_type.type, value, pos),
                        built_in_named_type.name,
                    )
                raise InterpreterError(pos,
                    f"There is no built in type in named types of variant '{target_type}' so can not convert built in of type '{value.type}'"
                )
            if self.scopes.is_struct_type_(target_type):
                raise InterpreterError(pos,"Can not convert built in type into struct type. ")
            raise InterpreterError(pos,"Hmmm sth went wrong?")
        if self.scopes.is_variant_type_(target_type):
            named_types = self.scopes.get_named_types_for_(target_type, pos)
            for named_type in named_types:
                if value.type == named_type.type:
                    return VariantValue(named_type.type, value, named_type.name)
        return value

    def _get_default_value(self, type_: str, value: ASTNode, depth, pos):
        if value is not None:
            return value.accept(self)
        return self._get_default_value_for_(type_, depth, pos)

    def _get_default_value_for_(self, type_: str, depth: int, pos):
        if self.scopes.is_built_in_type_(type_):
            return None
        if self.scopes.is_struct_type_(type_):
            return self._get_default_value_for_struct_(type_, depth, pos)
        if self.scopes.is_variant_type_(type_):
            return self._get_default_value_for_variant_(type_)
        raise InterpreterError(pos,f"Type '{type_}' not found in any scope")

    def _get_default_value_for_struct_(self, type_: str, depth, pos):
        """Struct value is not None when at least one of its attributes have non none value"""
        if depth > self.max_struct_depth:
            raise InterpreterError(pos,
                f"Max struct depth reached. Probably you have cycle dependency in type '{type_}'"
            )
        var_defs: List[VariableDeclaration] = self.scopes.get_var_defs_for_(type_, pos)
        attr_dict: Dict[str, Variable] = dict()
        not_none = False
        for var_def in var_defs:
            default_value = self._get_default_value(
                var_def.type, var_def.default_value, depth + 1, pos
            )
            if default_value:
                not_none = True
            attr_dict[var_def.name] = Variable(
                var_def.type, var_def.is_mutable, default_value
            )
        if not_none:
            return StructValue(type_, attr_dict)
        return None

    def _get_default_value_for_variant_(self, type_: str):
        return None

    def visit_struct_def(self, struct_def: StructDef):
        pos = struct_def.pos
        self.scopes.add_struct_type(struct_def.name, struct_def.attributes, pos)

    def visit_variant_def(self, variant_def: VariantDef):
        pos = variant_def.pos
        self.scopes.add_variant_type(variant_def.name, variant_def.named_types, pos)
        if len(variant_def.named_types) <= 1: 
            raise InterpreterError(pos,f"Variant '{variant_def.name}' should have more than 1 variant options")
        for named_type in variant_def.named_types:
            named_type.accept(self)
        

    def visit_named_type(self, named_type):
        pos = named_type.pos
        if self.scopes.is_variant_type_(named_type.type):
            raise InterpreterError(pos,f"Variant option '{named_type.name}' can no be of type variant")

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
                result = self.add(result, add_expr.children[i + 1].accept(self), add_expr.pos)
            elif op == "-":
                result = self.sub(result, add_expr.children[i + 1].accept(self), add_expr.pos)
        return result

    def visit_multi(self, multi_expr):
        result = multi_expr.children[0].accept(self)
        for i, op in enumerate(multi_expr.operations):
            if op == "*":
                result = self.mul(result, multi_expr.children[i + 1].accept(self), multi_expr.pos)
            elif op == "/":
                right = multi_expr.children[i + 1].accept(self)
                result = self.div(result, right, multi_expr.pos)
        return result

    def visit_unary(self, unary_expr):
        value = unary_expr.negated.accept(self)
        return self.minus(value, unary_expr.pos)

    def visit_null_literal(self, null_literal):
        return None

    def visit_int_literal(self, int_literal):
        return BuiltInValue("int", int_literal.value)

    def visit_float_literal(self, float_literal):
        return BuiltInValue("float", float_literal.value)

    def visit_str_literal(self, str_literal):
        return BuiltInValue("str", str_literal.value)
    
    @dispatch(BuiltInValue, object) 
    def minus(self, value, pos):
        return self.minus(value.value, pos)

    @dispatch(int, object) 
    def minus(self, value, pos):
        value *= -1
        return BuiltInValue('int', value)

    @dispatch(float, object) 
    def minus(self, value, pos):
        value *= -1
        return BuiltInValue('float', value)
    
    @dispatch(str, object) 
    def minus(self, value, pos):
        raise NotSupportedOperation(pos, "Can not '-' a string.")

    @dispatch(StructValue, object) 
    def minus(self, value, pos):
        raise NotSupportedOperation(pos, "Can not '-' a struct.")

    @dispatch(VariantValue, object) 
    def minus(self, value, pos):
        value.value = self.minus(value.value, pos)
        return value
    
    @dispatch(BuiltInValue, BuiltInValue, object)
    def mul(self, left, right, pos):
        return self.mul(left.value, right.value, pos)

    @dispatch(int, int, object)
    def mul(self, left, right, pos):
        return BuiltInValue('int', left * right)
    
    @dispatch(int, float, object)
    def mul(self, left, right, pos):
        right = self._convert_to_('int', BuiltInValue('float', right), pos)
        return self.mul(BuiltInValue('int', left), right, pos)

    @dispatch(int, str, object)
    def mul(self, left, right, pos):
        right = self._convert_to_('int', BuiltInValue('str', right), pos)
        return self.mul(BuiltInValue('int', left), right, pos)

    @dispatch(BuiltInValue, StructValue, object)
    def mul(self, left, right, pos):
        raise NotSupportedOperation(pos, "Can not '*' a builtin and struct.")
    
    @dispatch(StructValue, BuiltInValue, object)
    def mul(self, left, right, pos):
        raise NotSupportedOperation(pos, "Can not '*' a struct and builtin.")

    @dispatch(BuiltInValue, VariantValue, object)
    def mul(self, left, right, pos):
        return self.mul(left, right.value, pos)
    
    @dispatch(VariantValue, BuiltInValue, object)
    def mul(self, left, right, pos):
        return self.mul(left.value, right, pos)

    @dispatch(float, int, object)
    def mul(self, left, right, pos):
        return BuiltInValue('float', left * float(right))
    
    @dispatch(float, float, object)
    def mul(self, left, right, pos):
        return BuiltInValue('float', left * right)
    
    @dispatch(float, str, object)
    def mul(self, left, right, pos):
        right = self._convert_to_('float', BuiltInValue('str', right), pos)
        return self.mul(BuiltInValue('float', left), right, pos)
    
    @dispatch(str, int, object)
    def mul(self, left, right, pos):
        return BuiltInValue('str', left*right) # reapeating right times left value.
    
    @dispatch(str, float, object)
    def mul(self, left, right, pos):
        right = self._convert_to_('int', BuiltInValue('float', right), pos)
        return self.mul(BuiltInValue('str', left), right, pos)

    @dispatch(str, str, object)
    def mul(self, left, right, pos):
        result = []
        for l, r in zip(left,right):
            result.append((l+r))
        return BuiltInValue('str', "".join(result))
    
    @dispatch(BuiltInValue, BuiltInValue, object)
    def div(self, left, right, pos):
        return self.div(left.value, right.value, pos)

    @dispatch(int, int, object)
    def div(self, left, right, pos):
        if right == 0:
            raise DivisionByZero(pos, "Not good.")
        return BuiltInValue('int', int(left / right))

    @dispatch(int, float, object)
    def div(self, left, right, pos):
        right = self._convert_to_('int', BuiltInValue('float', right), pos)
        if right.value == 0:
            raise DivisionByZero(pos, "Not good.")
        return BuiltInValue('int', int(left / right.value))

    @dispatch(int, str, object)
    def div(self, left, right, pos):
        right = self._convert_to_('int', BuiltInValue('str', right), pos)
        if right.value == 0:
            raise DivisionByZero(pos, "Not good.")
        return BuiltInValue('int', int(left / right.value))
    

    @dispatch(BuiltInValue, StructValue, object)
    def div(self, left, right, pos):
        raise NotSupportedOperation(pos, "Can not '/' a builtin and struct.")
    
    @dispatch(StructValue, BuiltInValue, object)
    def div(self, left, right, pos):
        raise NotSupportedOperation(pos, "Can not '/' a struct and builtin.")

    @dispatch(BuiltInValue, VariantValue, object)
    def div(self, left, right, pos):
        return self.div(left, right.value, pos)
    
    @dispatch(VariantValue, BuiltInValue, object)
    def div(self, left, right, pos):
        return self.div(left.value, right, pos)
    

    @dispatch(float, int, object)
    def div(self, left, right, pos):
        return BuiltInValue('float', left / float(right))
    
    @dispatch(float, float, object)
    def div(self, left, right, pos):
        return BuiltInValue('float', left / right)
    
    @dispatch(float, str, object)
    def div(self, left, right, pos):
        right = self._convert_to_('float', BuiltInValue('str', right), pos)
        return self.div(BuiltInValue('float', left), right, pos)
    
    @dispatch(str, int, object)
    def div(self, left, right, pos):
        return BuiltInValue('str', left[right] if len(left) > right else "") # getting char at right idx
    
    @dispatch(str, float, object)
    def div(self, left, right, pos):
        right = self._convert_to_('int', BuiltInValue('float', right), pos)
        return self.div(BuiltInValue('str', left), right, pos)

    @dispatch(str, str, object)
    def div(self, left, right, pos):
        return BuiltInValue('str', left.replace(right, ""))
    

    @dispatch(BuiltInValue, BuiltInValue, object)
    def add(self, left, right, pos):
        return self.add(left.value, right.value, pos)

    @dispatch(int, int, object)
    def add(self, left, right, pos):
        if int(left + right) > self.number_limit:
            raise NumberTooBig(pos, "Not good.")
        return BuiltInValue('int', int(left + right))

    @dispatch(int, float, object)
    def add(self, left, right, pos):
        right = self._convert_to_('int', BuiltInValue('float', right), pos)
        return BuiltInValue('int', int(left + right.value))

    @dispatch(int, str, object)
    def add(self, left, right, pos):
        right = self._convert_to_('int', BuiltInValue('str', right), pos)
        return BuiltInValue('int', int(left + right.value))
    

    @dispatch(BuiltInValue, StructValue, object)
    def add(self, left, right, pos):
        raise NotSupportedOperation(pos, "Can not '+' a builtin and struct.")
    
    @dispatch(StructValue, BuiltInValue, object)
    def add(self, left, right, pos):
        raise NotSupportedOperation(pos, "Can not '+' a struct and builtin.")

    @dispatch(BuiltInValue, VariantValue, object)
    def add(self, left, right, pos):
        return self.add(left, right.value, pos)
    
    @dispatch(VariantValue, BuiltInValue, object)
    def add(self, left, right, pos):
        return self.add(left.value, right, pos)
    

    @dispatch(float, int, object)
    def add(self, left, right, pos):
        return BuiltInValue('float', left + float(right))
    
    @dispatch(float, float, object)
    def add(self, left, right, pos):
        return BuiltInValue('float', left + right)
    
    @dispatch(float, str, object)
    def add(self, left, right, pos):
        right = self._convert_to_('float', BuiltInValue('str', right), pos)
        return self.add(BuiltInValue('float', left), right, pos)
    
    @dispatch(str, int, object)
    def add(self, left, right, pos):
        right = self._convert_to_('str', BuiltInValue('int', right), pos)
        return BuiltInValue('str', left + right.value)
    
    @dispatch(str, float, object)
    def add(self, left, right, pos):
        right = self._convert_to_('str', BuiltInValue('float', right), pos)
        return BuiltInValue('str', left + right.value)

    @dispatch(str, str, object)
    def add(self, left, right, pos):
        return BuiltInValue('str', left + right)
    

    @dispatch(BuiltInValue, BuiltInValue, object)
    def sub(self, left, right, pos):
        return self.sub(left.value, right.value, pos)

    @dispatch(int, int, object)
    def sub(self, left, right, pos):
        return BuiltInValue('int', int(left - right))

    @dispatch(int, float, object)
    def sub(self, left, right, pos):
        right = self._convert_to_('int', BuiltInValue('float', right), pos)
        return BuiltInValue('int', int(left - right.value))

    @dispatch(int, str, object)
    def sub(self, left, right, pos):
        right = self._convert_to_('int', BuiltInValue('str', right), pos)
        return BuiltInValue('int', int(left - right.value))
    

    @dispatch(BuiltInValue, StructValue, object)
    def sub(self, left, right, pos):
        raise NotSupportedOperation(pos, "Can not '-' a builtin and struct.")
    
    @dispatch(StructValue, BuiltInValue, object)
    def sub(self, left, right, pos):
        raise NotSupportedOperation(pos, "Can not '-' a struct and builtin.")

    @dispatch(BuiltInValue, VariantValue, object)
    def sub(self, left, right, pos):
        return self.sub(left, right.value, pos)
    
    @dispatch(VariantValue, BuiltInValue, object)
    def sub(self, left, right, pos):
        return self.sub(left.value, right, pos)
    

    @dispatch(float, int, object)
    def sub(self, left, right, pos):
        return BuiltInValue('float', left - float(right))
    
    @dispatch(float, float, object)
    def sub(self, left, right, pos):
        return BuiltInValue('float', left - right)
    
    @dispatch(float, str, object)
    def sub(self, left, right, pos):
        right = self._convert_to_('float', BuiltInValue('str', right), pos)
        return self.sub(BuiltInValue('float', left), right, pos)
    
    @dispatch(str, int, object)
    def sub(self, left, right, pos):
        right = self._convert_to_('str', BuiltInValue('int', right), pos)
        return self.sub(BuiltInValue('str', left), right, pos)

    @dispatch(str, float, object)
    def sub(self, left, right, pos):
        right = self._convert_to_('str', BuiltInValue('float', right), pos)
        return self.sub(BuiltInValue('str', left), right, pos)
    
    
    @dispatch(str, str, object)
    def sub(self, left, right, pos):
        right_index = left.find(right)
        if right_index == -1:
            return BuiltInValue('str', left)    
        return BuiltInValue('str', left[:right_index] + left[right_index + len(right):])
    