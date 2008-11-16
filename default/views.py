from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login

def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            return HttpResponseRedirect(reverse('site_root'))
    else:
        form = UserCreationForm()
        form.fields['username'].help_text = ''

    return render_to_response("register.html", {'form' : form}, context_instance=RequestContext(request))

