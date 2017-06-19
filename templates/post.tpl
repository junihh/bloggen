<!DOCTYPE html>
<html lang="es">
    <head>
        <title>{{ site_title }} | {{ post.title }}</title>

        {% include 'meta.tpl' %}
    </head>
    <body>
        {% include 'header.tpl' %}
        
        <div class="center">
            <div class="margins">
                <article class="post" data-pagetype="post">
                    <header class="post-header">
                        <h2>{{ post.title }}</h2>
                        <div class="meta">
                            <a href="index.html?category={{ post.category }}" data-category="{{ post.category }}" class="category">{{ post.category }}</a>
                            <span><time datetime="{{ post.date }}">{{ post.date|humanizeddate }}</time></span>
                            <span>|</span>
                            <span rel="author">By {{ post.author }}</span>
                        </div>
                    </header>
                    <div class="post-content">
                        {% if post.image -%}
                        <figure class="post-image">
                            <img src="{{ post.image }}" alt="{{ post.title }}" width="1280" height="650">
                        </figure>
                        {%- endif %}
                        {% if post.content -%}
                        {{ post.content|parsemd }}
                        {%- endif %}
                    </div>
                    {% if post.inshort -%}
                    <div class="post-info">
                        <h3>In short</h3>
                        <ul>
                            {% for row in post.inshort -%}
                            <li><strong>{{ row }}:</strong> {{ post.inshort[row] }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                    {%- endif %}
                </article>
                {% include 'footer.tpl' %}
            </div>
        </div>

        <script src="resources/js/bloggen.js"></script>
        <script>
            bloggen.categoriesNav();
        </script>
    </body>
</html>
