from django.contrib import admin

# Register your models here
def get_model_fields(model):
    return [field.name for field in model._meta.get_fields()]