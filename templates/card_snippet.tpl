<div class="card-box{% if longbox %} long-card-box{% endif %}{% if card.solved %} solved{% endif %}">
	{% if firstsolve %}<p class="firstsolve">First solved by <a href="{% url solved_view firstsolve.user.username%}">{{ firstsolve.user.username }}</a> on {{firstsolve.solved|date:"D jS N Y"}}</p>{%endif%}
	<img src="/images/card/{{card.key}}.png" class="card-image" />
	<p class="number"><span class="{{card.colour|lower}}">#{{card.key}}</span></p>
	<p class="title">{% if user.is_authenticated %}<a href="{{card.get_absolute_url}}">{{card.name}}</a>{% else %}{{card.name}}{% endif %}</p>
</div>