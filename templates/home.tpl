<!DOCTYPE html>
<html lang="es">
    <head>
        <title>{{ site_title }}</title>

        {% include 'meta.tpl' %}
    </head>
    <body>
        {% include 'header.tpl' %}

        <div class="search-box">
            <div class="center">
                <div class="margins">
                    <input type="text" placeholder="search the content below" name="input-search" id="input-search">
                </div>
            </div>
        </div>
        
        <div class="center">
            <div class="margins">
                <main class="home" data-pagetype="home" id="post-list">
                    {% for row in rows %}
                    <article data-filter="{{ row.category }}">
                        <h2 class="title"><a href="{{ row.file }}">{{ row.title }}</a></h2>
                        <div class="meta">
                            <a href="index.html?category={{ row.category }}" data-category="{{ row.category }}" class="category">{{ row.category }}</a>
                            <time>{{ row.date }}</time>
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

        <script src="resources/js/bloggen.js"></script>
        <script>
            bloggen.categoriesNav();
            bloggen.homeSearch();
        </script>
    </body>
</html>
