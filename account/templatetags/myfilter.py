from django import template

register = template.Library()
@register.filter(name='prevpage')
def prevpage(page,maxpage):
    try:
        if page is None or page=='':
            page = 1
        page = int(page)
        maxpage = int(maxpage)
        page = page-1
        page = max(min(maxpage, page),1)
        return page
    except Exception as e:
        print(e)
        return 1
@register.filter(name='nextpage')
def nextpage(page,maxpage):
    try:
        if page is None or page=='':
            page = 1
        page = int(page)
        maxpage = int(maxpage)
        page = page+1
        page = max(min(maxpage, page),1)
        return page
    except Exception as e:
        print(e)
        return 1