<header class="blog-header">
                    <div class="table">
                        <div class="cell">
                            <h1>{{ site_title }}</h1>
                        </div>
                        <nav class="cell" id="site-nav">
                            <ul>
                                <li><a href="index.html" data-category="home">home</a></li>
                                {% for category in categories %}
                                <li><a href="index.html?category={{ category }}" data-category="{{ category }}">{{ category }}</a></li>
                                {% endfor %}
                            </ul>
                        </nav>
                    </div>
                </header>