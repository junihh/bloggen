
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

    function xFilterRows (params)
    {
        // @param(string): params.rows
        // @param(string): params.input
        // @param(string): params.classEven
        // @param(string): params.classOdd

        if ( !params.rows && !params.input )
        {
            console.error('xFilterRows [error]: "rows" and "input" are mandatory.')
            return;
        };
        
        var input = document.querySelector(params.input);
        var rows = document.querySelectorAll(params.rows);
        var classEven = (params.classEven && (typeof params.classEven === 'string')) ? params.classEven.trim() : undefined;
        var classOdd = (params.classOdd && (typeof params.classOdd === 'string')) ? params.classOdd.trim() : undefined;

        input.addEventListener('input',filter,false);
        input.addEventListener('keyup',filter,false);

        function filter ()
        {
            var inputVal = clean(input.value);
            var isEven = true;

            for ( var r = 0, c = rows.length; r < c; r++ )
            {
                var row = rows[r];
                var rowVal = clean(row.textContent);

                row.classList.remove(classEven);
                row.classList.remove(classOdd);
                
                if ( rowVal.indexOf(inputVal) > -1 )
                {
                    if ( row.style.removeProperty )
                    {
                        row.style.removeProperty('display');
                    } else {
                        row.style.removeAttribute('display');
                    };

                    if ( isEven )
                    {
                        if ( classOdd ) row.classList.add(classOdd);
                        isEven = false;
                    } else {
                        if ( classEven ) row.classList.add(classEven);
                        isEven = true;
                    };
                } else {
                    row.style.display = 'none';
                };
            };
        };

        function clean (str)
        {
            var s = String(str).toLowerCase();

            s = s.replace(/(\r\n|\n|\r|\s+)/gm,'');
            
            s = s.replace(/á|à|â|ã|ä|å|ā|æ/gm,'a');
            s = s.replace(/é|è|ê|ë|ē|ę/gm,'e');
            s = s.replace(/í|î|ï|ī/gm,'i');
            s = s.replace(/ó|õ|ô|ö|ő|ō|ø|œ/gm,'o');
            s = s.replace(/ú|ü|û|ů|ű|ŭ|ū/gm,'u');

            s = s.replace(/ç|č|ĉ|ć/gm,'c');
            s = s.replace(/š|ŝ|ś|ş/gm,'s');
            s = s.replace(/ÿ|ý|ŷ/gm,'y');
            s = s.replace(/ž|ź|ż/gm,'z');
            s = s.replace(/ţ|ț/gm,'t');
            s = s.replace(/ñ|ň/gm,'n');
            s = s.replace(/ř/gm,'r');
            s = s.replace(/ĵ/gm,'j');
            s = s.replace(/ğ/gm,'g');
            s = s.replace(/ŵ/gm,'w');
            s = s.replace(/ß/gm,'b');

            return s;
        };
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
        categoriesNav: xCategories,

        homeSearch: function()
        {
            xFilterRows({
                input: '#input-search',
                rows: '#post-list article[data-filter]'
            });
        }
    };
})();

