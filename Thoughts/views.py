from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, JsonResponse
from .models import *
from .forms import *
from django.utils import timezone
from django.views.decorators.cache import cache_control, never_cache
from django.contrib.auth.decorators import login_required
try:
    from django.utils import simplejson as json
except:
    import json
# Create your views here.

@never_cache
@login_required(login_url='/accounts/login')
def index(request):
    Tuser = request.user
    try:
        user = Profile.objects.get(email=Tuser.email)
        if user is None:
            user = Profile()
            user.email = Tuser.email
            user.username = Tuser.username
            user.firstname = Tuser.first_name
            user.lastname = Tuser.last_name
            user.first_flag = 1
            user.save()
        else:
            user.first_flag = 0
            user.save()
    except Profile.DoesNotExist:
        user = Profile()
        user.email = Tuser.email
        user.username = Tuser.username
        user.firstname = Tuser.first_name
        user.lastname = Tuser.last_name
        user.first_flag = 1
        user.save()

    allThoughts = thots.objects.order_by('-thought_on')
    allThoughts = allThoughts.filter(active=True)
    return render(request, 'Thoughts/index.html', {'thoughts': allThoughts})

@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/accounts/login')
def view_thought(request, thought_id):
    Tuser = request.user

    thought = get_object_or_404(thots, id=thought_id)
    relates = thought.relates.filter(active=True)
    relate_form = RelateForm()
    new_relate = None
    like_form = LikeForm()
    new_like = None
    if request.method == 'POST':
        relate_form = RelateForm(data=request.POST)
        like_form = LikeForm(data=request.POST)
        if relate_form.is_valid():
            try:
                new_relate = relate_form.save(commit=False)
                new_relate.related_by_name = Tuser.first_name
                new_relate.thought = thought
                new_relate.related_on = timezone.now()
                new_relate.active = True
                new_relate = relate_form.save()
                relate_form = RelateForm()
                new_relate = None
                #return render(request, 'Thoughts/view.html', {'thought': thought, 'relates': relates, 'new_relate': new_relate, 'relate_form': relate_form, 'new_like': new_like, 'like_form': like_form})
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except:
                pass
        else:
            if thought.likes.filter(liked_by=Tuser.email):
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            new_like = like_form.save(commit=False)
            new_like.liked_by = Tuser.email
            new_like.thought = thought
            new_like.liked = True
            new_like = like_form.save()
            like_form = LikeForm()
            new_like = None
            relate_form = RelateForm()
            new_relate = None
            #return render(request, 'Thoughts/view.html', {'thought': thought, 'relates': relates, 'new_relate': new_relate, 'relate_form': relate_form, 'new_like': new_like, 'like_form': like_form})
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        relate_form = RelateForm()
        like_form = LikeForm()
        return render(request, 'Thoughts/view.html', {'thought': thought, 'relates': relates, 'new_relate': new_relate, 'relate_form': relate_form, 'new_like': new_like, 'like_form': like_form})
    return render(request, 'Thoughts/view.html', {'thought': thought, 'relates': relates, 'new_relate': new_relate, 'relate_form': relate_form, 'new_like': new_like, 'like_form': like_form})

@never_cache
@login_required(login_url='/accounts/login')
def add_thot(request):
    allThoughts = thots.objects.order_by('-thought_on')
    thought_form = ThoughtForm()
    if request.session.get('f'):
        del request.session['f']
        response = redirect('/')
        return response

    new_thought = None
    Tuser = request.user

    if request.method == 'POST':
        thought_form = ThoughtForm(data=request.POST)
        if thought_form.is_valid():
            try:
                new_thought = thought_form.save(commit=False)
                new_thought.thought_on = timezone.now()
                new_thought.active = True
                new_thought.uname = Tuser.first_name
                new_thought = thought_form.save()
                new_thought = None
                thought_form = ThoughtForm()
                request.session['f'] = True
                response = redirect('/')
                return response
                # return HttpResponsePermanentRedirect(reverse('index', args=['allThoughts']))
            except:
                pass
        else:
            return render(request, 'Thoughts/create.html', {'thought_form': thought_form})
    else:
        thought_form = ThoughtForm()
    return render(request, 'Thoughts/create.html', {'thought_form': thought_form, 'new_thought': new_thought})

@never_cache
@login_required(login_url='/accounts/login')
def profile(request):
    Tuser = request.user
    user = Profile.objects.get(email=Tuser.email)
    thoughts = thots.objects.filter(uname=Tuser.first_name)
    thoughts = thoughts.filter(active=True)
    about_form = AboutForm()
    if request.method == 'POST':
        about_form = AboutForm(data=request.POST)
        if about_form.is_valid():
            user.about = about_form.cleaned_data['about_field']
            user.save()
            about_form = AboutForm()
            return HttpResponsePermanentRedirect('')
        else:
            about_form = AboutForm()
            return HttpResponsePermanentRedirect('')
    return render(request, 'Thoughts/profile.html', {'user': user, 'thoughts': thoughts, 'about_form': about_form})


# @login_required(login_url='/accounts/login')
# def like(request, thought_id):
#     allThoughts = thots.objects.order_by('-thought_on')
#     Tuser = request.user
#     #user = Profile.objects.get(email=Tuser.email)
#     thought = get_object_or_404(thots, id=thought_id)
#     like_form = LikeForm()
#     new_like = None
#     if request.method == 'POST':
#         like_form = LikeForm(data=request.POST)
#         # if like_form.is_valid():
#         try:
#             new_like = like_form.save(commit=False)
#             new_like.liked_by = Tuser.email
#             new_like.thought = thought
#             new_like.liked = True
#             new_like = like_form.save()
#             like_form = LikeForm()
#             new_like = None
#             return HttpResponsePermanentRedirect('')
#         except:
#             pass
#     else:
#         like_form = LikeForm()
#     return render(request, 'Thoughts/index.html', {'allThoughts': allThoughts, 'new_like': new_like, 'like_form': like_form})

    # if request.method == 'POST':
    #     if thought.reads.filter(username=Tuser.username):
    #         form = LikeForm(request.POST)
    #         if form.is_valid():
    #             val = form.cleaned_data.get("btn")
    #         thought.reads.remove(Tuser)
    #         thought.save()
    #         message = 'You unread this'
    #         return HttpResponsePermanentRedirect('')
    #     else:
    #         form = LikeForm()
    #         thought.reads.add(Tuser)
    #         thought.save()
    #         message = 'You read this'
    #         return HttpResponsePermanentRedirect('')
    # #ctx = {'reads_count': thought.total_reads, 'message': message}
    # # return HttpResponse(json.dumps(ctx), content_type='application/json')
    #     return HttpResponsePermanentRedirect('')
    # return HttpResponsePermanentRedirect('')
