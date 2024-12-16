# Interpreter of my own programming language. 

### Introduction
Static and weak typing, everything is passed as a value. 
This is an educational project - main goal was to learn something new. 
I used several of the object oriented design patterns. Including but not limited to:
 - visitator

## DEMO:
![](https://github.com/user-attachments/assets/8e271c75-b9b0-43e3-a57b-b57768ffa9e5)
### Getting started
There are two ways of typing statements:
    1. external `.txt` file
    2. interactive mode
Or you can first interpret entire file and then immedietly go into interactive mode. Following example shows just that:
```bash
> git clone https://github.com/szymon-lukawski/interpreter
> cd interpreter
> python -m venv .venv
> source .venv/bin/activate
> pip install -r requirements.txt
> python main.py --source binary_tree.txt -i
interpreter  >>> Sum of my_tree is:
interpreter  >>> 45
Interactive mode enabled. Type q to quit
Type statement : 
```
Congrats! Now you should be able to type any statement and it will be interpreted for you.

### Types:
#### Built-In
1. `int`      - integer in range [-999_999_999; +999_999_999]
2. `float`    - floating-point number. Standard float64 
3. `str`      - represents list of UTF-8 characters. 
```
current_year    : int   = 2024;
pi_aprox        : float = 3.14;
msg             : str   = 'Hello!';
```
#### User-defined
   1. `struct`:
      1. consists of 'attributes'
      2. attributes can have default values.
      3. groups other types
      4. should not have cyclic type dependency
      5. attributes SHOULD NOT have same name.
   2. `variant`:
      1. consists of named `options`
      2. assigning a value determines which of the options type it is.
      3. there MUST be at least 2 options
      4. option names SHOULD be different
      5. option types SHOULD be different
      6. option can not be directly of type `variant`
```
Point2D : struct
begin
  x : mut int = 0;
  y : mut int = 0;
end

Point3D : struct
begin
  x : mut int = 0;
  y : mut int = 0;
  z : mut int = 0;
end

Point : variant
begin
    p2d : Point2D;
    p3d : Point3D;
end

A : Point2D;
B : Point3D;
```
### Operations
* different operations have different precedance:
    1. `.`  - access to struct attribute
    2. `-`  - unary minus
    3. `*` and `/`
    4. `+` and `-`
    5. `<=` and `<` and `==` and `!=` and `>=` and `>`
    6. `&` - logical and
    7. `|` - logical or

* `.` - works only on struct type or struct assigned variant
* `-` unary - works with just `int` and `float`
* left operand of binary operation determines output value type.
* usually binary operation does: convert to left operand's type, perform operation. But there are exceptions:
  * `str_val` `*` `int_val` - repeat str_val, int_val times. 
  * `str_val` `*` `float_val` - convert right side to int. perform operation on new value types.
  * `str_val_1` `*` `str_val_2` - sum of products. e.g. 'ABCD' * '12' => 'A1B2'
  * `str_val` `/` `int` - get a char at index. e.g. 'ABCD' / 2 => 'C'
  * `str_val` `/` `float_val` - convert right side to int. perform operation on new value types.
  * `str_val_1` `/` `str_val_2` - remove all occurances of str_val_2 from str_val_1
  * `str_val_1` `+` `str_val_2` - string concatenation
  * `str_val_1` `-` `str_val_2` - remove first occurance of str_val_2 from str_val_1
  * `str_val_1` `<` `str_val_2` - compares lenght


### Conversion:
| From\To | int | float | str | struct | variant |
|-----------|-----|-------|-----|--------|---------|
| int       | ✅    |  ✅  | ✅    |   ❌     |  ❌       |
| float     |  ✅ - floors float| ✅      |   ✅ - always rounds to 4 digits after dot  |    ❌    |   ❌       |
| str       |  🟡 - if can be interpreted as int, str characters can only be digits 0-9 and at max one `.` not before any digits and not at the end   |    🟡 - if can be interpreted as int, str characters can only be digits 0-9 and at max one `.` not before any digits and not at the end    |  ✅   |    ❌     |     ❌     |
| struct    |   ❌  |    ❌   | ❌    |   🟡 - if types match     |   🟡 - if struct type is in one of variant options      |
| variant   |   🟡 - if types match  |     🟡 - if types match   |    🟡 - if types match  |  🟡 - if types match     |  🟡 - if current variant value match any option in target variant. If source is of built in type then converts to first built in option in target variant       |


### Expression
* combination of object accesses, literals, operations, function calls, brackets.
**Example:**
```
(a.b + 32) * power(4,12) <= - (5 * '3.14') | is_true(a, c) &  another_func(a, d)
```

### Scope
Placeholder for variables, functions, types.
There MUST NOT be two variables with the same name in one scope.
There MUST NOT be two functions with the same name in one scope.
There MUST NOT be two types with the same name in one scope.
New scope can be created when interpreting:
* if
* while
* visit
* function call **Also change of context**

### Statements:
#### if / while
**Example:**
```
n : mut int = 10
if n * 2 - 17
begin 
    while n
    begin
        print(('There will be: '+ n +'lines more.'))
        n = n - 1; 
    end
end 
else 
begin
    print('Hmm. It seems that n did not manage to satisfy a condition')
end
```
**Template:**
* `if <condition> begin <program_1> end` or 
  `if <condition> begin <program_1> end else begin <program_2> end`
  * when condition is evaled true
    1. open new scope
    2. interpret program_1
    3. close scope
  * when condition is evalued false and there exist program_2:
    1. open new scope
    2. interpret program_2
    3. close scope.  
* `while <condition> begin <program> end`
    1. check condition
    2. if it is evaled false go to point `vii.`
    3. open new scope
    4. interpret program
    5. close scope
    6. go back to point `i.`
    7. .

* `condition` - any expression. Depending on the expression value:
  * false, when value is:
    * Not initialised variable
    * Empty `str`
    * 0.0 `float`
    * 0 `int`
  * true, when value is:
    * initialised variables of type struct, or variant if it is initialised struct
    * all other values.
* `program` - list of statements. Can be empty. Statements are interpreted in order they have been defined.

#### visit
**Example:**
```
visit point
begin
    case Point2D
    begin
        msg = '[' + p2d.x + '; ' + p2d.y + ']';
    end
    case Point3D
    begin
        msg = '[' + p3d.x + '; ' + p3d.y + '; ' + p3d.z + ']';
    end
end
print(msg);
```
**Template:**
* available only for variant values.
* if variant value type matches case type:
  * open new scope
  * add new variable. Variable name is the same as in variant option of matched type. Value of this variable is the value of expression.
  * program of the case gets interpreted
  * close scope
* if no type match then go to next statement

#### variable declaration
**Example:**
```
a : int;
b : mut int;
c : int = 1;
d : mut int = 123;
```
**Template:**
```
<variable_name> : [mut] <type_name> [= <expr>];
```
* variable can be either mutable or non-mutable. non-mutable means that after being initialised it can not change. They are non-mutable by default
* expr value should be convertable to specified type.
* Without expr, variable of built in type or variant type is considered not initialised until assignment. 
* struct type variable can be initialised without expr if at least one of their attribute has default value. Not initialised otherwise.

#### assignment
**Example:**
```
a.b.c.d.e = sum(1,2,3) + 5 * 7;
a = '1234.567';
```
**Template:**
```
<object_access> = <expr>;
```
* expr value is automaticaly converted into target type.
* object access:
  * either just variable name:      e.g.: `a`, `this_is_variable_name`, `x1`
  * or name with chain of attributes separated by `.`:      e.g.: `point.x`, `john.address.postal_code`

#### struct definition
**Example:**
```
Point3D : struct
begin
  x : mut int = 0;
  y : mut int = 0;
  z : mut int = 0;
end
```
**Template:**
```
<struct type name> : struct begin {<variable_declaration_statement>} end
```
* number of attributes in one struct type is not limited

#### variant definition
**Example:**
```
Point : variant
begin
  point2d : Point2D
  point3d : Point3D
end
```
**Template:**
```
<variant type name> : struct begin { <option name> : <option type> ; } end
```
* number of options MUST be greater than one.

#### function definition
**Example:**
```
add(arg1: int, arg2: int) : int
begin
  add_sub_function(arg1: int, arg2: int) : int
  begin
    return arg1 + arg2;
  end
  
  add(arg1: int, arg2: int) : int
  begin
    return add_sub_function(arg1, arg2);
  end

  return add(arg1, arg2);
end
```
* in this example there is no recursion, because inner function `add` overloads function name. 
* each time the outer function `add` is called, two inner functions are created. 
**Template:**
```
<function name> ( <params> )  : <return type> begin {statements} end; 
```
* return type is determined during runtime
* function is identified by its name, so there can not be two function with the same name defined in the same scope, even with different parameters 
* function name is visable within function program - recursion is supported
* params: comma separated variable definitions:
  * there can be zero or more
  * default value can be specified but has no effect
  * param names are visable from within function program

#### return 
**Example:**
```
return arg1 + arg2;
```
**Template:**
```
return [<expr>] ;
```
* ends context:
  * global context: ends interpretation
  * function call context: ends interpretation of called function program
* transfers the value of the expr when function call took place

#### function call
**Example:**
```
print('Ala' + 3.14);
```
**Template:**
```
<function name> ( <arguments> ) ;
```
* function call can be independent of expression or can be called within expression.
* Arguments MUST be convertable to corresponding param type
* function call statement loses return value of function call
* arguments are comma separated expressions
* when function is called, context of interpretation gets changed:
  * active scope is the scope of function definition
  * create new scope
  * add params to new scope, assign value from arguments of function call
  * interpret program from function definition
  * close scope
  * get value from return statement and convert it into function return type.
  * active scope is the scope of function call






### Grammar of this language in EBNF 2.0:
```
program             ::= {statement};

statement           ::=  variable_declaration_statement
                       | assignment_statement
                       | if_statement
                       | while_statement
                       | function_definition_statement
                       | type_definition_statement
                       | visit_statement
                       | return_statement
					   | block
                       | function_call_statement
                       | comment;

function_call_statement ::= function_call, ';'

visit_statement ::= 'visit', object_access, 'begin', {case_section} ,'end';

case_section ::= 'case', type, 'begin', program,'end';

block 				            ::= 'begin', program, 'end';
return_statement                ::== 'return', [expression], ';';

variable_declaration_statement  ::= variable_declaration, ';';
variable_declaration            ::= identifier, ':', ['mut'], type, ['=', expression];



assignment_statement            ::= identifier, {'.', identifier}, '=', expression, ';';

if_statement                    ::= 'if', expression, block, ['else', block];

while_statement                 ::= 'while', expression, block;

function_definition_statement   ::= identifier, '(', params, ')', ':', type, block; 

type_definition_statement       ::= struct_def | variant_def;
struct_def                      ::= identifier, ':', 'struct', 'begin', {variable_declaration_statement} ,'end';
variant_def                     ::= identifier, ':', 'variant', 'begin', {named_type_statement} ,'end';

named_type_statement ::= identifier, ':', type, ';'

expression              ::= logical_or_expression;
logical_or_expression   ::= logical_and_expression, {'|', logical_and_expression};
logical_and_expression  ::= relational_expr {'&', relational_expr};
relational_expr         ::= additive_expr, [relational_operator, additive_expr];
additive_expr           ::= multi_expr, {additive_operator, multi_expr};
multi_expr              ::= unary_expr, {multi_operator, unary_expr};
unary_expr              ::= ['-'], term;
term                    ::=	literal
                          | object_access
                          | '(', expression, ')';

object_access           ::=  func_or_ident, {('.', func_or_ident)};

func_or_ident           ::= function_call | identifier;


function_call ::= identifier, '(', [expression , {',', expression}], ')';

param         ::= identifier, ':', ['mut'], type;
params        ::= param , {',', param};

type          ::=  'int'
        		| 'float'
        		| 'str'
        		| 'null'
        		| identifier;

literal        ::=  int_literal
            	| float_literal
            	| str_literal;
            	| 'null'

str_literal  ::= ''',{all_chars_from_utf8_if_Apostrophe_is_escaped} , ''';

int_literal  ::=  '0'
                 | digit_positive, {digit};

float_literal ::= int_literal, ".", digit, { digit };

digit          ::= digit_positive 
                | '0';

digit_positive ::= '1' 
                 | '2' 
                 | '3' 
                 | '4' 
                 | '5' 
                 | '6' 
                 | '7' 
                 | '8' 
                 | '9';
				  


identifier   ::= letter, {alphanumeric | '_'};
alphanumeric ::= letter | digit;
letter       ::= 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G'
               | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N'
               | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U'
               | 'V' | 'W' | 'X' | 'Y' | 'Z' | 'a' | 'b'
               | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i'
               | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p'
               | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w'
               | 'x' | 'y' | 'z' ;

comment      ::= '@', {all_exept_newline}, newline;
newline      ::= '\n'
              |  '\r\n';
```




