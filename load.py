# varhandler/load.py

def parse_line(line, parse_delimiter):
    """
    Parse a line into variable and value based on the given delimiter.

    Parameters:
        line (str): The line to parse.
        parse_delimiter (str): Delimiter used for parsing the line.

    Returns:
        tuple: Variable and value extracted from the line.
    """
    parts = line.strip().split(parse_delimiter)
    if len(parts) == 2:
        variable = parts[0].strip()
        value = parts[1].strip()
        return variable, value
    else:
        return None, None

def load_variables(file, parse_delimiter):
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
        print (value)
        # Remove quotes from the value
        if type(value)==str:
            if value is not None and value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
        if variable: 
            variables[variable] = value

    return variables

def load(file, datatype=None, parse_delimiter='='):
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
            # Check if the value matches the specified datatype
            if (datatype == str and (val.startswith('"') and val.endswith('"')) or
                    (val.startswith("'") and val.endswith("'"))) or \
               (datatype == int and val.isnumeric()) or \
               (datatype == float and is_float(val)) or \
               (datatype == list and val.startswith('[') and val.endswith(']')) or \
               (datatype == tuple and val.startswith('(') and val.endswith(')')) or \
               (datatype == dict and val.startswith('{') and val.endswith('}')):
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
    """
    Search for a specific variable in the loaded variables and return its value.

    Parameters:
        file (str): Path to the file where variables will be loaded from.
        value (str): Name of the variable to search for.
        delimiter (str): Delimiter used for loading variables (default: '=').
        parse_delimiter (str): Delimiter used for parsing lines in the file (default: '=').

    Returns:
        str: Value of the specified variable.

    Raises:
        ValueError: If the variable is not found.
    """
    with open(file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        variable, val = parse_line(line, parse_delimiter)
        if variable and variable.strip() == value:
            return val.strip()

    raise ValueError(f"Variable '{value}' not found in the loaded file.")
