from functools import wraps

def pre_hook_once(original):
    """
    Decorator to insert a pre-hook in original function with target function.
    The hook is removed after first execution.

    Arguments can be passed to original function by returning the tuple
    (args, kwargs). Returning None will not modify any argument.
    """
    def decorator(target):
        @wraps(target)
        def wrapper(*args, **kwargs):
            target.func_globals[target.__name__] = original
            ret = target(*args, **kwargs)
            if ret:
                (args, kwargs) = ret
            return original(*args, **kwargs)
        return wrapper
    return decorator

def post_hook_once(original):
    """
    Decorator to insert a post-hook in original function with target function.
    The hook is removed after first execution.

    Return value is passed to target function as kwargs['target_retval'].
    """
    def decorator(target):
        @wraps(target)
        def wrapper(*args, **kwargs):
            target.func_globals[target.__name__] = original
            kwargs['target_retval'] = original(*args, **kwargs)
            return target(*args, **kwargs)
        return wrapper
    return decorator

if __name__ == '__main__':
    def pprint(a):
        print '[>>]', a
        return 1

    @pre_hook_once(pprint)
    def pprint(*args, **kwargs):
        return [args[0].swapcase()], kwargs

    print pprint('world')
    print pprint('world')

    @post_hook_once(pprint)
    def pprint(*args, **kwargs):
        return kwargs['target_retval'] ^ 1

    print pprint('world')
    print pprint('world')
