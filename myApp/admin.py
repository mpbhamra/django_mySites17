from django.contrib import admin
from .models import Author,Book,Student,Course,Topics
# Register your models here.
admin.site.register(Author)


admin.site.register(Course)
admin.site.register(Topics)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','numpages','in_stock',)
admin.site.register(Book, BookAdmin)

class StudentAdmin(admin.ModelAdmin):

    list_display = ('first_name','last_name')

admin.site.register(Student,StudentAdmin)
