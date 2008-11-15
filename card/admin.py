from django.contrib import admin
from pxcs2w2.card.models import Card, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2
    
class CardAdmin(admin.ModelAdmin):
    inlines = [AnswerInline,]
    list_display = ('key', 'name',)
    list_display_links = list_display
    list_filter = ('colour',)
    save_on_top = True
    
admin.site.register(Card, CardAdmin)

