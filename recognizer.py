import submission, detector, lexer, render, re

possible_errors = [
            (detector.variable_cannot_be_resolved , render.variable_cannot_be_resolved),
            (detector.incorrect_return_type , render.incorrect_return_type), #only when with "must return a result of type..."
            (detector.missing_semicolon , render.missing_semicolon),
            (detector.type_mismatch_return, render.type_mismatch_return),
            (detector.no_return, False), #no need for a line to be shown
            (detector.type_mismatch , render.type_mismatch),
            (detector.missing_closing_curly_brace , False), #line is simply "}" no use in showing and no line numbers
            (detector.else_syntax_error , render.else_syntax_error), 
            (detector.conditional_not_in_brackets , render.conditional_not_in_brackets),
            (detector.if_without_conditional , render.if_without_conditional),
            (detector.incorrect_if_statement , False), #too general, see nonrender file
            (detector.missing_closing_bracket , False),
            (detector.duplicate_variable , render.duplicate_variable),
            (detector.too_many_curly_braces , False), #line is simply "}" no use in showing and no line numbers
            (detector.missing_opening_curly_brace, False),
            (detector.incorrect_arguments , render.incorrect_arguments),
            (detector.variable_not_initialized , render.variable_not_initialized),
            (detector.unreachable_code , render.unreachable_code), 
            (detector.including_method_header , False),
            (detector.undefined_user_method , False),
            (detector.undefined_library_method , render.undefined_library_method),
            (detector.invalid_invocation , render.invalid_invocation),
            (detector.variable_type_on_right_hand_side_of_equals , render.variable_type_on_right_hand_side_of_equals),
            (detector.type_cannot_be_resolved , render.type_cannot_be_resolved),
            (detector.too_many_closing_braces , render.too_many_closing_braces),
            (detector.invalid_assignment_operator , render.invalid_assignment_operator),
            (detector.single_equals_comparison , render.single_equals_comparison),
            (detector.predicate_operators_undefined , render.predicate_operators_undefined),
            (detector.incorrect_operator_usage , render.incorrect_operator_usage),
            (detector.predicate_combination_operators_undefined , render.predicate_combination_operators_undefined),
            (detector.empty_square_braces , render.empty_square_braces),
            (detector.assignment_not_using_equals , render.assignment_not_using_equals),
            (detector.illegal_predicate_operation , render.illegal_predicate_operation),
            (detector.single_quotes_string , render.single_quotes_string),
            (detector.using_length_as_method , render.using_length_as_method),
            (detector.not_double_equals , render.not_double_equals),
            # need to get up to here to get most of the errors
            (detector.casting_error , render.casting_error),
            (detector.out_of_place_semicolon , render.out_of_place_semicolon),
            (detector.assigning_to_non_variable , False),
            (detector.accessing_non_array , render.accessing_non_array),
            (detector.invalid_variable_name , render.invalid_variable_name),
            (detector.missing_outer_brackets_on_conditional , render.missing_outer_brackets_on_conditional),
            (detector.out_of_place_new , render.out_of_place_new),
            (detector.invalid_character , False),
            (detector.incorrect_increment_or_decrement , render.incorrect_increment_or_decrement),
            (detector.variable_type_in_method_call , False),
            (detector.incomplete_for_loop , render.incomplete_for_loop),
            (detector.illegal_modifier , render.illegal_modifier),
            (detector.variable_type_in_brackets , False),
            (detector.including_main_header , False),
            (detector.comma_next_to_bracket , False),
            (detector.multiple_returns , render.multiple_returns),
            (detector.expected_assignment_operator , False)
            ]

def diagnose (code, error):

      sub = submission.Submission(lexer.begin_lex(code), error)

      for poss_error in possible_errors:
            detected = poss_error[0](sub)
            if detected:
                  with open('errors/' + detected, "r") as f:
                        data = f.read()

                  if poss_error[1]:
                        line = poss_error[1](sub)
                        print "Can render"
                        if line:
                              print "GOt line - " + line
                              data = data.replace( "<LINE>" , line)
                        else:
                              print "no line"
                              data = data.replace( """<div style = "margin: 20px;">
      <p style="font-family: courier; font-size: 120%; color: #000;">
            <span style = "background-color: #ffff99; padding: 10px; border: 1px solid #cc0;">
            <LINE>
            </span>
      </p>
</div>""" , "") 
                        
                        
                  return data

      if not detected:
            return '<pre>' + error + '</pre>'

                  


            
