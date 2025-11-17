from django.contrib import admin
from Switch.models import ProductionSwitch
from WebsiteTemplate.admin import admin_site
from WebsiteTemplate.settings import TOTP_ADMIN

# Register your models here.

class ProductionSwitchAdmin(admin.ModelAdmin):
    list_display = ['production_switch']

    def has_add_permission(self, request):
        # if there's already an entry, do not allow adding
        count = ProductionSwitch.objects.all().count()
        if count == 0:
            return True

        return False
    
    def has_delete_permission(self, request, obj=None):
        # if there's already an entry, do not allow adding
        count = ProductionSwitch.objects.all().count()
        if count == 0:
            return True

        return False
    

if TOTP_ADMIN:
    admin_site.register(ProductionSwitch, ProductionSwitchAdmin)
else:
    admin.site.register(ProductionSwitch, ProductionSwitchAdmin)