from functools import wraps
from typing import List, Callable


def requires(deps: List[Callable] = []):
    """
    Decorator which executes the functions of the list 'deps'
    before calling the decorated function

    """

    def require2(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            for f in deps:
                f(*args, **kwargs)

            msg = "Executing '%s'" % func.__name__
            print("=" * len(msg))
            print(msg)
            print("=" * len(msg))

            res = func(*args, **kwargs)

            print()

        new_func.proma_command = True

        return new_func

    return require2
