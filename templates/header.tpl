<header class="blog-header">
                    <div class="table">
                        <div class="cell">
                            <h1>{{ site_title }}</h1>
                        </div>
                        <nav class="cell" id="site-nav">
                            <ul>
                                <li><a href="index.html" data-category="home">home</a></li>
                                {% for item in categories %}
                                <li><a href="index.html?category={{ item }}" data-category="{{ item }}">{{ item }}</a></li>
                                {% endfor %}
                            </ul>
                        </nav>
                    </div>
                </header>