from modules.bloggen import Bloggen

Bloggen().make(
    domain = 'junihh.com',
    site_title = 'My bloggen test',
    postdir = './posts', 
    outputdir = './output'
)
