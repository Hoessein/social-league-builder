from django.contrib import admin

# Register your models here.

from .models import Project, Profile, ProjectPosition

from . import forms

#
# class project_position_inline(admin.TabularInline):
#     model = Project.positions.through

# class projectAdmin(admin.ModelAdmin):
#     inlines = (project_position_inline,)
#
#
# class positionAdmin(admin.ModelAdmin):
#     inlines = (project_position_inline,)


# admin.site.register(Position, positionAdmin)
# admin.site.register(Project, projectAdmin)
# admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(ProjectPosition)


