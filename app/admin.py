from django.contrib import admin

from .models import Person
from .models import Poll
from .models import Question
from .models import Choice

admin.site.register(Person)
admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Choice)
