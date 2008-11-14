from django.shortcuts import get_object_or_404, render_to_response
from pxcs2w2.card.models import Card

def index(request, card_id):
    card = get_object_or_404(Card, number=int(card_id))
    return render_to_response('card/index.html', {'card': card, 'answers': card.answer_set.order_by('key')})
