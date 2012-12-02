#!/usr/bin/python

import sys
import re
import operator
import os

MULTILINE_COMMENT_EXPR = re.compile(r"/\*.*?\*/")
EOL_COMMENT_EXPR = re.compile(r"//.*?\n")

def lex_multiline_comment(s):
    match = MULTILINE_COMMENT_EXPR.match(s)
    if match is not None:
        return [('multiline_comment', match.group(0))], s[len(match.group(0)):]
    else:
        return [], s


def lex_eol_comment(s):
    match = EOL_COMMENT_EXPR.match(s)
    if match is not None:
        return [('eol_comment', match.group(0))], s[len(match.group(0)):]
    else:
        return [], s


def lex_string(s):
    if s[0] != '"':
        return [], s

    buf = ['"']
    it = iter(s)
    next(it)

    for c in it:
        if c == '"':
            break

        if c == '\\':
            # ignore the next character, whatever it is
            buf.append(c)
            buf.append(next(it))
            continue

        buf.append(c)

    return [('string', ''.join(buf))], ''.join(it)


def lex_program(s):
    tokens = []
    while s:
        matched = False
        for rule in [lex_multiline_comment, lex_eol_comment, lex_string]:
            next_tokens, s = rule(s)

            if next_tokens:
                tokens.extend(next_tokens)
                matched = True
                break

        if not matched:
            tokens.append(('passthru', s[0]))
            s = s[1:]

    return tokens


def begin_lex(s):
    cleaned = []
    for tag, token in lex_program(s):
        if tag == 'passthru':
            cleaned.append(token)
        elif tag == 'string':
            cleaned.append('$STRING$')
        elif tag == 'eol_comment':
        	cleaned.append('$EOL_COMMENT$\n')

    return ''.join(cleaned)

