<?xml version="1.0" encoding="UTF-8"?> 
<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" 
        xmlns:n="http://www.google.com/schemas/sitemap-news/0.9" 
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
    
    <url>
        <loc>{{ https }}://{{ site_domain }}/</loc>
        <priority>1.0</priority>
        <changefreq>{{ changefreq }}</changefreq>
        <lastmod>{{ lastmod }}</lastmod>
    </url>

    {% for category in categories -%}
    <url>
        <loc>{{ https }}://{{ site_domain }}/index.html?category={{ category|slugify }}</loc>
        <priority>0.8</priority>
        <changefreq>{{ changefreq }}</changefreq>
        <lastmod>{{ lastmod }}</lastmod>
    </url>
    {% endfor %}
    {% for row in rows -%}
    <url>
        <loc>{{ https }}://{{ site_domain }}/{{ row.file }}</loc>
        <priority>0.7</priority>
        <changefreq>{{ changefreq }}</changefreq>
        <lastmod>{{ row.date.modified }}</lastmod>
    </url>
    {% endfor %}
</urlset>
