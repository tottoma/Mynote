from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import HeartLog, Note, Category, KeyLog
# Register your models here.

class HeartLogResource(resources.ModelResource):
    # Modelに対するdjango-import-exportの設定
    class Meta:
        model = HeartLog

@admin.register(HeartLog)
class HeartLogAdmin(ImportExportModelAdmin):
    pass
    list_display = ('pk', 'user_id', 'measured_at', 'bpm')
    ##list_filter = ['measured_at']
    search_fields = ['user_id']
    # django-import-exportsの設定
    resource_class = HeartLogResource

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'user', 'category', 'created_at', 'updated_at')
    ##search_fields = ['category']

admin.site.register(Category)

class KeyLogResource(resources.ModelResource):
    # Modelに対するdjango-import-exportの設定
    class Meta:
        model = KeyLog

@admin.register(KeyLog)
class KeyLogAdmin(ImportExportModelAdmin):
    list_display = ('note_id', 'counted_at', 'count')
    search_fields = ['note_id']
    # django-import-exportsの設定
    resource_class = KeyLogResource
