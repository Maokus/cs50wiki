from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from markdownify import markdownify as md
import random
import markdown
import os


from . import util

class hiddeninfoform(forms.Form):
    pass

def index(request):
    rendered_entries=[]

    if request.method=="POST":
        query = request.POST.get('q')
        for entry in util.list_entries():
            if entry==query:
                return HttpResponseRedirect("/wiki/"+entry)
            if query in entry:
                rendered_entries+=[entry]
    else:
        rendered_entries = util.list_entries()
    
    return render(request, "encyclopedia/index.html", {
        "entries": rendered_entries
        })

def article(request, articletitle):
    articlecontent = util.get_entry(articletitle)
    if articlecontent==None:
        return HttpResponse("The article " + articletitle + " does not exist!")
    print(articlecontent)
    return render(request, "encyclopedia/article.html", {"titlestr" : articletitle, "articlecontent" : markdown.markdown(articlecontent)}) 

def newpage(request):
    if request.method=="POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if util.get_entry(title)!=None:
            return HttpResponse("A page with this title already exists!")
        util.save_entry(title,content)
        return HttpResponseRedirect("/wiki/"+title)
    return render(request, "encyclopedia/newpage.html", {
        "action":"/newpage",
        "defaultContent":"",
        "editing":False
    })

def editpage(request, articletitle):
    if request.method=="POST":
        util.save_entry(articletitle,request.POST.get('content'))
        return HttpResponseRedirect("/wiki/"+articletitle)

    return render(request, "encyclopedia/newpage.html",{
        "action":"/edit/"+articletitle,
        "defaultContent":util.get_entry(articletitle),
        "editing":True,
    })

def randompage(request):
    return HttpResponseRedirect("/wiki/"+random.choice(util.list_entries()))
