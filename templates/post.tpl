<!DOCTYPE html>
<html lang="es">
    <head>
        <title>{{ post.title }}</title>

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
                <article class="post">
                    <header class="post-header">
                        <h2>{{ post.title }}</h2>
                        <div class="meta">
                            <time>{{ post.date }}</time>
                            <a href="javascript:;">{{ post.category }}</a>
                        </div>
                    </header>
                    {% if post.image %}
                    <figure class="post-image">
                        <img src="{{ post.image }}" alt="{{ post.title }}" width="709" height="360">
                    </figure>
                    {% endif %}
                    <div class="post-content">
                        {{ post.content }}
                    </div>
                </article>
                {% include 'footer.tpl' %}
            </div>
        </div>

        <script src="js/jquery-3.2.1.slim.min.js"></script>
        <script>
            
        </script>
    </body>
</html>
