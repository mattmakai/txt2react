from django.contrib import admin

from .models import ReactionEvent, Reaction

class ReactionInline(admin.TabularInline):
    model = Reaction

class ReactionEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer', 'event_date')
    fieldsets = (
        ('ReactionEvent', {'fields': (
            'name', 'customer', 'url', 'event_date', 'phone_number',
        )}),
    )
    inlines = (ReactionInline,)

admin.site.register(ReactionEvent, ReactionEventAdmin)
admin.site.register(Reaction)
