# varhandler/get.py
def parse_line(line, parse_delimiter):
    parts = line.strip().split(parse_delimiter)
    if len(parts) == 2:
        variable = parts[0].strip()
        value = parts[1].strip()
        return variable, value
    else:
        return None, None

def evaluate_expression(value, variables):
    try:
        # Evaluate the expression if it's a valid expression
        converted_value = convert_expression(value, variables)
        result = eval(converted_value)
        
        return result
    except (ValueError, SyntaxError, NameError, ZeroDivisionError):
        return value  # Return the original value if evaluation fails

def convert_expression(expression, variables):
    operators = set(['+', '-', '*', '/', '**', '%', '//', '(', ')', '[', ']', '{', '}'])

    def tokenize(expression):
        tokens = []
        current_token = ''
        i = 0

        while i < len(expression):
            char = expression[i]

            if char in operators:
                if current_token:
                    tokens.append(current_token)
                tokens.append(char)
                current_token = ''
            elif char.isdigit() or (char == '-' and (i == 0 or expression[i-1] in operators) and (i + 1 < len(expression) and expression[i+1].isdigit())):
                current_token += char
            else:
                if current_token:
                    tokens.append(current_token)
                current_token = char

            i += 1

        if current_token:
            tokens.append(current_token)

        return tokens

    def is_valid_variable(token):
        return token.isalpha() and token not in operators

    tokens = tokenize(expression)
    converted_tokens = []

    for token in tokens:
        if is_valid_variable(token):
            converted_tokens.append(f"variables['{token}']")
        elif token.isnumeric() or (token[0] == '-' and token[1:].isnumeric()):
            converted_tokens.append(token)
        else:
            converted_tokens.append(token)

    return ''.join(converted_tokens)

def load_variables(file, parse_delimiter='='):
    """
    Load variables from a file and return as a dictionary.

    Parameters:
        file (str): Path to the file where variables will be loaded from.
        parse_delimiter (str): Delimiter used for parsing lines in the file.

    Returns:
        dict: Dictionary containing the loaded variables.
    """
    variables = {}
    with open(file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        variable, value = parse_line(line, parse_delimiter)
        if variable:
            # Remove quotes from the value
            # Evaluate the expression and store the result
            evaluated_value = evaluate_expression(value, variables)
            variables[variable] = evaluated_value

    return variables
def get(file, datatype=None, parse_delimiter='='):
    """
    Load variables from a file and filter based on datatype.

    Parameters:
        file (str): Path to the file where variables will be loaded from.
        datatype (type): Desired data type for filtering variables (default: None).
        parse_delimiter (str): Delimiter used for parsing lines in the file (default: '=').

    Returns:
        dict: Dictionary containing the loaded and filtered variables.
    """
    variables = load_variables(file, parse_delimiter)

    # Filter variables based on datatype if specified
    if datatype:
        filtered_variables = {}
        for var, val in variables.items():
            if ((datatype == str and isinstance(val, str)) or
                (datatype == int and isinstance(val, int)) or
                (datatype == float and isinstance(val, float)) or
                (datatype == list and val.startswith('[') and val.endswith(']')) or
                (datatype == tuple and val.startswith('(') and val.endswith(')')) or
                (datatype == dict and val.startswith('{') and val.endswith('}'))):
                filtered_variables[var] = val

        return filtered_variables

    return variables


def is_float(value):
    """
    Check if the value is a float.

    Parameters:
        value (str): The value to check.

    Returns:
        bool: True if the value is a float, False otherwise.
    """
    try:
        float_value = float(value)
        # Check if the float has a decimal point
        if float_value.is_integer():
            return False
        return True
    except ValueError:
        return False
    
def search(file, value, delimiter='=', parse_delimiter='='):
    try: 
        variables = load_variables(file, parse_delimiter)
        val = variables[value]
        final = str(str(value)+delimiter+str(val))
        return final
    except KeyError:
        raise ValueError(f"Variable '{value}' not found in the loaded file.")
    
def valueOf(file, value, parse_delimiter='='):
    try: 
        variables = load_variables(file, parse_delimiter)
        val = variables[value]
        return val
    except KeyError:
        raise ValueError(f"Variable '{value}' not found in the loaded file.")
    
def exists(file, value, parse_delimiter='='):
    variables = load_variables(file, parse_delimiter)
    return value in variables
