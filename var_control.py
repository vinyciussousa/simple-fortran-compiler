class var_control:
    def __init__(self):
        self._variables = {}

    def set_variable(self, name, value, var_type):
        self._variables[name] = {'value': value, 'type': var_type}

    def get_variable(self, name):
        if name not in self._variables:
            raise ValueError(f'Undenfined: {name}')
        return self._variables.get(name, {}).get('value')

    def get_variable_type(self, name):
        if name not in self._variables:
            raise ValueError(f'Undenfined: {name}')
        return self._variables.get(name, {}).get('type')

    def delete_variable(self, name):
        if name in self._variables:
            del self._variables[name]
            return True     
        return False

    def list_variables(self):
        return [(name, var['value'], var['type']) for name, var in self._variables.items()]
    
    def is_variable_declared(self, name):
        return name in self._variables