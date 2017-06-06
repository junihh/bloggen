from modules.bloggen import maker

# REQUIREMENTS:
# pip install pyyaml
# pip install mistune

myblog = dict(
    domain='junihh.com', 
    site_title='My bloggen test', 
    postmds='./postmds', 
    output='./output'
)

maker(myblog)
