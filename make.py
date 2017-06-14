from bloggenmod.bloggen import Bloggen

Bloggen().make(
    postdir = './posts', 
    outputdir = './blog-output',
    domain = 'myanime.blog',
    site_title = 'My anime blog',
    # embeddedResources = False
)
