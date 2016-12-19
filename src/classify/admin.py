from django.contrib import admin

# Register your models here.
from .models import classify

class classifyAdmin(admin.ModelAdmin):
    class Meta:
        model = classify

admin.site.register(classify, classifyAdmin)
