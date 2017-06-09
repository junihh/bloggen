
var bloggen = (function() {

    function xClean (str)
    {
        return String(str).trim().toLowerCase();
    };

    function xLocationVars ()
    {
        var loc = String(window.location.search).substring(1);
        var obj = {};
        
        if ( loc )
        {
            var par = loc.split('&');
            
            for ( var i = 0, c = par.length; i < c; i++ )
            {
                var p = par[i].split('=');
                obj[ p[0] ] = p[1];
            };
        };
        
        return obj;
    };

    function xCategories ()
    {
        var nodesFilter = document.querySelectorAll('[data-filter]');
        var locationCategory = xLocationVars().category ? xClean(xLocationVars().category) : undefined;
        var pageType = xClean(document.querySelector('[data-pagetype]').dataset.pagetype);
        var classActive = 'active';

        if ( pageType == 'home' )
        {
            if ( locationCategory )
            {
                document.querySelector('#site-nav [data-category="' + locationCategory + '"]').className = classActive;
            } else {
                document.querySelector('#site-nav [data-category="home"]').className = classActive;
            };
        } else {
            var cat = xClean(document.querySelector('[data-pagetype="post"] [data-category]').dataset.category);
            document.querySelector('#site-nav [data-category="' + cat + '"]').className = classActive;
        };

        if ( locationCategory )
        {
            var nodes = nodesFilter.length;

            if ( nodes )
            {
                for ( var i = 0; i < nodes; i++ )
                {
                    var node = nodesFilter[i];
                    var cat = xClean(node.dataset.filter);

                    if ( cat != locationCategory )
                    {
                        node.style.display = 'none';
                    };
                }
            };
        };
    };

    return {
        ini: xCategories
    };
})();
