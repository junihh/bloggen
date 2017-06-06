from modules.bloggen import maker

myblog = dict(
    domain='junihh.com', 
    site_title='My bloggen test', 
    postmds='./postmds', 
    output='./output'
)

maker(myblog)
