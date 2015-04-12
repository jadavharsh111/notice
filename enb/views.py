from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import logout
from forms import *
from models import *
from django.views.generic.base import TemplateView
from django.db import models
from django.contrib.auth.decorators import login_required


class RegisterSuccess(TemplateView):
    template_name = 'registration/register_success.html'
# Create your views here.
class start_page(TemplateView):
    template_name = 'enb/index.html'

class plan(TemplateView):
    template_name = 'enb/plan.html'

def main_page(request):
    posts = Dashboard.objects.all().order_by("-pub_date")
    variables = RequestContext(request,{
        'posts':posts,
    })
    return render_to_response('enb/main_page.html', variables)

def user_page(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.dashboard_set.order_by('-pub_date')
    variables = RequestContext(request, {
        'username': username,
        'posts': posts,
        'show_tags': True,
    })
    return render_to_response('enb/user_page.html', variables)

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/enb/success')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response(
        'registration/register.html',
        variables
    )

def tag_page(request, tag_name):
    pass

@login_required(login_url='/enb/login')
def submit_page(request):
    if request.method == 'POST':
        form = DashForm(request.POST,request.FILES)
        if form.is_valid(): #create a ink then

            sub = Dashboard.objects.create(
                user= request.user,
                topic= form.cleaned_data['topic'],
                desc= form.cleaned_data['desc'],
                img= form.cleaned_data['img'],
                file= form.cleaned_data['file'],

            )

            #create a new tag list
            tag_names = form.cleaned_data['tags'].split()
            for tag_name in tag_names:
                tag, dummy = Tag.objects.get_or_create(name=tag_name)
                sub.tag_set.add(tag)
            sub.save()
            return HttpResponseRedirect('/enb/user/%s' % request.user.username)

    else:
        form = DashForm
    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('enb/submit.html', variables)

def tag_cloud_page(request):
    MAX_WEIGHT = 5
    tags = Tag.objects.order_by('name')
# Calculate tag, min and max counts.
    min_count = max_count = tags[0].dash.count()
    for tag in tags:
        tag.count = tag.dash.count()
        if tag.count < min_count:
            min_count = tag.count
        if max_count < tag.count:
            max_count = tag.count
# Calculate count range. Avoid dividing by zero.
    range = float(max_count - min_count)
    if range == 0.0:
        range = 1.0
# Calculate tag weights.
    for tag in tags:
        tag.weight = int(
            MAX_WEIGHT * (tag.count - min_count) / range
        )
    variables = RequestContext(request, {
    'tags': tags
})
    return render_to_response('enb/tag_cloud_page.html', variables)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/enb')
