<header class="site-header">
            <div class="center">
                <div class="margins">
                    <div class="table">
                        <div class="cell">
                            <h1 class="site-title">
                                <a href="index.html">{{ site_title }}</a>
                            </h1>
                        </div>
                        <div class="cell">
                            <nav class="site-nav" id="site-nav">
                                <a href="javascript:;" class="nav-button" id="nav-button">
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </a>
                                <ul>
                                    <li><a href="index.html" data-category="home">home</a></li>
                                    {% for category in categories %}
                                    <li><a href="index.html?category={{ category }}" data-category="{{ category }}">{{ category }}</a></li>
                                    {% endfor %}
                                </ul>
                            </nav>
                        </div>
                    </div>
                </div>
            </div>
        </header>