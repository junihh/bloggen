import re


def slugify(name=None):
    s = name

    if name is not None:
        s = name.lower()
        
        s = re.sub('á|à|â|ã|ä|å|ā|æ', 'a', s);
        s = re.sub('é|è|ê|ë|ē|ę', 'e', s);
        s = re.sub('í|î|ï|ī', 'i', s);
        s = re.sub('ó|õ|ô|ö|ő|ō|ø|œ', 'o', s);
        s = re.sub('ú|ü|û|ů|ű|ŭ|ū', 'u', s);

        s = re.sub('ç|č|ĉ|ć', 'c', s);
        s = re.sub('š|ŝ|ś|ş', 's', s);
        s = re.sub('ÿ|ý|ŷ', 'y', s);
        s = re.sub('ž|ź|ż', 'z', s);
        s = re.sub('ţ|ț', 't', s);
        s = re.sub('ñ|ň', 'n', s);
        s = re.sub('ř', 'r', s);
        s = re.sub('ĵ', 'j', s);
        s = re.sub('ğ', 'g', s);
        s = re.sub('ŵ', 'w', s);
        s = re.sub('ß', 'b', s);

        s = re.sub('([^\s\w]|_)+', '', s);
        s = re.sub('(\r\n|\n|\r|\s+)', '-', s);

    return s


print slugify('Esto es un -título- muy cool de [Junior Hernández]')





