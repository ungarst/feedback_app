import re

def missing_semicolon (sub):
    """ Diagnoses a missing semicolon error. """
    if 'Syntax error, insert ";"' in sub.report:
        return 'missing_semicolon.html'

def illegal_predicate_operation (sub):
    """ Diagnoses the use of illegal predicate operations.

    Predicate operations counted as illegal:
        * =!
        * =>
        * =<
        * <<
        * >>
        * \\ I don't know why people are using that one

    """
    match = re.search(r'.*if\s*\(.*(\=\!|\=\>|\=\<|\>\>|\<\<|\\\\).*\)',
                        sub.report)
    if match:
        return 'illegal_predicate_operation.html'

def predicate_operators_undefined (sub):
    """ Diagnoses the improper use of predicate operators.

    Ususally the result of people putting the equals sign in the wrong place 
    e.g. =! rather than != and => rather than >=

    """
    match = re.search(r'The operator (\=\=|\!\=|\<\=|\>\=) is undefined for the argument type\(s\)',
                        sub.report)
    match2 = re.search(r'Incompatible operand types \w+ and \w+', sub.report)
    if match or match2:
        return('predicate_operators_undefined.html')

def missing_closing_curly_brace (sub):
    """ Diagnoses a missing curly brace error. """
    if 'Syntax error, insert "}"' in sub.report:
        return('missing_closing_curly_brace.html')

def missing_opening_curly_brace (sub):
    """ Diagnoses a missing opening curly brace error. """
    diagnostic = "{ expected"
    if diagnostic in sub.report:
        return('missing_opening_curly_brace.html')

def type_cannot_be_resolved(sub):
    """ Diagnoses a variable not resolve error. """
    match = re.search(r'[\w\_]+ cannot be resolved to a type', sub.report)
    if match:
        return('type_cannot_be_resolved.html')

def variable_cannot_be_resolved (sub):
    """ Diagnoses a variable not resolve error. """
    match = re.search(r'[\w\_]+ cannot be resolved(?! to a type)', sub.report)
    if match:
        return('variable_cannot_be_resolved.html')

def undefined_library_method (sub):
    """ Diagnoses a undefined library method error.

    It will only diagnose an error if the code is trying to invoke a
        method on an object that it doesn't have, or is trying to call 
        a static method that doesn't exist from a library.
    It doesn't diagnose an undefined method that should have been implemented 
        by the user.

    """
    match = re.search(r'The method [\w\.\(\),\s]+ is undefined for the type (?!user)\w*', 
            sub.report)
    if match: 
        return('undefined_library_method.html')

def undefined_user_method (sub):
    """ Diagnoses a undefined library method error.

    It will only diagnose missing methods that should be implemented by the 
        programmer, not ones that should be defined in the programming language.

    Relies on the fact that the name of the class that the method is placed into 
        begins with 'user'.

    """
    match = re.search(r'The method [\w\.\,\(\) ]+ is undefined for the type user', 
            sub.report)
    if match: 
        return('undefined_user_method.html')

def incorrect_arguments (sub):
    """ Diagnoses the error of incorrect arguments to a method. """
    match = re.search(r'The method .* in the type .* is not applicable for the arguments', sub.report)
    if match:
        return('incorrect_arguments.html')

def not_double_equals (sub):
    """ Diagnoses the error of attempting to compare two 
    things using a single equals.

    """
    match = re.search(r'if\s*\(.*=(?!=).*\)', sub.report)
    if match and 'The left-hand side of an assignment must be a variable' in sub.report:
        return('not_double_equals.html')

def assigning_to_non_variable (sub):
    diagnostic = 'The left-hand side of an assignment must be a variable'
    if diagnostic in sub.report:
        return('assigning_to_non_variable.html')

def type_mismatch_return (sub):
    if 'Type mismatch' in sub.report:
        report_lines = sub.report.split('\n')
        for i, line in enumerate(report_lines):
            if 'Type mismatch' in line:
                i -= 2
                break
        if 'return' in report_lines[i]:
            return 'wrong_return.html'

