class ApplicationModuleProvider:
    def __init__(self, module):
        self.module = module

    def get_module(self):
        return self.module
