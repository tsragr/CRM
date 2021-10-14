from django.contrib import admin
from crm import models

admin.site.register(models.Company)
admin.site.register(models.Worker)
admin.site.register(models.Office)
admin.site.register(models.Cooperation)
admin.site.register(models.Profile)
admin.site.register(models.UserSkill)
admin.site.register(models.UserLanguage)


