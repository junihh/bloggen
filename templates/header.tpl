<header class="blog-header">
                    <div class="table">
                        <div class="cell">
                            <h1>{{ site_title }}</h1>
                        </div>
                        <nav class="cell">
                            <ul>
                                <li><a href="javascript:;">home</a></li>
                                {% for item in categories %}
                                <li><a href="javascript:;">{{ item }}</a></li>
                                {% endfor %}
                            </ul>
                        </nav>
                    </div>
                </header>