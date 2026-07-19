from ..models import *
from django import template
from django.contrib.sessions.models import Session

register = template.Library()

# 判断头像是否为选择的头像
@register.filter
def Compare_Picture(pid, pic):
    avatar1 = pic
    avatar2 = 'users/avatar/{}.png'.format(pid)

    if avatar1 == avatar2:
        return True
    else:
        return False


# 获取所有活跃用户
@register.simple_tag
def Get_All_Users():
    return UserProfile.objects.filter(status=1).filter(is_active=True)


# 获取在线用户
@register.simple_tag
def Get_Friends_List(num=10):
    try:
        all_session = Session.objects.all()
        user_list = []
        for session in all_session:
            try:
                decoded = session.get_decoded()
                uid = decoded.get('_auth_user_id')
                if uid:
                    user_list.append(uid)
            except Exception:
                # 忽略错误的会话
                continue

        if user_list:
            return UserProfile.objects.filter(id__in=user_list)[:num]
        else:
            # 如果没有找到用户，返回空列表而不是QuerySet
            return []
    except Exception:
        # 发生任何错误，返回空列表
        return []


# 获取用户数量
@register.simple_tag
def Get_Users_Nums():
    return UserProfile.objects.filter(status=1).filter(is_active=True).count()


# 最近一年
@register.simple_tag
def Get_Latest_Year_List():
    ym_list = []
    y_now = datetime.datetime.now().year
    m_now = datetime.datetime.now().month
    i = 0
    while (i < 12):
        ym_list.append(str(y_now) + '-' + str(m_now))
        m_now = m_now - 1
        if m_now == 0:
            m_now = 12
            y_now = y_now - 1

        i+=1

    return list(reversed(ym_list))




















