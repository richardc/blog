---
layout: page
title: Home
---
{% include JB/setup %}

This is the occasional blog of Richard Clamp.  Mostly technical, rarely updated.

## Recent Posts

<ul class="posts">
  {% for post in site.posts limit:5 %}
    <li><span>{{ post.date | date_to_string }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>
