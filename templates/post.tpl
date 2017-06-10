<!DOCTYPE html>
<html lang="es">
    <head>
        <title>{{ site_title }} | {{ post.title }}</title>

        {% include 'meta.tpl' %}
    </head>
    <body>
        <div class="blog">
            <div class="margins">
                {% include 'header.tpl' %}
                <article class="post" data-pagetype="post">
                    <header class="post-header">
                        <h2>{{ post.title }}</h2>
                        <div class="meta">
                            <time>{{ post.date }}</time>
                            <a href="index.html?category={{ post.category }}" data-category="{{ post.category }}">{{ post.category }}</a>
                        </div>
                    </header>
                    {% if post.image %}
                    <figure class="post-image">
                        <img src="{{ post.image }}" alt="{{ post.title }}" width="1280" height="650">
                    </figure>
                    {% endif %}
                    <div class="post-content">
                        {{ post.content }}
                    </div>
                    {% if post.moreinfo %}
                    <div class="post-info">
                        <h3>In short</h3>
                        <ul>
                            {% for row in post.moreinfo %}
                            <li><strong>{{ row }}:</strong> {{ post.moreinfo[row] }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                    {% endif %}
                </article>
                {% include 'footer.tpl' %}
            </div>
        </div>

        {% include 'jscripts.tpl' %}
    </body>
</html>
