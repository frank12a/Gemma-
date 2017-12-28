from crm import models


class XXX(object):
    users = None # [1,2,1,2,3,1,...]
    iter_users = None # iter([1,2,1,2,3,1,...])
    reset_status = False
    roll_back_list=[]

    @classmethod
    def fetch_users(cls):
        # [obj(销售顾问id,num),obj(销售顾问id,num),obj(销售顾问id,num),obj(销售顾问id,num),]
        sales = models.SaleRank.objects.all().order_by('-weight')
        # print('销售顾问',sales)
        #方法二
        v=[]
        count=0
        while True:
            flag=False
            for row in sales:
                if row.num >count:
                    v.append(row.id)
                    flag=True
            count=count+1
            if not flag:
                break


        # #方法一
        # num_obj = models.SaleRank.objects.all().order_by('-num').first()
        # v = []
        # for i in range(num_obj.num):
        #     for obj in sales:
        #         if obj.num > i:
        #             v.append(obj.id)
        #
        # print('v', v)

# v = [短期, 番禺, 富贵, 秦晓, 短期, 番禺, 富贵, 秦晓, 番禺, 富贵, 秦晓, 秦晓, 秦晓, 秦晓, 秦晓, 秦晓, 秦晓...]
#         v = [3, 1, 2, 6, 3, 1, 2, 6, 3, 1, 2, 6, 3, 1, 2, 6, 3, 1, 2, 6, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 3, 3, 3, 3]
        cls.users = v

    @classmethod
    def get_sale_id(cls):
        if cls.roll_back_list:
            return cls.roll_back_list.pop()
        if not cls.users:
            cls.fetch_users()
        if not cls.iter_users:
            cls.iter_users = iter(cls.users)
        try:
            user_id = next(cls.iter_users)
        except StopIteration as e:
            if cls.reset_status:
                cls.fetch_users()
                cls.reset_status = False
            cls.iter_users = iter(cls.users)
            user_id = cls.get_sale_id()
        return user_id

    @classmethod
    def reset(cls):
        cls.reset_status = True

    @classmethod
    def rollback(cls,nid):
        cls.roll_back_list.insert(0,nid)
