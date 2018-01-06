from rbac import  models
from django.conf import  settings
def inin_permission(request,user):
    permission_list=models.Userinfo.objects.filter(name=user).values(
                                                "role_userinfo__name",#角色的名字
                                                "role_userinfo__role_perimission__id",#权限的id
                                                 "role_userinfo__role_perimission__title",#权限的名字
                                                 "role_userinfo__role_perimission__url",#权限的url
                                                "role_userinfo__role_perimission__code",#权限分组的依据
                                                 "role_userinfo__role_perimission__menu_id",#是不是菜单
                                                  "role_userinfo__role_perimission__group_perimission__name",#组的名字
                                                   "role_userinfo__role_perimission__group_perimission__id" ,#组的id
                                                    "role_userinfo__role_perimission__group_perimission__group_menu__id",#菜单的id
                                                   "role_userinfo__role_perimission__group_perimission__group_menu__title",#菜单的名字
    ).distinct()
    print("原始数据",permission_list)
    #菜单数据的保留
    menu_list=[]
    for item in permission_list:
        tpl={
            "id":item["role_userinfo__role_perimission__id"] ,#权限id
            "title":item["role_userinfo__role_perimission__title"],#权限的名字
            "url":item["role_userinfo__role_perimission__url"],#权限的url
            "menu_gp_id":item["role_userinfo__role_perimission__menu_id"],#是不是菜单
            "menu_id":item["role_userinfo__role_perimission__group_perimission__group_menu__id"],#菜单的id
            "menu_title":item["role_userinfo__role_perimission__group_perimission__group_menu__title"]#菜单的title

        }
        menu_list.append(tpl)
    request.session[settings.PRIMSSION_MEN_DIC]=menu_list
    print("最开始的菜单",menu_list)



    #保留权限的代码
    result={}
    for item in permission_list:
        group_id=item["role_userinfo__role_perimission__group_perimission__id"]
        code=item["role_userinfo__role_perimission__code"]
        url=item["role_userinfo__role_perimission__url"]
        if group_id in result:
            result[group_id]["codes"].append(code)
            result[group_id]["urls"].append(url)
        else:
            result[group_id]={
                "codes":[code,],
                "urls":[url,]
            }

    request.session[settings.PRIMANRY_LIST]=result
    print("8888888888****",result)


