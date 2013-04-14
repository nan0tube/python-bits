import functools
import inspect

def pre_hook_once(original):
    """
    Decorator to insert a pre-hook in original function with target function.
    The hook is removed after first execution.

    Arguments can be passed to original function by returning a tuple
    (args, kwargs). Returning None will not modify any argument.
    """
    def decorator(target):
        @functools.wraps(target)
        def wrapper(*args, **kwargs):
            if target.func_name not in target.func_globals:
                raise NameError('Function not in global scope')
            target.func_globals[target.func_name] = original
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

    Return value of original function is passed to target function as
    target_retval (keyword argument). Return value is not passed if target
    function has no argument.
    """
    def decorator(target):
        @functools.wraps(target)
        def wrapper(*args, **kwargs):
            if target.func_name not in target.func_globals:
                raise NameError('Function not in global scope')
            target.func_globals[target.func_name] = original
            kwargs['target_retval'] = original(*args, **kwargs)
            args, varargs, keywords, defaults = inspect.getargspec(target)
            if args or varargs or keywords:
                return target(*args, **kwargs)
            return target()
        return wrapper
    return decorator

if __name__ == '__main__':
    def pprint(a):
        print '[>>]', a
        return 1

    @pre_hook_once(pprint)
    def pprint(*args, **kwargs):
        return ([args[0].swapcase()], kwargs)

    print pprint('world')
    print pprint('world')

    @post_hook_once(pprint)
    def pprint(*args, **kwargs):
        return kwargs['target_retval'] ^ 1

    print pprint('world')
    print pprint('world')
