from django.contrib import admin

from themes.models import Theme, Favorite

admin.site.register(Theme)
admin.site.register(Favorite)