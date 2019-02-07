import re

from django.utils.translation import ugettext as _

def enum2choices(enum):
    pattern = re.compile("^[A-Z][A-Z_]+$")
    return tuple(
        (getattr(enum, key), key)
        for key in dir(enum)
        if re.match(pattern, key)
    )
    
def check_wechat_permission(request, permission, appid):
    """
    :type request: django.http.request.HttpRequest
    """
    from .models import WeChatApp
    app = WeChatApp.get_by_id(appid)
    if not app:
        return False
    return request.user.has_perm("wechat.{appname}_{permission}".format(
        appname=app.name,
        permission=permission
    ))

def get_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip