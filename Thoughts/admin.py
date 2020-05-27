from django.contrib import admin
from .models import thots, Relates, Profile, Likes
# Register your models here.


class RelateInLine(admin.TabularInline):
    model = Relates
    extra = 1


class LikesInLine(admin.TabularInline):
    model = Likes
    extra = 1


class ThotAdmin(admin.ModelAdmin):
    inlines = [RelateInLine, LikesInLine]
    list_display = ('uname', 'head', 'thought_on')
    search_fields = ['uname']
    #inlines = [LikesInLine]


admin.site.register(thots, ThotAdmin)
# admin.site.register(Relates)
admin.site.register(Profile)
