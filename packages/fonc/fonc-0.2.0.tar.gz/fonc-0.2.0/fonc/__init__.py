import re
import random
from typing import Callable, Tuple


def _replace_fn_name(fn_str: str) -> Tuple[str, str]:
    """
    Return function text and name of that function
    """
    new_name = "F" + "".join([random.choice("ABCDEF1234567890") for _ in range(64)])
    fn_str = re.sub(r"def (.+)\(", f"def {new_name}(", fn_str)
    return fn_str, new_name


def fonc(function_definition: str) -> Callable:
    """
    """
    _callable = None
    if isinstance(function_definition, str):
        if function_definition.strip().startswith("def"):
            # This is a function definition in conventional syntax.
            fn, name = _replace_fn_name(function_definition)
            exec(fn, globals())
            _callable = lambda args: eval(f"{name}")(args)
    return _callable
