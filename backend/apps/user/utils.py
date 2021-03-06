# coding=utf-8
from user.models import *
from django.db.models import Q
from utils.get_config import get_conf

def generate_menu(has_id,type):
    menus = []
    perms = []
    router = []
    user_menus = Menu.objects.filter(Q(id__in=has_id)&Q(del_flag=0))
    user_perms = Perms.objects.filter(Q(id__in=has_id)&Q(del_flag=0)&~Q(perms=''))
    menu_dir = []
    for item in user_menus:
        if (item.mtype == 0):
            menu_dir.append({'id':item.id,'name':item.name,'mtype':item.mtype,'icon':item.icon,'path':item.url,'children':[]})
    for item in menu_dir:
        menu_node = user_menus.filter(Q(parent_id=item['id'])&Q(mtype__in=[1,2])&Q(del_flag=0))
        for node in menu_node:
            item['children'].append({'id':node.id,'name':node.name,'mtype':node.mtype,'icon':node.icon,'path':node.url,})
    # user_perms = user_perms.filter(Q(mtype=2)&Q(del_flag=0))
    user_router = user_menus.filter(~Q(url='')&Q(del_flag=0))
    menus = menu_dir
    for item in user_perms:
        perms.append(item.perms)
    for item in user_router:
        router.append(item.url)
    if (type == 'menu'):
        return menus
    elif (type == 'perms'):
        return perms
    elif (type == 'router'):
        return router

# 白名单url
white_url_list = ['/dashboard']

def init_permissions(user,type):
    menus_id = []
    perms_id = []
    white_menus = Menu.objects.filter(Q(url__in=white_url_list)&Q(del_flag=0)).values('id').distinct()
    for i in white_menus:
        menus_id.append(i['id'])
    if (user.is_superuser):
        all_menus_id = Menu.objects.filter(Q(del_flag=0)).values('id').distinct()
        all_perms_id = Perms.objects.filter(Q(del_flag=0),~Q(perms='')).values('id').distinct()
        for i in all_menus_id:
            menus_id.append(i['id'])
        for i in all_perms_id:
            perms_id.append(i['id'])
    else:
        if (hasattr(user,'roles')):
            for role in user.roles.all():
                role.menu.all()
                for i in role.menu.all():
                    menus_id.append(i.id)
                for i in role.perms.all():
                    perms_id.append(i.id)
                menus_id = list(set(menus_id))
                perms_id = list(set(perms_id))
        else:
            menus_id = list(set(menus_id))
            perms_id = list(set(perms_id))
    if (type == 'menu'):
        return generate_menu(menus_id,'menu')
    elif (type == 'perms'):
        return generate_menu(perms_id,'perms')
    elif (type == 'router'):
        return generate_menu(menus_id,'router')

# 获取部署环境
def get_env():

    env = get_conf('deployment','environment')
    return env

def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'username': user.username,
        'is_superuser': user.is_superuser,
        'menu': init_permissions(user,'menu'),
        'perms': init_permissions(user,'perms'),
        'router': init_permissions(user,'router'),
        'environment': get_env(),
    }