
class error_handler:

    def __init__(self, own_function):
        self.func = own_function

    def __call__(self, *args, **kwargs):
        try:
            self.func(*args, **kwargs)
        except Exception as e:
            print(e)