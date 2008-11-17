from django.contrib import admin
from pxcs2w2.card.models import Card, Answer, CardSolve

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2
    
class CardAdmin(admin.ModelAdmin):
    inlines = [AnswerInline,]
    list_display = ('key', 'name', 'colour',)
    list_display_links = list_display
    list_filter = ('colour',)
    save_on_top = True
    search_fields = ['name']
    
    fieldsets = (
            (None, {
                'fields': ('number', 'name', 'colour',)
            }),
            (None, {
                'fields': ('hint', 'question', 'notes', )
            }),
            ('Advanced options', {
                'classes': ('collapse',),
                'fields': ('factory', 'data',)
            }),
        )

class CardSolveAdmin(admin.ModelAdmin):
	list_display = ('user', 'card', 'solved',)
	list_display_links = ('user', 'card',)
	list_filter = ('card', 'user',)
    
admin.site.register(Card, CardAdmin)
admin.site.register(CardSolve, CardSolveAdmin)

