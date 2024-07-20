# varhandler/save.py

def parse_line(line, parse_delimiter):
    parts = line.strip().split(parse_delimiter)
    if len(parts) == 2:
        variable = parts[0].strip()
        value = parts[1].strip()
        return variable, value
    else:
        return None, None

def save(file, save, datatype=None, delimiter='=', parse_delimiter='='):
    """
    Save variables to a file with the specified file extension.

    Parameters:
        file (str): Path to the file where variables will be loaded from.
        save (str): Path to the file where the variables will be saved.
        datatype (type): Desired data type for filtering variables (default: None).
        delimiter (str): Delimiter to use for saving variables (default: '=').

    Returns:
        dict: Dictionary containing the loaded variables.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    if '.' not in save:
        save += '.txt'

    # Load variables from the specified file (e.g., sample.py)
    original_dictionary = load_variables(file, save, parse_delimiter, datatype)

    # Save the specified variables to the specified file
    with open(save, 'w') as file:
        for name, value in original_dictionary.items():
            line = f"{name}{delimiter}{value}\n"
            file.write(line)

def search(file, save, value, delimiter='=', parse_delimiter='='):
    """
    Search for a specific variable in the loaded variables and save it to a file.

    Parameters:
        file (str): Path to the file where variables will be loaded from.
        value (str): Name of the variable to value for.
        save (str): Path to the file where the variable will be saved.
        delimiter (str): Delimiter used for saving variables (default: '=').

    Returns:
        Value of the specified variable.

    Raises:
        ValueError: If the variable is not found.
        FileNotFoundError: If the specified file does not exist.
    """
    # Load variables from the specified file
    original_dictionary = load_variables(file, save, parse_delimiter)

    # Check if the specified variable exists
    if value not in original_dictionary:
        raise ValueError(f"Variable '{value}' not found in the loaded file.")

    # Save the specified variable to the specified file
    variable_value = original_dictionary[value]
    with open(save, 'w') as save_file:
        line = f"{value}{delimiter}{variable_value}\n"
        save_file.write(line)

    return variable_value

# Helper function to filter variables by datatype and remove quotes
def load_variables(file, save, parse_delimiter='=', datatype=None):
    """
    Load variables from a file using a generic approach and save the filtered variables.

    Parameters:
        file (str): Path to the file where variables will be loaded from.
        save (str): Path to the file where the variables will be saved.
        parse_delimiter (str): Delimiter used for parsing lines in the file.
        datatype (type): Desired data type for filtering variables.

    Returns:
        dict: Dictionary containing the loaded variables.
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
    try:
        float_value = float(value)
        # Check if the float has a decimal point
        if float_value.is_integer():
            return False
        return True
    except ValueError:
        return False

