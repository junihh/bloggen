<!DOCTYPE html>
<html lang="es">
    <head>
        <title>{{ site_title }}</title>

        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,minimum-scale=1,user-scalable=no">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <meta name="googlebot" content="noindex,nofollow">
        <meta name="robots" content="noindex,nofollow">
        
        <link href="css/styles.css" rel="stylesheet" type="text/css" media="screen">
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

        <script src="js/bloggen.js"></script>
        <script>
            bloggen.ini()
        </script>
    </body>
</html>
