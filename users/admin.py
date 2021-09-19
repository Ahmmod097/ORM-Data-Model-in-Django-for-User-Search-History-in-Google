from django.contrib import admin
from .models import UserInfo, Keyword, SearchedDate

admin.site.register(UserInfo)
admin.site.register(Keyword)
admin.site.register(SearchedDate)
