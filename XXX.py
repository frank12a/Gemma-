class Foo(object):
    pass


class Bar(Foo):
    pass


class WW(Foo):
    pass


# obj = Bar()
# obj1 = WW()

# isinstance用于判断，对象是否是指定类的实例 （错误的）
# isinstance用于判断，对象是否是指定类或其派生类的实例
# print(isinstance(obj, Foo))
# print(isinstance(obj, Bar))
# print(isinstance(obj1, Foo))

# print(type(obj) == Bar)
# print(type(obj) == Foo)
class Foo(object):
    def __init__(self,name):
        self.name = name
        # self.name="haiyan"
    def func(self):
        print(self.name)

# obj = Foo('egon')
# # obj.func()
# # Foo.func(Foo('égon'))
# Foo.func(obj)


# for x in range(1000):
#     for y in range(1000):
#         for z in range(1000):
#             if x**2+y**2==z**2 and x+y+z==1000:
#                 print('%s,%s,%s'%(x,y,z))

# import time
# start_time=time.time()
# for i in range(0,1001):
#     for j in range(0,1001-i):
#             z=1000-i-j
#             if i+j+z ==1000 and i**2+j**2==z**2:
#                 print("i==%s,j==%s,z==%s"%(i,j,z))
# end_time=time.time()
# print("times:%s"%(end_time-start_time))
import copy
a=[1,2,[3,4,],'fuck']
b=a.copy()
# a.append(5)
print(b,id(b))
print(a,id(a))
# for i in a:
#     print(id(i))
# for i in b:
#     print(id(i))

