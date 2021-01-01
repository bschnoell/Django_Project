from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Testkunde)
admin.site.register(Testangebot)


admin.site.register(Test_Bauweise)
admin.site.register(Test_Baustoff)
admin.site.register(Test_Raum)
admin.site.register(Test_Angebot)
admin.site.register(Test_Heizkoerper)
admin.site.register(Test_Kunde)
admin.site.register(Test_Objekt)
admin.site.register(Test_Steuerung)
admin.site.register(t_config)
admin.site.register(t_lambda)