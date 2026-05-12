from django.contrib import admin
from .models import Application
from .models import TrainingContent

admin.site.register(Application)
admin.site.register(TrainingContent)