from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

from .models import Post, Comment

# Login required decorator, makes sure that people can't open the site
# without being logged in. They will be returned to /login.


@login_required
def index(request):
    # Index view gets all posts and renders the index.html with posts inside
    # the context
    posts = Post.objects.all()
    context = {
        'posts': posts
    }

    return render(request, 'whiteboard_app/index.html', context)


@login_required
def createPost(request):
    # If something was posted, gather the information and create a post
    if request.method == "POST":
        user = request.user
        text = request.POST['text']
        url = request.POST['url']
        Post.create_post(user, text, url)
        return HttpResponseRedirect(reverse('whiteboard_app:createPost'))
    myPosts = Post.objects.filter(user=request.user)
    context = {
        'myPosts': myPosts
    }

    return render(request, 'whiteboard_app/createPost.html', context)


@login_required
def deletePost(request, post_pk):
    # An extra check, just to make sure that the user that is trying to delete
    # the post, is actually the creator of the post
    if request.user.pk == Post.objects.get(pk=post_pk).user.pk:
        post = get_object_or_404(Post, pk=post_pk)
        post.delete()
        return HttpResponseRedirect(reverse('whiteboard_app:index'))


@login_required
def createComment(request):
    # Same procedure as index, get the info and create a comment.
    if request.method == "POST":
        user = request.user
        text = request.POST['comment']
        post = get_object_or_404(Post, pk=request.POST['post-pk'])
        Comment.create_comment(user, text, post)
        return HttpResponseRedirect(reverse('whiteboard_app:index'))


@login_required
def createUser(request):
    if request.method == "POST":
        if request.POST['password'] == request.POST['confirm_password']:
            # As "User" is a django-model, i haven't done a custom
            # create-method, so with the gathered data from the post,
            # I create the User directly in the view (if it passes the checks)
            try:
                User.objects.create_user(username=request.POST['username'],
                                         first_name=request.POST['first_name'],
                                         last_name=request.POST['last_name'],
                                         email=request.POST['email'],
                                         password=request.POST['password']
                                         ).save()
            except:
                pass
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'whiteboard_app/createUser.html', context)

# Only users that are superusers, are allowed to enter this view


@user_passes_test(lambda u: u.is_superuser)
def adminPage(request):
    if request.method == "POST":
        # Check if the checkbox is checked, if it is, I change the users status
        # to superuser, if it isn't checked, the superuser status will be removed
        form_superuser = request.POST.get('is_superuser', False)
        pk = request.POST['pk']
        user = User.objects.get(pk=pk)
        user.is_superuser = form_superuser
        user.save()

    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'whiteboard_app/adminPage.html', context)
