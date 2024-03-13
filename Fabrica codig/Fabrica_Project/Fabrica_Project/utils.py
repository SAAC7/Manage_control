# En tu archivo utils.py
from django.contrib.auth.models import User

def user_groups_context(request):
    user_groups = []
    if request.user.is_authenticated:
        user_groups = request.user.groups.values_list("name", flat=True)
    return {'user_groups': user_groups}
