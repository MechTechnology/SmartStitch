import inspect


def print_tracking(*args) -> None:
    print("{:.2f}".format(args[0]), '% |', args[1])


def get_classname_stack(stack_level: int = 1) -> str:
    try:
        return inspect.stack()[stack_level][0].f_locals['self'].__class__.__name__
    except KeyError:
        return None


def get_funcname_stack(stack_level: int = 1) -> str:
    try:
        return inspect.stack()[stack_level].function
    except KeyError:
        return None
