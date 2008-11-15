from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=64)
    hint = models.CharField(max_length=256, null=True, blank=True)
    question = models.TextField()
    
    def __unicode__(self):
        return "#%s - %s" % (self.key, self.name)
        
    @models.permalink
    def get_absolute_url(self):
        return ('card_view', [self.key])
        
    @property
    def key(self):
        return "%03u" % self.number
        
    class Meta:
        ordering = ["number"]


class Answer(models.Model):
    card = models.ForeignKey(Card)
    key = models.CharField(max_length=1, unique=True)
    value = models.CharField(max_length=128)
    
    def __unicode__(self):
        return "%s:%s" % (self.key, self.value)
        
    class Meta:
        ordering = ["key"]
        order_with_respect_to = 'card'
        

class SolverProfile(models.Model):
    # This is the only required field
    user = models.ForeignKey(User, unique=True)
    
    solve_start = models.DateTimeField(auto_now_add=True)
    solve_count = models.PositiveSmallIntegerField(default=0)
    
    @property
    def cansolve(self):
        return True
        
    def incr_attempt(self):
        pass
        