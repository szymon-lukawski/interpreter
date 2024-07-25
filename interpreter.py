from AST import VisitStatement, WhileStatement
from visitor import Visitor

class Interpreter(Visitor):


    class Struct:
        def __init__(self, attributes) -> None:
            self.attr_dict = {}
            for k in attributes:
                self.attr_dict[k] = None
            

    class Scopes:
        def __init__(self):
            self.variable_stack = []
            self.function_stack = []
            self.type_stack = []
            self.variant_stack = [] # ?

        def push_scope(self):
            self.variable_stack.append({})
            self.function_stack.append({})
            self.type_stack.append({})
            self.variant_stack.append({})

        def pop_scope(self):
            if len(self.variable_stack) > 1:
                self.variable_stack.pop()
                self.function_stack.pop()
                self.type_stack.pop()
                self.variant_stack.pop()
            else:
                raise RuntimeError("Cannot pop the global scope")

        def add_variable(self, name, var_type, value=None):
            if name in self.variable_stack[-1]:
                raise RuntimeError(f"Variable '{name}' already declared in the current scope")
            self.variable_stack[-1][name] = {'type': var_type, 'value': value}

        def variable_exists_in_current_scope(self, name):
            return name in self.variable_stack[-1]

        def variable_is_visable(self, name):
            return any(name in scope for scope in self.variable_stack)

        def get_variable_value(self, name):
            for scope in reversed(self.variable_stack):
                if name in scope:
                    value = scope[name]['value']
                    if value is None:
                        raise RuntimeError(f"Variable '{name}' has no value")
                    return value
            raise RuntimeError(f"Variable '{name}' not found in any scope")

        def set_variable_value(self, name, value):
            for scope in reversed(self.variable_stack):
                if name in scope:
                    scope[name]['value'] = value
                    return
            raise RuntimeError(f"Variable '{name}' not found in any scope")

        def add_function(self, name, definition):
            if name in self.function_stack[-1]:
                raise RuntimeError(f"Function '{name}' already declared in the current scope")
            self.function_stack[-1][name] = definition

        def function_exists_in_current_scope(self, name):
            return name in self.function_stack[-1]

        def function_exists_in_all_scopes(self, name):
            return any(name in scope for scope in self.function_stack)

        def get_function_definition(self, name):
            for scope in reversed(self.function_stack):
                if name in scope:
                    return scope[name]
            raise RuntimeError(f"Function '{name}' not found in any scope")

        def add_type(self, name, definition):
            if name in self.type_stack[-1]:
                raise RuntimeError(f"Type '{name}' already declared in the current scope")
            self.type_stack[-1][name] = definition

        def type_exists_in_current_scope(self, name):
            return name in self.type_stack[-1]

        def type_exists_in_all_scopes(self, name):
            return any(name in scope for scope in self.type_stack)

        def get_type_definition(self, name):
            for scope in reversed(self.type_stack):
                if name in scope:
                    return scope[name]
            raise RuntimeError(f"Type '{name}' not found in any scope")

        def add_variant(self, name, definition):
            if name in self.variant_stack[-1]:
                raise RuntimeError(f"Variant '{name}' already declared in the current scope")
            self.variant_stack[-1][name] = definition

        def variant_exists_in_current_scope(self, name):
            return name in self.variant_stack[-1]

        def variant_exists_in_all_scopes(self, name):
            return any(name in scope for scope in self.variant_stack)

        def get_variant_definition(self, name):
            for scope in reversed(self.variant_stack):
                if name in scope:
                    return scope[name]
            raise RuntimeError(f"Variant '{name}' not found in any scope")



    def __init__(self):
        self.scopes = self.Scopes()


    def visit_program(self, program):
        for statement in program.children:
            statement.accept(self)

    def visit_assignment(self, assignment):
        # 1 bez .
        # sprawdz czy jest i ew zwróć referencję do struktury opisującej tą nazwę.
        # sprawdz czy reszta dostępu (reszta object_accessu) pasuje do zwróconej struktury i zwróć referencję do pola które nalezy przypisać.
        # 
        # sprawdz czy zmienna jest niemutowalna i nie ma wartości.
        value = assignment.expr.accept(self)
        # porównaj typy. Jesli sa zgodne lub kompatybilne to przypisz wartość
        self.environment[assignment.obj_access.nested_objects[0].name] = value

    def visit_visit(self, visit_statement: VisitStatement):
        return super().visit_visit(visit_statement)
    
    def visit_while(self, while_stmt: WhileStatement):
        return super().visit_while(while_stmt)

    def visit_if(self, if_stmt):
        evaled_condition = if_stmt.cond.accept(self)
        # sprawdz czy wynik condition da się zamienić na wartość 
        if evaled_condition:
            if_stmt.prog.accept(self)
        elif if_stmt.else_prog:
            if_stmt.else_prog.accept(self)

    def visit_return(self, return_stmt):
        # TODO
        return self.visit(return_stmt.expr)

    def visit_type(self, type_node):
        return type_node.name

    def visit_case_section(self, case_section):
        return {
            "type": self.visit(case_section.type),
            "program": self.visit(case_section.program)
        }

    def visit_func_call(self, func_call):
        args = [self.visit(arg) for arg in func_call.args]
        return f"Calling {func_call.name} with arguments {args}"

    def visit_identifier(self, identifier):
        return self.environment.get(identifier.name, None)

    def visit_obj_access(self, obj_access):
        result = None
        for obj in obj_access.nested_objects:
            result = result.get(obj.name, None)
            if result is None:
                break
        return result

    def visit_fork(self, fork):
        for statement in fork.statements:
            statement.accept(self)

    def visit_var_dec(self, var_dec):
        # TODO dodaj zmienną do tego scopa
        pass
        # self.environment[var_dec.name] = {
        #     "type": var_dec.type.name,
        #     "is_mutable": var_dec.is_mutable,
        #     "value": None
        # }

    def visit_struct_def(self, struct_def):
        # TODO dodaj strukturę do tego scopa
        return {
            "name": struct_def.name,
            "attributes": struct_def.attributes
        }

    def visit_variant_def(self, variant_def):
        # TODO dodaj variant do tego scopa
        pass  # Implement as needed

    def visit_named_type(self, named_type):
        return {
            "name": named_type.name,
            "type": self.visit(named_type.type)
        }

    def visit_func_def(self, func_def):
        
        # TODO dodaj funckję do tego scopa
        pass  # Implement as needed

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
            case '==':
                return left == right
            case '!=':
                return left != right
            case '<':
                return left < right
            case '>':
                return left > right
            case '<=':
                return left <= right
            case '>=':
                return left >= right
            


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
        return -value

    def visit_null_literal(self, null_literal):
        return None

    def visit_int_literal(self, int_literal):
        return int_literal.value

    def visit_float_literal(self, float_literal):
        return float_literal.value

    def visit_str_literal(self, str_literal):
        return str_literal.value

