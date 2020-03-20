from django.contrib import admin

from .models import Course, Details, Participants

'''
admin.site.register(Course)
admin.site.register(Details)
'''

admin.site.register(Participants)


class DetailsInline(admin.TabularInline):
    model = Details
    extra = 0


class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['course_name']}),
        ('Image',           {'fields': ['image']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [DetailsInline]


admin.site.register(Course, CourseAdmin)
