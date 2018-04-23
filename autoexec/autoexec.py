import argparse
import inspect
from numpydoc.docscrape import FunctionDoc


__all__ = ['construct_parser', 'extract_function_arguments', 'execute_function',
           'execute_functions']


def construct_parser(function, parser=None):
    """Automatically construct an argument parser from the function signature and docstring.

    Parameters
    ----------
    function : callable
        The function that we want to turn into a script.
    parser : argparse.ArgumentParser, optional
        An existing argument parser.

    Returns
    -------
    parser : argparse.ArgumentParser
        The parser for this particular function.

    Raises
    ------
    ArgumentError
        If parser is not None and already has a corresponding argument.
    ValueError
        If it cannot automatically extract the dtype from the function.
    """
    # Try extracting the docstring
    docstring = FunctionDoc(function)
    docstring_params = {param_name: (param_type, param_doc) for
                        param_name, param_type, param_doc in docstring['Parameters']}

    # Get the function description
    if docstring['Summary']:
        description = '\n'.join(docstring['Summary'])
    else:
        description = f'The {function.__name__} function.'

    if docstring['Extended Summary']:
        description += '\n\n' + '\n'.join(docstring['Extended Summary'])

    # Construct parser if none is provided
    if parser is None:
        parser = argparse.ArgumentParser(description=description,
                                         formatter_class=argparse.RawTextHelpFormatter)

    # Set default callback for the function.
    parser.set_defaults(_function=function)

    # Go through parameters of function signature
    signature = inspect.signature(function)
    for name, parameter in signature.parameters.items():
        # Whether the parameter is a kwarg
        is_kwarg = parameter.default is not parameter.empty

        # Get the parameter dtype
        param_type = None
        if parameter.annotation is not parameter.empty:
            # Annotation is provided (e : int)
            param_type = parameter.annotation
        elif is_kwarg and parameter.default is not None:
            # Kwargs have default parameters / dtypes
            param_type = type(parameter.default)
        elif param_type is None and name in docstring_params:
            # Otherwise, let's get it from the docstring if provided
            str_type = docstring_params[name][0]
            if str_type:
                # Remove optional parameter if specified
                str_type = str_type.split(',')[0].strip()
                param_type = eval(str_type)

        if param_type is None:
            raise ValueError(f"Unable to identify type of `{name}` parameter. Please "
                             f"specify the dtype as part the annotation, kwarg, "
                             f"or in the docstring.")

        # Get the default value if it's a keyword argument
        if parameter.default is parameter.empty:
            param_default = dict(required=True)
        else:
            param_default = dict(default=parameter.default)

        # Get the parameter description if it's available
        if name in docstring_params and docstring_params[name][1]:
            param_help = '\n'.join(docstring_params[name][1])
        else:
            param_help = None
            # Nothing provided, use some sane defaults
            if param_type is not None:
                param_help = param_type.__name__

                if is_kwarg:
                    param_help += f', default: {parameter.default}'

        parser.add_argument(f'--{name}', type=param_type, help=param_help,
                            **param_default)

    return parser


def extract_function_arguments(parsed_arguments, function=None):
    """Extract the required arguments for function from parsed arguments.

    Parameters
    ----------
    parsed_arguments : argparse.Namespace
        The parsed arguments from argparse.
    function : callable
        The function for which we want to extract input arguments. If None, then
         parsed_arguments._function is used instead.

    Returns
    -------
    function : callable
        The corresponding function to evaluate.
    args : list
        The input arguments for the function.
    kwargs : dict
        The keyword arguments for the function.
    """
    args = []
    kwargs = {}
    if function is None:
        function = parsed_arguments._function

    signature = inspect.signature(function)
    for name, parameter in signature.parameters.items():

        # Handle kwargs first
        if parameter.default is not parameter.empty:
            try:
                value = getattr(parsed_arguments, name)
                kwargs[name] = value
            except AttributeError:
                continue
        else:
            args.append(getattr(parsed_arguments, name))

    return function, args, kwargs


def kwargs_to_call(function_name, **kwargs):
    """Convert kwargs to a function call compatible with `execute_function`."""
    arguments = [f'--{key}={value}' for key, value in kwargs.items()]
    return f"{function_name} {' '.join(arguments)}"


def execute_function(function):
    """Execute a function based on arguments provided.

    Specifically, this function constructs and argument parser based on the function
    annotation, default values for keyword arguments,

    The function can be executed as
    file.py --arg1_name arg1_value

    Parameters
    ----------
    function : callable, optional
        The function that we want to execute.

    Returns
    -------
    results : tuple
        The result of calling the function with the namespace parameters.

    See Also
    --------
    construct_parser
    extract_function_arguments

    """
    parser = construct_parser(function)
    parsed_arguments = parser.parse_args()

    _, args, kwargs = extract_function_arguments(parsed_arguments)
    return function(*args, **kwargs)


def execute_functions(functions):
    """Execute several functions based on arguments provided.

    Specifically, this function constructs and argument subparsers based on the function
    annotation, default values for keyword arguments. Resulting functions are called as

    file.py function_name --arg1_name arg1_value

    Parameters
    ----------
    function : callable
        The function that we want to execute.

    Returns
    -------
    results : tuple
        The result of calling the function with the namespace parameters.

    See Also
    --------
    construct_parser
    extract_function_arguments

    """
    parser = argparse.ArgumentParser(prog=__file__)
    subparsers = parser.add_subparsers(help='sub-command help', dest='sub_command')
    subparsers.required = True

    for function in functions:
        subparser = subparsers.add_parser(function.__name__)
        construct_parser(function, parser=subparser)

    parsed_arguments = parser.parse_args()
    fun, args, kwargs = extract_function_arguments(parsed_arguments)

    return fun(*args, **kwargs)
