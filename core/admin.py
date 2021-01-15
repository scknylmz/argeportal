from django.contrib import admin
from .models import Personel,DepartmentList,News,Projects,IsPaketiekle, AdamAy, ArgeTesvik

class PersonelAdmin(admin.ModelAdmin):
    list_display = ("name", "surName")

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)

class NewsAdmin(admin.ModelAdmin):
    list_display = ("title",)

class ProjectsAdmin(admin.ModelAdmin):
    filter_verticaly = ('projeAdamlar',)

class IsPaketiekleAdmin(admin.ModelAdmin):
    list_display = ("projeKodu","isPaketino", "isPaketiadi")

class AdamAyAdmin(admin.ModelAdmin):
    list_display = ("projeKodu", "tarih")

class ArgeTesvikAdmin(admin.ModelAdmin):
    list_display = ("date",)

admin.site.register(Personel, PersonelAdmin)
admin.site.register(DepartmentList, DepartmentAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Projects, ProjectsAdmin)
admin.site.register(IsPaketiekle, IsPaketiekleAdmin)
admin.site.register(AdamAy, AdamAyAdmin)
admin.site.register(ArgeTesvik, ArgeTesvikAdmin)

# Register your models here.
