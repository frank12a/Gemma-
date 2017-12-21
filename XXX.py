class Foo(object):
    pass


class Bar(Foo):
    pass


class WW(Foo):
    pass


obj = Bar()
obj1 = WW()

# isinstance用于判断，对象是否是指定类的实例 （错误的）
# isinstance用于判断，对象是否是指定类或其派生类的实例
print(isinstance(obj, Foo))
print(isinstance(obj, Bar))
print(isinstance(obj1, Foo))

# print(type(obj) == Bar)
# print(type(obj) == Foo)