def type_mismatch (sub):
    """ Diagnoses a type mismatch error. """
    match = re.search(r'Type mismatch: cannot convert from \w* to \w*',
            sub.report)
    if match:
        return('type_mismatch.html')

def duplicate_variable (sub):
    """ Diagnoses a duplicate variable error.

    These tend to be a result of the programmer redefining the 
        parameters or redefining a variable, most likely 'i' 
        used in a for loop.

    """
    if 'Duplicate local variable' in sub.report:
        return('duplicate_variable.html')

def illegal_modifier (sub):
    """ Diagnoses the use of an illegal modifier.

    Often occurs when the programmer tries to make a local
        variable public..

    """
    if 'Illegal modifier' in sub.report:
        return('illegal_modifier.html')

def assignment_not_using_equals (sub):
    """ Diagnoses the error of attempting to assign not using equals.

    Usually occurs when the programmer tries to assign to a boolean 
        using a predicate e.g. boolean x == 4.

    """
    match = re.search(r'Syntax error on token ".*", = expected',
                        sub.report)
    if match:
        return('assignment_not_using_equals.html')

def no_return (sub):
    if 'return' not in sub.code:
        return 'no_return.html'

def incorrect_return_type (sub):
    """ Diagnoses an incorrect return type. 

    Tends to be a result of either:
    * Missing a return statement completely.
    * Returning a variable that is of the wrong type.
    * Having return statements inside an if statement and 
        no return at the end and so code is not guaranteed to 
        reach return.

    """
    diagnostics = ['return expected',
                    'This method must return a result of type']
    for diagnostic in diagnostics:
        if diagnostic in sub.report:
            return('incorrect_return_type.html')

def unreachable_code (sub):
    """ Diagnoses unreachable code errors.

    Tends to be a result of having code in the 
    sam branch following a return statement.

    """
    if 'Unreachable code' in sub.report:
        return('unreachable_code.html')

def too_many_curly_braces (sub):
    """ Diagnoses too many curly braces. 

    Trying to close the method them selves even though 
        compilation engine does it for them.

    """
    if 'Syntax error on token "}", delete this token' in sub.report:
        return('too_many_curly_braces.html')

def accessing_non_array (sub):
    """ Diagnoses attempts to access non-arrays using square braces.

    Tends to be due to accidentally using the wrong variable or using 
        python style string indexing rather than using the charAt(int)
        string method.

    """
    if 'The type of the expression must be an array type but it resolved to' in sub.report:
        return('accessing_non_array.html')

def empty_square_braces (sub):
    """ Diagnoses empty square braces. """
    diagnostic = 'Syntax error on token "[", Expression expected after this token'
    if diagnostic in sub.report:
        return('empty_square_braces.html')

def variable_not_initialized (sub):
    """ Diagnoses variables that are not initialized but are declared.

    Tends to be the use of summing or iterative 
        varibles that are not set to zero.

    """
    match = re.search(r'The local variable \w* may not have been initialized',
                        sub.report)
    if match:
        return('variable_not_initialized.html')

def using_length_as_method (sub):
    """ Diagnoses the use of length as a method on an array. """
    diagnostic = 'Cannot invoke length() on the array type'
    if diagnostic in sub.report:
        return('length_as_a_method.html')


def including_main_header (sub):
    """ Diagnoses the student putting in unnessasary code.

    Code snippet is wrapped in method header and placed in file 
        by compiler backend so students don't have to include it.
        When they do, it causes compiler errors.

    """
    if 'void main(String' in sub.code:
        return('including_main_header.html')


def including_method_header (sub):
    """ Diagnoses including method header which is done by the compiler. """
    match = re.search(r'(public|private) \w*(\[\])? .+\(.+\).*\n?{?', sub.code)
    if match and 'public static void main(String args[])' not in match.group():
        return('including_method_header.html')


def single_quotes_string (sub):
    """ Diagnoses the use of single quote strings. """
    diagnostic = 'Invalid character constant'
    if diagnostic in sub.report:
        return('single_quotes_string.html')

