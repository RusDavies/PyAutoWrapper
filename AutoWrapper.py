from types import FunctionType
from functools import wraps

class AutoWrapper():
    @staticmethod
    def getMethods2Wrap(class_type, hints=None):
        if (hints == None):
            # In this case, where we have no hints, then we wrap all functions
            results = [ (name,att) for (name,att) in class_type.__dict__.items() if isinstance(att, FunctionType)]
        else: 
            # In this case, where a hint dictionary has beengiven to us, then we use it. 
            results = [ (name,att) for (name,att) in class_type.__dict__.items() if hints.get(name, {}).get('proxy', False)]
        return results 

    def build_wrapper(self, class_to_wrap, hints=None):
        class_type = type(class_to_wrap)
        for (attributeName, attribute) in __class__.getMethods2Wrap(class_type, hints):
            if ((isinstance(attribute, FunctionType) == True) & (hints.get(attributeName, {}).get('wrap', False) == True)):
                attribute = self._wrapper(attribute)
            self.__dict__[attributeName] = attribute

    def _wrapper(self, method):
        @wraps(method)
        def wrapped(*args, **kwargs):
            self._pre_method_hook(method, *args, **kwargs)
            result = method(self, *args, *kwargs)
            self._post_method_hook(method, *args, **kwargs)
            return result
        return wrapped

    def _pre_method_hook(self, method, *args, **kwargs):
        pass

    def _post_method_hook(self, method, *args, **kwargs):
        pass


if __name__ == '__main__':
    # Example usage
    class Example:
        def methodA(self):
            print("Method A called")

        def methodB(self):
            print("Method B called")

    class WExample(AutoWrapper):
        def __init__(self):
            self.example = Example()
            hints = { 'methodA': {'proxy': True, 'wrap': True}, 
                      'methodB': {'proxy': True, 'wrap': False} }
            self.build_wrapper( self.example, hints=hints )

        def _pre_method_hook(self, method, *args, **kwargs):
            print("_pre_method_hook() called for {!r}".format(method.__name__))

        def _post_method_hook(self, method, *args, **kwargs):
            print("_post_method_hook() called for {!r}".format(method.__name__))

            
    test = WExample()
    test.methodA()

    # Results:
    # _pre_method_hook() called for 'methodA'
    # Method A called
    # _post_method_hook() called for 'methodA'