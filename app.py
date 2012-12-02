from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
import recognizer
import os

app = Flask(__name__)

error_files = {
    'Illegal predicate operation' : 'illegal_predicate_operation.html',
    'Missing Semicolon' : 'missing_semicolon.html',
    'Trying to compare two things that cannot be compared' : 'predicate_operators_undefined.html',
    'Missing closing curly brace' : 'missing_closing_curly_brace.html',
    'Missing opening curly brace' : 'missing_opening_curly_brace.html',
    'Cannot be resolved' : 'variable_cannot_be_resolved.html',
    'Undefined library method' : 'undefined_library_method.html',
    'Undefined user method' : 'undefined_user_method.html',
    'Incorrect arguments' : 'incorrect_arguments.html',
    'No double equals' : 'not_double_equals.html',
    'Assigning to non variable' : 'assigning_to_non_variable.html',
    'Type mismatch' : 'type_mismatch.html',
    'Duplicate variable' : 'duplicate_variable.html',
    'Illegal modifiers' : 'illegal_modifier.html',
    'None equals assignment' : 'assingment_not_using_equals.html',
    'Wrong or no return type' : 'incorrect_return_type.html',
    'Unreachable code' : 'unreachable_code.html',
    'Too many curly braces' : 'too_many_curly_braces.html',
    'Non array access' : 'accessing_non_array.html',
    'Empty square braces' : 'empty_square_braces.html',
    'Variable not initialized' : 'variable_not_initialized.html',
    'Used length as a method' : 'length_as_a_method.html',
    'Including main method header' : 'including_main_header.html',
    'Including method header' : 'including_method_header.html',
    'Single quote string' : 'single_quotes_string.html',
    'Invalid assignment operator' : 'invalid_assignment_operator.html',
    'Incorrect use of && or ||' : 'predicate_combination_operators_undefined.html',
    'Else syntax error' : 'else_syntax_error.html',
    'Variable type on right hand side of assignment' : 'variable_type_on_right_hand_side_of_equals.html',
    'Varible type wrapped in brackets at declaration' : 'variable_type_in_brackets.html',
    'Requires a closing bracket to be completed' : 'missing_closing_bracket.html',
    'Too many closing braces' : 'too_many_closing_braces.html',
    'Casting error' : 'casting_error.html',
    'Incorrect assignmet in conditional' : 'incorrect_assignment_in_conditional.html',
    'Incorrect operator usage' : 'incorrect_operator_usage.html',
    'Invalid invocation of method' : 'invalid_invocation.html',
    'Out of place semicolon' : 'out_of_place_semicolon.html',
    'Illegal use of comma next to bracket' : 'comma_next_to_bracket.html',
    'Puts variable type in front of variable name in method call' : 'variable_type_in_method_call.html',
    'Conditional not in brackets' : 'conditional_not_in_brackets.html',
    'Incomplete forloop' : 'incomplete_for_loop.html',
    'Out of place new' : 'out_of_place_new.html',
    'Invalid variable name' : 'invalid_variable_name.html',
    'Incorrect if statement' : 'incorrect_if_statement.html',
    'Returning multiple things' : 'multiple_returns.html',
    'Using a single equals to compare' : 'single_equals_comparison.html',
    'Missing outer braces' : 'missing_outer_brackets_on_conditional.html',
    'Assignment to variable expected' : 'expected_assignment_operator.html',
    'If without conditional' : 'if_without_conditional.html',
    'Illegal increment or decrement' : 'incorrect_increment_or_decrement.html',
    'InvalidCharacter' : 'invalid_character.html',
    'No match' : 'no_match.html'    
}

@app.route('/')
def index():
    return '<h1><a href="{}">click here for feedback</a></h1>'.format(url_for('feedback'))

@app.route('/recog')
def recog ():
	return recognizer.test_method()

@app.route('/report', methods=['GET', 'POST'])
def report ():
    code = request.form['code']
    errors = request.form['errors']
    return render_template('errors/' + error_files[recognizer.diagnose(code, errors)])

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """Registers the user."""
    return render_template('feedback.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
