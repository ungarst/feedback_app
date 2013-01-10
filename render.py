import re

def get_caret_index (line):
    return line.find('^'), line.rfind('^')+1
    

def render_line (report, i):
    start, stop = get_caret_index(report[i+1]) 
    line = report[i]
    return line[0:start] + '<span style = "color: #F00; font-weight: 900;">' + line[start:stop] + '</span>' + line[stop:].decode('utf-8')

def accessing_non_array (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines):
        if 'The type of the expression must be an array type but it resolved to' in line:
            i -= 2
            break
    return render_line(report_lines, i)

def empty_square_braces (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines):
        if 'Syntax error on token "[", Expression expected after this token' in line:
            i -= 2
            break
    return render_line(report_lines, i)

def casting_error (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines):
        match = re.search(r'Cannot cast from .* to .*', line)
        if match:
            i -= 2
            break
    return render_line (report_lines, i)

def duplicate_variable (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines):
        if 'Duplicate local variable' in line:
            i -= 2
            break
    return render_line(report_lines, i)

def incomplete_for_loop (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines):
        if 'to complete ForStatement' in line:
            i -= 2
            break

    if report_lines[i].startswith('catch'):
        return None

    return render_line(report_lines, i)

def incorrect_arguments (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines):
        match = re.search(r'The method .* in the type .* is not applicable for the arguments', line)
        if match:
            i -= 2
            break
    return render_line(report_lines, i)

def incorrect_increment_or_decrement (sub):
    diagnostics = ['Syntax error on token "++", delete this token',
                    'Syntax error on token "--", delete this token',
                    'Syntax error on token "++", Expression expected after this token',
                    'Syntax error on token "--", Expression expected after this token'
            ]

    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines):
        print line
        for diagnostic in diagnostics:
            if diagnostic in line:
                i -= 2
                break

    return render_line(report_lines, i)

def invalid_variable_name (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines):
        if 'invalid VariableDeclarator' in line:
            i -= 2
            break
    return render_line(report_lines, i)

def using_length_as_method (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines):
        if 'Cannot invoke length() on the array type' in line:
            i -= 2
            break
    return render_line(report_lines, i)

def invalid_invocation (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines): 
        match = re.search(r'Cannot invoke (?!length\(\)).* on the .* type .*',
                            line)
        if match:
            i -= 2
            break

    return render_line(report_lines, i)

def incorrect_operator_usage (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines): 
        match = re.search(r'The operator [\+\-\\\*\%] is undefined for the argument type\(s\)',
                    line)

        if match:
            i -= 2
            break

    return render_line(report_lines, i)

def missing_outer_brackets_on_conditional (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines):
        if 'invalid OnlySynchronized' in line:
            i -= 2
            break
    return render_line(report_lines, i)

def multiple_returns (sub):
    match = re.search(r'return\s?\(\s?(\w+\s?,)+\s?\w+\)',
                        sub.code)
    return match.group()

def out_of_place_new (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines):
        if 'Syntax error on token "new", delete this token' in line:
            i -= 2
            break
    return render_line(report_lines, i)

def missing_semicolon (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines):
        if 'Syntax error, insert ";"' in line:
            i -= 2
            break
    return render_line(report_lines, i)

def single_quotes_string (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines):
        if 'Invalid character constant' in line:
            i -= 2
            break
    return render_line(report_lines, i)

def undefined_library_method (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines): 
        match = re.search(r'The method [\w\.\(\),\s]+ is undefined for the type (?!user)\w*', 
            line)

        if match:
            i -= 2
            break

    return render_line(report_lines,i)

def variable_not_initialized (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines): 
        match = re.search(r'The local variable \w* may not have been initialized',
            line)

        if match:
            i -= 2
            break

    return render_line(report_lines,i)


def variable_cannot_be_resolved (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines): 
        match = re.search(r'[\w\_]+ cannot be resolved(?! to a type)', 
            line)
    
        if match:
            i -= 2
            break

    return render_line(report_lines, i)

def type_cannot_be_resolved (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines): 
        match = re.search(r'[\w\_]+ cannot be resolved to a type', 
            line)

        if match:
            i -= 2
            break

    return render_line(report_lines, i)

def unreachable_code (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines):
        if 'Unreachable code' in line:
            i -= 2
            break
    return render_line(report_lines, i)

def type_mismatch_return (sub):
        report_lines = sub.report.split('\n')
        for i, line in enumerate(report_lines):
            if 'Type mismatch' in line:
                i -= 2
                break
                
        if 'return' in report_lines[i]:
            return render_line(report_lines, i)

def type_mismatch (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines): 
        match = re.search(r'Type mismatch: cannot convert from \w* to \w*', 
            line)

        if match:
            i -= 2
            break

    return render_line(report_lines, i)

def illegal_modifier (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines):
        if 'Illegal modifier' in line:
            i -= 2
            break
    return render_line(report_lines, i)

def predicate_operators_undefined (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines): 
        match = re.search(r'The operator (\=\=|\!\=|\<\=|\>\=) is undefined for the argument type\(s\)',
                        line)
        match2 = re.search(r'Incompatible operand types \w+ and \w+', line)
        if match or match2:
            i -= 2
            break
    return render_line(report_lines, i)   

def out_of_place_semicolon (sub):
    report_lines = sub.report.split('\n')
    for i, line in enumerate(report_lines):
        if 'Syntax error on token ";", delete this token' in line:
            i -= 2
            break
    return render_line(report_lines, i)
