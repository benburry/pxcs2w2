<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
 
<html> 
	<head> 
	
		<link rel="stylesheet" type="text/css" href="/styles/core.css" /> 
		<title>Perplex City S2W2 Solver</title> 
		</head> 
	
	<body> 
 
	<a name="top" id="top"></a> 
			<div id="header"> 
		<div id="header-content"> 
			<p class="hide"><a href="#nav">Skip to navigation</a></p> 
			<h1 class="header" id="linked"><a href="/" title="Perplex City S2W2">Perplex City S2W2<span></span></a></h1> 
		</div> 
	</div> 
	
	<div id="wrapper">	
	<!-- start wrapper --><!-- /# Start Inside Pages --> 
 
		<div id="inside"> 
			<div id="inside-content"> 

					
{% block body %}
{% endblock body %}

			</div> 
 
		</div> 
		
		<div id="main-bottom"></div> 
		<!-- /# End Inside Pages --> 
 
		<hr class="hide" /> 
		<a name="nav"></a> 
		<div id="navbar"> 
			<h3 class="hide">Main navigation:</h3> 
			<ul id="nav"> 
				<li><a accesskey="s" title="Solve" href="/">Solve</a></li> 
				{% if user.is_authenticated %}
				<li><a accesskey="s" title="Profile" href="{% url solved_view user.username %}">Profile</a></li> 				
				<li><a accesskey="l" title="Sign out"  href="{% url logout %}">Sign out</a></li> 
				{% endif %}
			</ul> 
		</div><!-- end wrapper -->	
		</div> 
		<!-- start footer --> 
		<div id="footer"> 
 
			<hr class="hide" /> 
			<p>&copy; <a href="http://www.perplexcity.com" title="View the Perplex City website">Perplex City</a></p> 
		</div> 
		<!-- end footer --> 
		{% if debug %}
		<div>
			{% for query in sql_queries %}
				<p>{{query.sql}} : {{query.time}}</p>
			{% endfor %}
		</div>
		{% endif %}
	</body> 
</html>