import inspect

def to_fstring(value):
    frame = inspect.currentframe().f_back
    local_vars = frame.f_locals
    global_vars = frame.f_globals

    if isinstance(value, str):
        return eval(f"f{repr(value)}", global_vars, local_vars)
    else:
        return str(value)

if __name__ == "__main__":
    user_input = input("Enter your string:\n> ")
    result = to_fstring(user_input)
    print("Result:", result)
