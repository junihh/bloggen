<!DOCTYPE html>
<html lang="es">
    <head>
        <title>{{ site_title }}</title>

        {% include 'meta.tpl' %}
    </head>
    <body>
        <div class="blog">
            <div class="margins">
                {% include 'header.tpl' %}
                <main class="home" data-pagetype="home">
                    {% for row in rows %}
                    <article data-filter="{{ row.category }}">
                        <h2><a href="{{ row.file }}" class="title">{{ row.title }}</a></h2>
                        <div class="meta">
                            <time>{{ row.date }}</time>
                            <a href="index.html?category={{ row.category }}" data-category="{{ row.category }}">{{ row.category }}</a>
                        </div>
                        {% if row.excerpt %}
                        <p>{{ row.excerpt }}</p>
                        {% endif %}
                    </article>
                    {% endfor %}
                </main>
                {% include 'footer.tpl' %}
            </div>
        </div>

        {% include 'jscripts.tpl' %}
    </body>
</html>
