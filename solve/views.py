from django.shortcuts import get_object_or_404, render_to_response
from pxcs2w2.card.models import Card
from pxcs2w2.card.forms import build_answer_form

def view_card(request, card_id):
    card = get_object_or_404(Card, number=int(card_id))
    return render_to_response('card/view.html', {'card': card, 'answers': build_answer_form(card)})
    
def solve_card(request, card_id):
    pass
