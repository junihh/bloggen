# Bloggen

Just another static site generator. ;-)

## Requirements:

    pip install pyyaml   
    pip install mistune   
    pip install jinja2   
    pip install beautifulsoup4   

## How to use:

    from modules.bloggen import Bloggen

    Bloggen().make(
        postdir = './posts', 
        outputdir = './blog-output',
        domain = 'myanime.blog',
        site_title = 'My anime blog'
    )

You can also do this if you want to compile multiple projects.

    coolblog = Bloggen()
    coolblog.make(
        ...
    )

    anotherblog = Bloggen()
    anotherblog.make(
        ...
    )

## Attributes of "make":  

- **postdir:** [required] The directory with the yaml files of the post.
- **outputdir:** [required] The directory where all post compiled to HTML will be created.
- **domain:** [optional] The domain of your website. Is used to make the permalink of the post.
- **site_title:** [optional] The main title of your website.
- **encodedResources:** [optional] False or True (boolean), depending on whether or not you want to compile the images to data uri.

## FQ&A
- **Why the images appear to be broken after compiling?**   
Because you forgot to add your images, CSS files and javascripts in the "outputdir" directory.

- **How to stop encoding the images to data uri?**  
Just add "encodedResources=False" to the "make" call.