def invalid_assignment_operator (sub):
    """ Diagnoses an incorrect assignment.

    Ususally occurs when the programmer accidentally assigns using an 
        operator that is not the equals operator or when they attempt 
        to change a variable without assigning it back to its name.
        e.g. var + 1 instead of var += 1

    """
    match = re.search(r'Syntax error on token ".+", invalid AssignmentOperator',
                        sub.report)
    if match:
        return('invalid_assignment_operator')

def predicate_combination_operators_undefined (sub):
    """ Diagnoses the incorrect usage of the && and || operators.

    Usually as a result of one of the predicates not actually being a 
        conditional.

    """
    match = re.search(r'The operator (\&\&|\|\||\!) is undefined for the argument',
                        sub.report)
    if match:
        return('predicate_combination_operators_undefined.html')


def else_syntax_error (sub):
    """ Diagnoses not closing an if statement with a curly brace 
        before leading on with an else or if else statement. 

    """
    match = re.search(r'if\s?\(.*\);\s? {', sub.code)
    diagnostic = 'Syntax error on token "else", delete this token'
    if match and diagnostic in sub.report:
        return("else_syntax_error.html")

def variable_type_on_right_hand_side_of_equals (sub):
    """ Diagnoses including the variable type on the right at assingment. 

    Negative lookahead on int(?!e) stops the incorrect call to Integer
    being included. (People often spell 'Integer' as 'integer' or 
        'interger')

    """
    match = re.search(r'=\s*(int(?!e)|double|String|boolean|char)(\[\])?', sub.report)
    if match:
        return('variable_type_on_right_hand_side_of_equals.html')

def variable_type_in_brackets (sub):
    """ Diagnoses wrapping the variable type in brackets at declaration time.

    e.g.    (int) i = 50;
            (String) s = "Hello";

    """
    match = re.search(r'\((int|double|String)\)\s*\w+\s*=', sub.report)
    if match:
        return('variable_type_in_brackets.html')

def missing_closing_bracket (sub):
    """ Diagnoses a missing closing brace. """
    diagnostics = ['insert ")',
                    ') expected']
    for diagnostic in diagnostics:
        if diagnostic in sub.report:
            return('missing_closing_bracket.html')
            break

def too_many_closing_braces (sub):
    diagnostic = 'Syntax error on token ")", delete this token'
    if diagnostic in sub.report:
        return('too_many_closing_braces.html')

def casting_error (sub):
    """ Diagnoses improper casting e.g. int x = (int) "Dave"; """
    match = re.search(r'Cannot cast from .* to .*', sub.report)
    if match:
        return('casting_error.html')

def incorrect_operator_usage (sub):
    """ Diagnoses the incorrect usage of a basic operator.

    An example of this is attempting to subtract two strings from one another, or 
    any other type of operator overloading that java does not support.

    """
    match = re.search(r'The operator [\+\-\\\*\%] is undefined for the argument type\(s\)',
                        sub.report)
    if match:
        return('incorrect_operator_usage.html')

def invalid_invocation (sub):
    """ Diagnoses an attempt to invoke a method on an object 
    for which the method is not defined.

    e.g. Cannot invoke substring(int, int) on the primitive type int

    """
    match = re.search(r'Cannot invoke (?!length\(\)).* on the .* type .*',
                    sub.report)
    if match:
        return('invalid_invocation.html')

def out_of_place_semicolon (sub):
    """ Diagnoses an out of place semicolon that needs to be removed. """
    diagnostic = 'Syntax error on token ";", delete this token'
    if diagnostic in sub.report:
        return('out_of_place_semicolon.html')

def comma_next_to_bracket (sub):
    """ Diagnoses the use of a comma after a ( or before a )

    This error is more common than you would expect. 
    E.g. someMethodCall(, "X")
         someMethodCall("X",)

    """
    if "(," in sub.code or ",)" in sub.code:
        return('comma_next_to_bracket.html')

