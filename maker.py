from modules.bloggen import maker

myBlog = dict(
    domain='junihh.com', 
    site_title='My bloggen test', 
    posts='./posts', 
    output='./public'
)

maker(myBlog)
