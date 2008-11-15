from django.contrib import admin
from pxcs2w2.card.models import Card, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    
class CardAdmin(admin.ModelAdmin):
    inlines = [AnswerInline,]
    
admin.site.register(Card, CardAdmin)

