from django.contrib import admin
from .models import Book
from .models import Person
from .models import Add
from .models import BookVisited
from .models import BookLike

# Register your models here.
admin.site.register(Book)
admin.site.register(Person)
admin.site.register(Add)
admin.site.register(BookLike)
admin.site.register(BookVisited)