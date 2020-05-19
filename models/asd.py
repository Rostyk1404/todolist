class A:
    a = 1

    def __init__(self):
        self.b = 2
        
    def mult(self):
        return None

A.mult()
obj = A()
print(obj.b)
print(obj.a)
print(obj.mult())
print(A.a)

