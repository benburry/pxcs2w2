import re
from django.shortcuts import get_object_or_404, render_to_response
from pxcs2w2.card.models import Card
from pxcs2w2.card.forms import build_answer_form

def view_card(request, card_id):
    card = get_object_or_404(Card, number=int(card_id))
    formtype = build_answer_form(card)
    
    params = {'card': card}
    
    if request.method == 'POST':
        form = formtype(request.POST)
        params['form'] = form
        
        if form.is_valid():
            correct = True
            for match in (re.match(f.data, f.field.correct, re.I) for f in form):
                correct = correct and match is not None
                if not correct:
                    break
        
            params['correct'] = correct
            if correct:
                del params['form']
                
    else:
        form = formtype()
        params['form'] = form
        
    return render_to_response('card/view.html', params)
    

    
    
