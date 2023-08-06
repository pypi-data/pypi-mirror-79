
class default_backend:

    def __init__(self):
        self.array_type = list
    
    def len(self, arr):
        return len(arr)

    def validate_array(self, data):
        if type(data) is list:
            return data
        elif type(data) is tuple:
            return list(data)
        else:
            return None

    def sum(self, arr):
        return sum(arr)
    
    def mean(self, arr):
        return sum(arr) / float(len(arr))
        
    def square(self, arr, inplace=False):
        if inplace:
            for i in range(len(arr)):
                val = arr[i]
                arr[i] = val * val
            return arr
        else:
            return [elem * elem  for elem in arr]
    
    def subtract(self, arr, val, inplace=False, modify_right=False):
        if type(val) is list:
            i, j = len(arr), len(val)
            if i != j: return
            if inplace:
                if modify_right:
                    for x in range(i):
                        val[x] -= arr[x]
                    return val
                else:
                    for x in range(i):
                        arr[x] -= val[x]
                    return arr
            else:
                return [arr[x] - val[x]  for x in range(i) ]
        else:
            if inplace:
                for i in range(len(arr)):
                    arr[i] -= val
                return arr
            else:
                return [elem - val  for elem in arr]
    

    def multiply(self, arr, val, inplace=False, modify_right=False):
        if type(val) is list:
            i, j = len(arr), len(val)
            if i != j: return
            if inplace:
                if modify_right:
                    for x in range(i):
                        val[x] *= arr[x]
                    return val
                else:
                    for x in range(i):
                        arr[x] *= val[x]
                    return arr
            else:
                return [arr[x] * val[x]  for x in range(i) ]
        else:
            if inplace:
                for i in range(len(arr)):
                    arr[i] *= val
                return arr
            else:
                return [elem * val  for elem in arr]
    
    
    

