import re

MULTILINE_COMMENT_EXPR = re.compile(r"/\*.*?\*/")
EOL_COMMENT_EXPR = re.compile(r"//.*?\n")
WHITESPACE_EXPR = re.compile(r'\s+')

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

def lex_whitespace(s):
	match = WHITESPACE_EXPR.match(s)
	if match is not None:
		return [('whitespace', match.group(0))], s[len(match.group(0)):]
	else:
		return [], s


def lex_program(s):
    tokens = []
    while s:
        matched = False
        for rule in [lex_multiline_comment, lex_eol_comment, lex_string, lex_whitespace]:
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
    	elif tag == 'whitespace':
    		cleaned.append(' ')

    return ''.join(cleaned)