
class numpy_backend:

    def __init__(self):
        import numpy as np
        self.np = np
        self.array_type = np.array
    
    def len(self, arr):
        return len(arr)
    
    def validate_array(self, data):
        np = self.np
        if type(data) is np.ndarray:
            return np.array(data)
        elif type(data) is list:
            return np.array(data)
        elif type(data) is tuple:
            return data
        else:
            return None
    
    def sum(self, arr):
        return self.np.sum(arr)

    def mean(self, arr):
        return self.np.mean(arr)
        
    def square(self, arr, inplace=False):
        if inplace:
            self.np.square(arr, arr)
            return arr
        else:
            return self.np.square(arr)
    
    def subtract(self, arr, val, inplace=False, modify_right=False):
        np = self.np
        if type(val) is np.ndarray:
            if inplace:
                if modify_right:
                    val -= arr
                    return val
                else:
                    arr -= val
                    return arr
            else:
                return arr - val
        else:
            if inplace:
                arr -= val
                return arr
            else:
                return arr - val
    
    def multiply(self, arr, val, inplace=False, modify_right=False):
        np = self.np
        if type(val) is np.ndarray:
            if inplace:
                if modify_right:
                    val *= arr
                    return val
                else:
                    arr *= val
                    return arr
            else:
                return arr * val
        else:
            if inplace:
                arr *= val
                return arr
            else:
                return arr * val

    