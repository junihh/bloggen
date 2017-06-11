from modules.bloggen import Bloggen

Bloggen().make(
    domain = 'junihh.com',
    site_title = 'My anime blog',
    postdir = './posts', 
    outputdir = './output'
)
