import redis
conn=redis.Redis(host='192.168.11.24',port=6379,password='')
conn.set('frank','你好呀，我很好')
val=conn.get('frank').decode('utf-8')#取出的是字节需要转换下
print(val)
# conn.delete('names_list')
# conn.lpush('names_list',*['把几个','鲁宁']) #插入数据从左边插
# for i in range(2):
#   c=conn.lindex('names_list',i)
#   print(c.decode('utf-8'))
# a=conn.llen('names_list')
# print(a)
# conn.lpush('names_list','frank')
# v = conn.llen('names_list')#打印这个代码的长度
# conn.delete('names_list')
# for i in range(3):
#     v=conn.lindex('names_list',i)
#     print(v.decode('utf-8'))

import redis

"""
{
    "k1":"v1",
    'names': ['把几个','鲁宁','把几个','鲁宁','把几个','把几个','把几个','把几个',]
}

"""

# conn = redis.Redis(host='47.93.4.198',port=6379,password='123123')
# conn = redis.Redis(host='ip地址',port=6379,password='密码')
# conn.set('k1','v1') # 向远程redis中写入了一个键值对
# val = conn.get('k1') # 获取键值对
# print(val)
# conn.lpush('names_list',*['把几个','鲁宁']) #插入数据从左边插
# v = conn.llen('names_list')#打印这个代码的长度
#
# for i in range(v):#这是循环
#     val = conn.rpop('names_list')#从右边删除数据
#     val = conn.lpop('names_list')#从左边删除数据
#     print(val.decode('utf-8'))#打印数据，出来是字节要转换下
# v = conn.llen('namessssss_list')#打印长度
# print(v)

# ['把几个','鲁宁','把几个','鲁宁','把几个','把几个','把几个','把几个',]

# conn.lpush('sale_id_list',*[1,2,3,1,2,1,1,1])#如果是列表就用*存入数据

# 自动分配时，获取销售ID
# sale_id = conn.rpop('sale_id_list')

# 获取之后，未使用。再重新加入到原来的列表中
# conn.rpush('sale_id_list',3)

# conn.delete('sale_id_list_origin')#整个键值对
# conn.rpush('sale_id_list_origin',*[1,2,3,1,2,1,1,1])#这是右边放入

# ct = conn.llen('sale_id_list_origin')#获取长度
# for i in range(ct):
#     v = conn.lindex('sale_id_list_origin',i)#这是通过索引获取值
#     conn.rpush('sale_id_list',v)#把取到的值从右边放入
#
# v = conn.lpop('sale_id_list')#pop出来是有返回值
# print(v)
#
# conn.delete('sale_id_list_origin')#删除这个键值对
# conn.delete('sale_id_list')#删除这个键值对

# 第一次运行，只有数据库有数据

# 如果数据库中没有取到数据，那么直接返回None
# 否则
# conn.rpush('sale_id_list',*[1,2,3,1,2,1,1,1])#放入数据
# conn.rpush('sale_id_list_origin',*[1,2,3,1,2,1,1,1])#放入数据

# 接下来个一个获取,如果取到None，表示已经取完
# sale_id = conn.lpop('sale_id_list')#
# if not sale_id:#如果是空的
#     # 先判断，是否需要重置
#     if reset:#先判断是否需要重启如果需要就把所有的都删除
#         conn.delete('sale_id_list_origin')
#         conn.delete('sale_id_list')
#         # 重新从数据库获取，并给两个进行复制
# 这部操作没有写
#         reset = False#接着要把reset重新设置为False
#     else:
#         ct = conn.llen('sale_id_list_origin')#这个表的长度
#         for i in range(ct):#循环赋值
#             v = conn.lindex('sale_id_list_origin', i)#这是按照索引取值的
#             conn.rpush('sale_id_list', v)#这是把取到的值放到里面
#     sale_id = conn.lpop('sale_id_list')#从里面取值
#
# print(sale_id)

#
# v = conn.get('xxfasdf9dfsd')
# print(v)






import redis

"""
{
    "k1":"v1",
    'names': ['把几个','鲁宁','把几个','鲁宁','把几个','把几个','把几个','把几个',]
}

"""

