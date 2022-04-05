from django.http import Http404, HttpResponse
from django.shortcuts import render
from . import util

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki_page(request, title):
    wiki_page = util.get_entry(title)
    if wiki_page == None:
        raise Http404

    return render(request, 'encyclopedia/wiki_page.html', {
        "page": wiki_page,
        "title": title,
    })