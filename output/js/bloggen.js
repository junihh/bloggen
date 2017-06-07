
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
        var navActive = 'active';

        if ( pageType == 'home' )
        {
            if ( locationCategory )
            {
                document.querySelector('#site-nav [data-category="' + locationCategory + '"]').className = navActive;
            } else {
                document.querySelector('#site-nav [data-category="home"]').className = navActive;
            };
        } else {
            var cat = xClean(document.querySelector('[data-pagetype="post"] [data-category]').dataset.category);
            document.querySelector('#site-nav [data-category="' + cat + '"]').className = navActive;
        };

        if ( locationCategory )
        {
            var nodes = nodesFilter.length;

            if ( nodes )
            {
                for ( var i = 0; i < nodes; i++ )
                {
                    var row = nodesFilter[i];
                    var cat = String(row.dataset.filter).trim().toLowerCase();

                    row.style.removeProperty('display');

                    if ( cat != locationCategory )
                    {
                        row.style.display = 'none';
                    };
                }
            };
        };
    };

    return {
        ini: xCategories
    };
})();
