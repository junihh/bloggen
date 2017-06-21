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
                    {% for row in rows -%}
                    <article data-filter="{{ row.category }}">
                        <h2 class="title"><a href="{{ row.file }}">{{ row.title }}</a></h2>
                        {% if row.excerpt -%}
                        {{ row.excerpt|parsemd(site_domain) }}
                        {%- endif %}
                        <p class="read-more">
                            <a href="{{ row.file }}">Read more</a>
                        </p>
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
