import inspect

# Function to print tracking information, given a percentage and some additional data.
def print_tracking(*args) -> None:
    print("{:.2f}".format(args[0]), '% |', args[1])

# Function to get the class name from the call stack at the specified stack level (default: 1).
def get_classname_stack(stack_level: int = 1) -> str:
    try:
        # Get the local variables of the calling frame (frame at the specified stack level).
        calling_frame_locals = inspect.stack()[stack_level][0].f_locals

        # Retrieve the 'self' variable from the local variables (assuming it's an instance method).
        # Then, access the class name using '__class__.__name__'.
        class_name = calling_frame_locals['self'].__class__.__name__

        return class_name
    except KeyError:
        # If 'self' is not found or there's no class name, return None.
        return None

# Function to get the function name from the call stack at the specified stack level (default: 1).
def get_funcname_stack(stack_level: int = 1) -> str:
    try:
        # Access the 'function' attribute of the calling frame (frame at the specified stack level).
        function_name = inspect.stack()[stack_level].function
        return function_name
    except KeyError:
        # If the function name is not found, return None.
        return None