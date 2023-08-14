from django.contrib import admin
from.models import Game, Platforms, Duels

# Register your models here.

class GameAdmin(admin.ModelAdmin):
    readonly_fields = ("id", )

class PlatformsAdmin(admin.ModelAdmin):
    readonly_fields = ("id", )

class DuelsAdmin(admin.ModelAdmin):
    readonly_fields = ("id", )




admin.site.register(Game, GameAdmin)
admin.site.register(Platforms, PlatformsAdmin)
admin.site.register(Duels,DuelsAdmin)