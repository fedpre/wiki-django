from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import random
from markdown2 import Markdown
from . import util

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki_page(request, title):
    wiki_page = util.get_entry(title)
    markdowner = Markdown()
    html_conversion = markdowner.convert(wiki_page)
    if wiki_page == None:
        return render(request, "encyclopedia/not_found.html", {
            "title": title,
        })

    return render(request, 'encyclopedia/wiki_page.html', {
        "page": html_conversion,
        "title": title,
    })

def search(request):
    if request.method == 'POST':
        new_entries = list()
        for entry in util.list_entries():
            if request.POST["q"].lower() == entry.lower():
                wiki_page = util.get_entry(entry)
                return render(request, "encyclopedia/wiki_page.html", {
                    "page": wiki_page,
                    "title": entry
                })
            if request.POST["q"].lower() in entry.lower():
                new_entries.append(entry)

        return render(request, "encyclopedia/search.html", {
            "entries": new_entries,
            "keyword": request.POST["q"],
        })
    return render(request, "encyclopedia/not_found.html")

def new_entry(request):
    if request.method == 'POST':
        title = request.POST["title"]
        content = request.POST["content"]
        if title == '' or content == '':
            return render(request, "encyclopedia/missing.html")
        wiki_pages = util.list_entries()
        for entry in wiki_pages:
            if title.lower() == entry.lower():
                return render(request, "encyclopedia/duplicate.html", {
                    "title": title,
                })
        util.save_entry(title, content)
        return HttpResponseRedirect(f"wiki/{title}")

    return render(request, "encyclopedia/new_entry.html", )

def edit_page(request, title):
    content = util.get_entry(title)
    if request.method == 'POST':
        # title_edit = request.POST["title_edit"]
        content_edit = request.POST["content_edit"]
        util.save_entry(title, content_edit)
        wiki_page = util.get_entry(title)
        url = reverse('title', args=[title])
        return HttpResponseRedirect(url)
    
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content,
    })

def random_entry(request):
    wiki_pages = util.list_entries()
    random_number = random.randint(0, len(wiki_pages) - 1)
    title = wiki_pages[random_number]
    url = reverse('title', args=[title])
    return HttpResponseRedirect(url)