def variable_type_in_method_call (sub):
    """ Diagnoses putting the var type in a method call.

    E.g. Integer.parseInt(String "123")

    """
    match = re.search(r'=.*[\w\_]+\(.*(String|int|boolean|double|char|\w*\[\])\s\w+\s?([\(\,].*|\))',
                        sub.code)
    if match:
        return('variable_type_in_brackets.html')

def conditional_not_in_brackets (sub):
    """ Diagnoses conditional not in brackets. """
    match = re.search(r'if(?!\s*\()', sub.code)
    if match:
        return('conditional_not_in_brackets.html')

def incomplete_for_loop (sub):
    """ Diagnoses incomplete for loop. """
    diagnostic = 'to complete ForStatement'
    if diagnostic in sub.report:
        return('incomplete_for_loop.html')

def out_of_place_new (sub):
    """ Diagnoses an out of place new. 

    Generally the programmer accidentally tries to construct a 
        new object somewhere a method call and misuse the new keyword.

    """
    diagnostic = 'Syntax error on token "new", delete this token'
    if diagnostic in sub.report:
        return('out_of_place_new.html')

def invalid_variable_name (sub):
    """ Diagnoses an invalid variable name.

    Examples seen are using the var names:
        * new
        * names beginning with a number
        * names that are lesser known keywords e.g. char or byte.

    """
    diagnostic = 'invalid VariableDeclarator'
    if diagnostic in sub.report:
        return('invalid_variable_name.html')

# One of the most general cases of incorrect if statement
# In this case it would be best just to show the user a correct 
#   if statement,
def incorrect_if_statement (sub):
    """ Diagnoses a generally incorrect or incomplete if statement """
    diagnostics = ['Syntax error on token "else"',
                    'Syntax error on token "if"',
                    'to complete IfStatement']
    for diagnostic in diagnostics:
        if diagnostic in sub.report:
            return('incorrect_if_statement.html')
            break

def multiple_returns (sub):
    """ Diagnoses attempts to return muliple things at once. """
    match = re.search(r'return\s?\(\s?(\w+\s?,)+\s?\w+\)',
                        sub.code)
    if match:
        return('multiple_returns.html')

def single_equals_comparsion (sub):
    """ Diagnoses trying to compare using a single equals. """
    diagnostics = ['Syntax error on token "=", <= expected',
                    'Syntax error on token "=", != expected',
                    'Syntax error on token "=", >= expected']
    for diagnostic in diagnostics:
        if diagnostic in sub.report:       
            return('single_equals_comparsion.html')
            break

def missing_outer_brackets_on_conditional (sub):
    """ Diagnoses missing outer braces on a conditional.

    Generally the result of using a conditional combinator without 
        having the braces around it to from a complete if statement.
        e.g. if (x==10) && (y==8) {}

    """
    diagnostic = 'invalid OnlySynchronized'
    if diagnostic in sub.report:
        return('missing_outer_brackets_on_conditional.html')

# Check this last
def expected_assignment_operator (sub):
    """ Diagnoses expected AssignmentOperator. """
    diagnostic = 'AssignmentOperator expected after this token'
    if diagnostic in sub.report:
        return('expected_assignment_operator.html')

def if_without_conditional (sub):
    """ Diagnoses using an if without testing it against a conditional. """
    match = re.search(r'if\s*{', sub.code)
    if match:
        return('if_without_conditional.html')

def incorrect_increment_or_decrement (sub):
    """ Diagnoses an illegal increment or decrement. """
    diagnostics = ['Syntax error on token "++", delete this token',
                    'Syntax error on token "--", delete this token',
                    'Syntax error on token "++", Expression expected after this token',
                    'Syntax error on token "--", Expression expected after this token']
    for diagnostic in diagnostics:
        if diagnostic in sub.report:
            return('incorrect_increment_or_decrement.html')
            break

def invalid_character (sub):
    """ Diagnoses an invalid character, appeared as a \ after a semicolon. """
    diagnostic = 'Syntax error on token "Invalid Character", delete this token'
    if diagnostic in sub.report:
        return('invalid_character.html')
