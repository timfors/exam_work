from django.contrib import admin

from .models import Sith, Question, Recruit, Answer, Planet
# Register your models here.
admin.site.register(Planet)
admin.site.register(Sith)
admin.site.register(Question)
admin.site.register(Recruit)
admin.site.register(Answer)
