<div class="card-box{% if card.solved %} solved{% endif %}">
	<img src="/images/card/{{card.key}}.png" class="card-image" />
	<p class="number"><span class="{{card.colour|lower}}">#{{card.key}}</span></p>
	<p class="title">{% if user.is_authenticated %}<a href="{{card.get_absolute_url}}">{{card.name}}</a>{% else %}{{card.name}}{% endif %}</p>
</div>