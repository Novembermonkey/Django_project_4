from datetime import timedelta

from django.contrib import admin

from courses.forms import VideoForm
from courses.models import Course, Video, Subject, Lesson, Image, File, Module, Text, Comment
from import_export.admin import ImportExportModelAdmin
# Register your models here.

models = [ Image, File, Module, Text, Comment]

admin.site.register(models)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    form = VideoForm
    list_display = ['id', 'title']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id',  'get_title']

    def get_title(self, obj):
        title = obj.item.title
        return title

@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']