from modules.bloggen import maker

myBlog = dict(
    domain='junihh.com', 
    site_title='My bloggen test', 
    postmds='./postmds', 
    output='./public'
)

maker(myBlog)
