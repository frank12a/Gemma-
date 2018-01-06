import re
from django.template import  Library
from django.conf import  settings
register=Library()

@register.inclusion_tag("xxxx.html")
def menu_html(request):
    menu_list=request.session[settings.PRIMSSION_MEN_DIC]
    print("菜单",menu_list)
    current_url=request.path_info
    print(current_url)
    menu_dict={}
    for item in menu_list:
        if not item["menu_gp_id"]:
            menu_dict[item["id"]]=item
    for item in menu_list:
        regax="^{0}$".format(item["url"])
        if re.match(regax,current_url):
            menu_gp_id=item["menu_gp_id"]
            print(menu_gp_id)
            if menu_gp_id:
                menu_dict[menu_gp_id]["active"]=True
            else:
                menu_dict[item["id"]]["active"]=True
    print("字典",menu_dict)
    result={}
    for item in menu_dict.values():
        print(item)
        active=item.get("active")
        menu_id=item["menu_id"]
        if menu_id in result:
            result[menu_id]["children"].append({"title":item["title"],"url":item["url"],"active":active})
            if active:
                result[menu_id]["active"]=True
        else:
            result[menu_id]={
                "menu_id":item["menu_id"],
                "menu_title":item["menu_title"],
                "active":active,
                "children":[
                    {"title":item["title"],
                     "url":item["url"],
                     "active":active}
                ]
            }
    print("最终菜单",result)
    return  {"menu_dict":result}





