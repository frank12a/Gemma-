# from crm import models
#
#
# class XXX(object):
#     users = None # [1,2,1,2,3,1,...]
#     iter_users = None # iter([1,2,1,2,3,1,...])
#     reset_status = False
#     roll_back_list=[]
#
#     @classmethod
#     def fetch_users(cls):
#         # [obj(销售顾问id,num),obj(销售顾问id,num),obj(销售顾问id,num),obj(销售顾问id,num),]
#         sales = models.SaleRank.objects.all().order_by('-weight')
#         # print('销售顾问',sales)
#         #方法二
#         v=[]
#         count=0
#         while True:
#             flag=False
#             for row in sales:
#                 if row.num >count:
#                     v.append(row.id)
#                     flag=True
#             count=count+1
#             if not flag:
#                 break
#
#
#         # #方法一
#         # num_obj = models.SaleRank.objects.all().order_by('-num').first()
#         # v = []
#         # for i in range(num_obj.num):
#         #     for obj in sales:
#         #         if obj.num > i:
#         #             v.append(obj.id)
#         #
#         # print('v', v)
#
#
#         cls.users = v
#
#     @classmethod
#     def get_sale_id(cls):
#         if cls.roll_back_list:
#             return cls.roll_back_list.pop()
#         if not cls.users:
#             cls.fetch_users()
#         if not cls.iter_users:
#             cls.iter_users = iter(cls.users)
#         try:
#             user_id = next(cls.iter_users)
#         except StopIteration as e:
#             if cls.reset_status:
#                 cls.fetch_users()
#                 cls.reset_status = False
#             cls.iter_users = iter(cls.users)
#             user_id = cls.get_sale_id()
#         return user_id
#
#     @classmethod
#     def reset(cls):
#         cls.reset_status = True
#
#     @classmethod
#     def rollback(cls,nid):
#         cls.roll_back_list.insert(0,nid)
import redis
from crm import models

POOL = redis.ConnectionPool(host='192.168.20.100', port=6379, password='')
CONN = redis.Redis(connection_pool=POOL)


class XXX(object):
    @classmethod
    def fetch_users(cls):
        sales = models.SaleRank.objects.all().order_by('-weight')
        sale_id_list = []
        count = 0
        while True:
            flag = False
            for row in sales:  # 循环取到的对象
                if count < row.num:  # 如果数字小于这个对象的最大承受数量
                    sale_id_list.append(row.user_id)  # 就把这个对象的id放在列表里面
                    flag = True
            count += 1  # 数字循环加一
            if not flag:  # 判断是否还有数字加入如果没有就跳出循环
                break
        if sale_id_list:  # 判断里列表里有没有id，如果有那就放在redis里面
            CONN.rpush('sale_id_list', *sale_id_list)
            CONN.rpush('sale_id_list_origin', *sale_id_list)
            return True
        return False

    @classmethod
    def get_sale_id(cls):

        sale_id_origin_count = CONN.llen('sale_id_list_origin')
        if not sale_id_origin_count:
            status = cls.fetch_users()
        if not status:
            return None

        user_id = CONN.lpop('sale_id_list')
        if user_id:
            return user_id
        reset = CONN.get('sale_id_reset')
        if reset:
            CONN.delete('sale_id_list_origin')
            status=cls.fetch_users()
            if  not status:
                return  None
            CONN.delete('sale_id_reset')
        else:
            ct = CONN.llen('sale_id_list_origin')
            for i in range(ct):
                item = CONN.lindex('sale_id_list_origin', i)
                CONN.rpush('sale_id_list', item)
        # cls.get_sale_id()
    @classmethod
    def reset(cls):
        CONN.set('sale_id_reset',1)
    @classmethod
    def rollback(cls,nid):
        CONN.lpush('sale_id_list',nid)