class Submission(object):
	
	def __init__ (self, info, code, report):
		self.info = info
		self.code = begin_lex(code)
		self.report = report
		self.errors = []




	def is_matched (self):
		""" Returns true if at least on of the errors has been matched. """
		return self.errors

	def diagnose (self):
		""" Diagnoses the submission's error messages.

		Goes through all diagnostic methods attempting to match 
			the error message with a diagnostic.
		More diagnostics can be added by writing a diagnostic method
			which appends the problem to the objects errors list and 
			inserting the method into the possible_errors list.

		"""
		possible_errors = [
					self.missing_semicolon_diagnose,
					self.illegal_predicate_operation,
					self.missing_closing_curly_brace_diagnose,
					self.missing_opening_curly_brace_diagnose,
					self.variable_cannot_be_resolved,
					self.undefined_library_method,
					self.undefined_user_method,
					self.not_double_equals,
					self.assigning_to_non_variable,
					self.type_mismatch,
					self.duplicate_variable,
					self.illegal_modifier,
					self.assignment_not_using_equals,
					self.incorrect_return_type,
					self.unreachable_code,
					self.too_many_curly_braces,
					self.accessing_non_array,
					self.empty_square_braces,
					self.variable_not_initialized,
					self.using_length_as_method,
					self.including_main_header,
					self.including_method_header,
					self.single_quotes_string,
					self.invalid_assignment_operator,
					self.predicate_combination_operators_undefined,
					self.predicate_operators_undefined,
					self.else_syntax_error,
					self.variable_type_on_right_hand_side_of_equals,
					self.variable_type_in_brackets,
					self.missing_closing_bracket,
					self.too_many_closing_braces,
					self.casting_error,
					self.incorrect_assignment_in_conditional,
					self.incorrect_operator_usage,
					self.invalid_invocation,
					self.out_of_place_semicolon,
					self.comma_next_to_bracket,
					self.variable_type_in_method_call,
					self.conditional_not_in_brackets,
					self.incomplete_for_loop,
					self.out_of_place_new,
					self.invalid_variable_name,
					self.incorrect_if_statement,
					self.multiple_returns,
					self.single_equals_comparsion,
					self.incorrect_arguments,
					self.missing_outer_brackets_on_conditional,
					self.expected_assignment_operator,
					self.if_without_conditional,
					self.incorrect_increment_or_decrement,
					self.invalid_character
					]
		for x in possible_errors: x()
		return self.errors

		#if len(self.errors) == 0:
		#	if 'Syntax error on token' in self.report:
		#		#print 'Unknown'
		#		self.errors.append('Unknown token error')

	def missing_semicolon_diagnose (self):
		""" Diagnoses a missing semicolon error. """
		if 'Syntax error, insert ";"' in self.report:
			self.errors.append('Missing Semicolon')



	def illegal_predicate_operation (self):
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
							self.report)
		if match:
			self.errors.append('Illegal predicate operation')


	def predicate_operators_undefined (self):
		""" Diagnoses the improper use of predicate operators.

		Ususally the result of people putting the equals sign in the wrong place 
		e.g. =! rather than != and => rather than >=

		"""
		match = re.search(r'The operator (\=\=|\!\=|\<\=|\>\=) is undefined for the argument type\(s\)',
							self.report)
		match2 = re.search(r'Incompatible operand types \w+ and \w+', self.report)
		if match or match2:
			self.errors.append('Trying to compare two things that cannot be compared')

	def missing_closing_curly_brace_diagnose (self):
		""" Diagnoses a missing curly brace error. """
		if 'Syntax error, insert "}"' in self.report:
			self.errors.append('Missing closing curly brace')

	def missing_opening_curly_brace_diagnose (self):
		""" Diagnoses a missing opening curly brace error. """
		diagnostic = "{ expected"
		if diagnostic in self.report:
			self.errors.append('Missing opening curly brace')

	def variable_cannot_be_resolved (self):
		""" Diagnoses a variable not resolve error. """
		match = re.search(r'[\w\_]+ cannot be resolved', self.report)
		if match:
			self.errors.append('Cannot be resolved')

	def undefined_library_method (self):
		""" Diagnoses a undefined library method error.

		It will only diagnose an error if the code is trying to invoke a
			method on an object that it doesn't have, or is trying to call 
			a static method that doesn't exist from a library.
		It doesn't diagnose an undefined method that should have been implemented 
			by the user.

		"""
		match = re.search(r'The method [\w\.\(\),\s]+ is undefined for the type (?!user)\w*', 
				self.report)
		if match: 
			self.errors.append('Undefined library method')

	def undefined_user_method (self):
		""" Diagnoses a undefined library method error.

		It will only diagnose missing methods that should be implemented by the 
			programmer, not ones that should be defined in the programming language.

		Relies on the fact that the name of the class that the method is placed into 
			begins with 'user'.

		"""
		match = re.search(r'The method [\w\.\,\(\) ]+ is undefined for the type user', 
				self.report)
		if match: 
			self.errors.append('Undefined user method')

	def incorrect_arguments (self):
		""" Diagnoses the error of incorrect arguments to a method. """
		match = re.search(r'The method .* in the type .* is not applicable for the arguments', self.report)
		if match:
			self.errors.append('Incorrect arguments')

	def not_double_equals (self):
		""" Diagnoses the error of attempting to compare two 
		things using a single equals.

		"""
		match = re.search(r'if\s*\(.*=(?!=).*\)', self.report)
		if match and 'The left-hand side of an assignment must be a variable' in self.report:
			self.errors.append('No double equals')

	def assigning_to_non_variable (self):
		diagnostic = 'The left-hand side of an assignment must be a variable'
		if 'No double equals' not in self.errors and diagnostic in self.report:
			self.errors.append('Assigning to non variable')

	def type_mismatch (self):
		""" Diagnoses a type mismatch error. """
		match = re.search(r'Type mismatch: cannot convert from \w* to \w*',
				self.report)
		if match:
			self.errors.append('Type mismatch')

	def duplicate_variable (self):
		""" Diagnoses a duplicate variable error.

		These tend to be a result of the programmer redefining the 
			parameters or redefining a variable, most likely 'i' 
			used in a for loop.

		"""
		if 'Duplicate local variable' in self.report:
			self.errors.append('Duplicate variable')

	def illegal_modifier (self):
		""" Diagnoses the use of an illegal modifier.

		Often occurs when the programmer tries to make a local
			variable public..

		"""
		if 'Illegal modifier' in self.report:
			self.errors.append('Illegal modifiers')

	def assignment_not_using_equals (self):
		""" Diagnoses the error of attempting to assign not using equals.

		Usually occurs when the programmer tries to assign to a boolean 
			using a predicate e.g. boolean x == 4.

		"""
		match = re.search(r'Syntax error on token ".*", = expected',
							self.report)
		if match:
			self.errors.append('None equals assignment')

	def incorrect_return_type (self):
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
			if diagnostic in self.report:
				self.errors.append('Wrong or no return type')
				break

	def unreachable_code (self):
		""" Diagnoses unreachable code errors.

		Tends to be a result of having code in the 
		sam branch following a return statement.

		"""
		if 'Unreachable code' in self.report:
			self.errors.append('Unreachable code')

	def too_many_curly_braces (self):
		""" Diagnoses too many curly braces. 

		Trying to close the method them selves even though 
			compilation engine does it for them.

		"""
		if 'Syntax error on token "}", delete this token' in self.report:
			self.errors.append('Too many curly braces')

	def accessing_non_array (self):
		""" Diagnoses attempts to access non-arrays using square braces.

		Tends to be due to accidentally using the wrong variable or using 
			python style string indexing rather than using the charAt(int)
			string method.

		"""
		if 'The type of the expression must be an array type but it resolved to' in self.report:
			self.errors.append('Non array access')

	def empty_square_braces (self):
		""" Diagnoses empty square braces. """
		diagnostic = 'Syntax error on token "[", Expression expected after this token'
		if diagnostic in self.report:
			self.errors.append('Empty square braces')

	def variable_not_initialized (self):
		""" Diagnoses variables that are not initialized but are declared.

		Tends to be the use of summing or iterative 
			varibles that are not set to zero.

		"""
		match = re.search(r'The local variable \w* may not have been initialized',
							self.report)
		if match:
			self.errors.append('Variable not initialized')

	def using_length_as_method (self):
		""" Diagnoses the use of length as a method on an array. """
		diagnostic = 'Cannot invoke length() on the array type'
		if diagnostic in self.report:
			self.errors.append('Used length as a method')


	def including_main_header (self):
		""" Diagnoses the student putting in unnessasary code.

		Code snippet is wrapped in method header and placed in file 
			by compiler backend so students don't have to include it.
			When they do, it causes compiler errors.

		"""
		if 'public static void main(String args[])' in self.code:
			self.errors.append('Including main method header')


	def including_method_header (self):
		""" Diagnoses including method header which is done by the compiler. """
		match = re.search(r'(public|private) \w*(\[\])? .+\(.+\).*\n?{?', self.code)
		if match and 'public static void main(String args[])' not in match.group():
			self.errors.append('Including method header')


	def single_quotes_string (self):
		""" Diagnoses the use of single quote strings. """
		diagnostic = 'Invalid character constant'
		if diagnostic in self.report:
			self.errors.append('Single quote string')

	def invalid_assignment_operator (self):
		""" Diagnoses an incorrect assignment.

		Ususally occurs when the programmer accidentally assigns using an 
			operator that is not the equals operator or when they attempt 
			to change a variable without assigning it back to its name.
			e.g. var + 1 instead of var += 1

		"""
		match = re.search(r'Syntax error on token ".+", invalid AssignmentOperator',
							self.report)
		if match:
			self.errors.append('Invalid assignment operator')

	def predicate_combination_operators_undefined (self):
		""" Diagnoses the incorrect usage of the && and || operators.

		Usually as a result of one of the predicates not actually being a 
			conditional.

		"""
		match = re.search(r'The operator (\&\&|\|\||\!) is undefined for the argument',
							self.report)
		if match:
			self.errors.append('Incorrect use of && or ||')


	def else_syntax_error (self):
		""" Diagnoses not closing an if statement with a curly brace 
			before leading on with an else or if else statement. 

		"""
		diagnostic = 'Syntax error on token "else", delete this token'
		if diagnostic in self.report:
			self.errors.append('Else syntax error')

	def variable_type_on_right_hand_side_of_equals (self):
		""" Diagnoses including the variable type on the right at assingment. 

		Negative lookahead on int(?!e) stops the incorrect call to Integer
		being included. (People often spell 'Integer' as 'integer' or 
			'interger')

		"""
		match = re.search(r'=\s*(int(?!e)|double|String|boolean|char)(\[\])?', self.report)
		if match:
			self.errors.append('Variable type on right hand side of assignment')

	def variable_type_in_brackets (self):
		""" Diagnoses wrapping the variable type in brackets at declaration time.

		e.g. 	(int) i = 50;
				(String) s = "Hello";

		"""
		match = re.search(r'\((int|double|String)\)\s*\w+\s*=', self.report)
		if match:
			self.errors.append('Varible type wrapped in brackets at declaration')

	def missing_closing_bracket (self):
		""" Diagnoses a missing closing brace. """
		diagnostics = ['insert ")',
						') expected']
		for diagnostic in diagnostics:
			if diagnostic in self.report:
				self.errors.append('Requires a closing bracket to be completed')
				break

	def too_many_closing_braces (self):
		diagnostic = 'Syntax error on token ")", delete this token'
		if diagnostic in self.report:
			self.errors.append('Too many closing braces')

	def casting_error (self):
		""" Diagnoses improper casting e.g. int x = (int) "Dave"; """
		match = re.search(r'Cannot cast from .* to .*', self.report)
		if match:
			self.errors.append('Casting error')

	def incorrect_assignment_in_conditional (self):
		""" Diagnoses incorrect assignments in conditionals.

		This is generally a result of programmers trying to assign in 
			an if statement but not using their braces correctly.
			e.g. if ((x = Integer.parseInt(word)) < 3)) is correct but often people use
				if ((x = Integer.parseInt)(word < 3))

		"""
		diagnostic = 'Syntax error, insert "AssignmentOperator Expression" ' + \
						'to complete Expression'
		if diagnostic in self.report:
			self.errors.append('Incorrect assignmet in conditional')

	def incorrect_operator_usage (self):
		""" Diagnoses the incorrect usage of a basic operator.

		An example of this is attempting to subtract two strings from one another, or 
		any other type of operator overloading that java does not support.

		"""
		match = re.search(r'The operator [\+\-\\\*\%] is undefined for the argument type\(s\)',
							self.report)
		if match:
			self.errors.append('Incorrect operator usage')

	def invalid_invocation (self):
		""" Diagnoses an attempt to invoke a method on an object 
		for which the method is not defined.

		e.g. Cannot invoke substring(int, int) on the primitive type int

		"""
		match = re.search(r'Cannot invoke (?!length\(\)).* on the .* type .*',
						self.report)
		if match:
			self.errors.append('Invalid invocation of method')

	def out_of_place_semicolon (self):
		""" Diagnoses an out of place semicolon that needs to be removed. """
		diagnostic = 'Syntax error on token ";", delete this token'
		if diagnostic in self.report:
			self.errors.append('Out of place semicolon')

	def comma_next_to_bracket (self):
		""" Diagnoses the use of a comma after a ( or before a )

		This error is more common than you would expect. 
		E.g. someMethodCall(, "X")
			 someMethodCall("X",)

		"""
		if "(," in self.code or ",)" in self.code:
			self.errors.append('Illegal use of comma next to bracket')

	def variable_type_in_method_call (self):
		""" Diagnoses putting the var type in a method call.

		E.g. Integer.parseInt(String "123")

		"""
		match = re.search(r'=.*[\w\_]+\(.*(String|int|boolean|double|char|\w*\[\])\s\w+\s?([\(\,].*|\))',
							self.code)
		if match:
			self.errors.append('Puts variable type in front of variable name in method call')

	def conditional_not_in_brackets (self):
		""" Diagnoses conditional not in brackets. """
		match = re.search(r'if(?!\s*\()', self.code)
		if match:
			self.errors.append('Conditional not in brackets')

	def incomplete_for_loop (self):
		""" Diagnoses incomplete for loop. """
		diagnostic = 'to complete ForStatement'
		if diagnostic in self.report:
			self.errors.append('Incomplete forloop')

	def out_of_place_new (self):
		""" Diagnoses an out of place new. 

		Generally the programmer accidentally tries to construct a 
			new object somewhere a method call and misuse the new keyword.

		"""
		diagnostic = 'Syntax error on token "new", delete this token'
		if diagnostic in self.report:
			self.errors.append('Out of place new')

	def invalid_variable_name (self):
		""" Diagnoses an invalid variable name.

		Examples seen are using the var names:
			* new
			* names beginning with a number
			* names that are lesser known keywords e.g. char or byte.

		"""
		diagnostic = 'invalid VariableDeclarator'
		if diagnostic in self.report:
			self.errors.append('Invalid variable name')

	# One of the most general cases of incorrect if statement
	# In this case it would be best just to show the user a correct 
	# 	if statement,
	def incorrect_if_statement (self):
		""" Diagnoses a generally incorrect or incomplete if statement """
		diagnostics = ['Syntax error on token "else"',
						'Syntax error on token "if"',
						'to complete IfStatement']
		for diagnostic in diagnostics:
			if diagnostic in self.report:
				self.errors.append('Incorrect if statement')
				break

	def multiple_returns (self):
		""" Diagnoses attempts to return muliple things at once. """
		match = re.search(r'return\s?\(\s?(\w+\s?,)+\s?\w+\)',
							self.code)
		if match:
			self.errors.append('Returning multiple things')

	def single_equals_comparsion (self):
		""" Diagnoses trying to compare using a single equals. """
		diagnostics = ['Syntax error on token "=", <= expected',
						'Syntax error on token "=", != expected',
						'Syntax error on token "=", >= expected']
		for diagnostic in diagnostics:
			if diagnostic in self.report:		
				self.errors.append('Using a single equals to compare')
				break

	def missing_outer_brackets_on_conditional (self):
		""" Diagnoses missing outer braces on a conditional.

		Generally the result of using a conditional combinator without 
			having the braces around it to from a complete if statement.
			e.g. if (x==10) && (y==8) {}

		"""
		diagnostic = 'invalid OnlySynchronized'
		if diagnostic in self.report:
			self.errors.append('Missing outer braces')

	# Check this last
	def expected_assignment_operator (self):
		""" Diagnoses expected AssignmentOperator. """
		diagnostic = 'AssignmentOperator expected after this token'
		if diagnostic in self.report:
			self.errors.append('Assignment to variable expected')

	def if_without_conditional (self):
		""" Diagnoses using an if without testing it against a conditional. """
		match = re.search(r'if\s*{', self.code)
		if match and 'Conditional not in brackets' not in self.errors:
			self.errors.append('If without conditional')

	def incorrect_increment_or_decrement (self):
		""" Diagnoses an illegal increment or decrement. """
		diagnostics = ['Syntax error on token "++", delete this token',
						'Syntax error on token "--", delete this token',
						'Syntax error on token "++", Expression expected after this token',
						'Syntax error on token "--", Expression expected after this token']
		for diagnostic in diagnostics:
			if diagnostic in self.report:
				self.errors.append('Illegal increment or decrement')
				break

	def invalid_character (self):
		""" Diagnoses an invalid character, appeared as a \ after a semicolon. """
		diagnostic = 'Syntax error on token "Invalid Character", delete this token'
		if diagnostic in self.report:
			self.errors.append('InvalidCharacter')


def diagnose(code, errors):
	sub = Submission("", code, errors)
	return sub.diagnose()[0]
	