# conn = redis.Redis(host='47.93.4.198',port=6379,password='123123')
# conn = redis.Redis(host='ip地址',port=6379,password='密码')
# conn.set('k1','v1') # 向远程redis中写入了一个键值对
# val = conn.get('k1') # 获取键值对
# print(val)
# conn.lpush('names_list',*['把几个','鲁宁']) #插入数据从左边插
# v = conn.llen('names_list')#打印这个代码的长度
#
# for i in range(v):#这是循环
#     val = conn.rpop('names_list')#从右边删除数据
#     val = conn.lpop('names_list')#从左边删除数据
#     print(val.decode('utf-8'))#打印数据，出来是字节要转换下
# v = conn.llen('namessssss_list')#打印长度
# print(v)

# ['把几个','鲁宁','把几个','鲁宁','把几个','把几个','把几个','把几个',]

# conn.lpush('sale_id_list',*[1,2,3,1,2,1,1,1])#如果是列表就用*存入数据

# 自动分配时，获取销售ID
# sale_id = conn.rpop('sale_id_list')

# 获取之后，未使用。再重新加入到原来的列表中
# conn.rpush('sale_id_list',3)

# conn.delete('sale_id_list_origin')#整个键值对
# conn.rpush('sale_id_list_origin',*[1,2,3,1,2,1,1,1])#这是右边放入

# ct = conn.llen('sale_id_list_origin')#获取长度
# for i in range(ct):
#     v = conn.lindex('sale_id_list_origin',i)#这是通过索引获取值
#     conn.rpush('sale_id_list',v)#把取到的值从右边放入
#
# v = conn.lpop('sale_id_list')#pop出来是有返回值
# print(v)
#
# conn.delete('sale_id_list_origin')#删除这个键值对
# conn.delete('sale_id_list')#删除这个键值对

# 第一次运行，只有数据库有数据

# 如果数据库中没有取到数据，那么直接返回None
# 否则
# conn.rpush('sale_id_list',*[1,2,3,1,2,1,1,1])#放入数据
# conn.rpush('sale_id_list_origin',*[1,2,3,1,2,1,1,1])#放入数据

# 接下来个一个获取,如果取到None，表示已经取完
# sale_id = conn.lpop('sale_id_list')#
# if not sale_id:#如果是空的
#     # 先判断，是否需要重置
#     if reset:#先判断是否需要重启如果需要就把所有的都删除
#         conn.delete('sale_id_list_origin')
#         conn.delete('sale_id_list')
#         # 重新从数据库获取，并给两个进行复制
# 这部操作没有写
#         reset = False#接着要把reset重新设置为False
#     else:
#         ct = conn.llen('sale_id_list_origin')#这个表的长度
#         for i in range(ct):#循环赋值
#             v = conn.lindex('sale_id_list_origin', i)#这是按照索引取值的
#             conn.rpush('sale_id_list', v)#这是把取到的值放到里面
#     sale_id = conn.lpop('sale_id_list')#从里面取值
#
# print(sale_id)


# v = conn.get('xxfasdf9dfsd')
# print(v)
# import importlib.util
#
#
# def import_source(module_name):
#     module_file_path = module_name.__file__
#     print('module_file_pat',module_file_path)
#     module_name = module_name.__name__
#     print('mdule_name',module_name)
#
#     module_spec = importlib.util.spec_from_file_location(
#         module_name, module_file_path
#     )
#     print('module_spec',module_spec)
#     module = importlib.util.module_from_spec(module_spec)
#     print('module',module)
#     module_spec.loader.exec_module(module)
#     print(dir((module)))
#
#     msg = 'The {module_name} module has the following methods {methods}'
#     print(msg.format(module_name=module_name, methods=dir(module)))
#
#
# if __name__ == "__main__":
#     import logging
#
# #     import_source(logging)
# import json#导入json
# from   django.db.models import  Q #导入Q查询
# from django.db import transaction  #事务
# from django.conf.urls import url      #导入url
# from django.forms import  ModelForm   #导入modelform
# # from django.forms import  Form      #导入from
# # from django.shortcuts import  HttpResponse,redirect,render,reverse#导入基本
# # from django.utils.safestring import mark_safe  #导入mark_safe()
# # import  datetime   #导入时间
#
#
#
#
#
#
#
# import json  #导入json
# from django.db.models import Q  #导入Q查询
# from django.shortcuts import HttpResponse,render,redirect
# from  django.utils.safestring import mark_safe
# from django.conf.urls import url
# from django.forms  import  ModelForm
# from django.forms import forms
# from django.db import  transaction







