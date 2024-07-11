from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
# for protect login user
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.


def index(req):
    return render(req,'index.html')


def Tweet_list(req):
    tweets = Tweet.objects.all().order_by('-createdAt')
    return render(req , 'tweet_list.html' , {'tweets':tweets})


@login_required
def Tweet_create(req):
    if req.method == "POST":
        form =TweetForm(req.POST, req.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    
    return render(req,'tweet_form.html',{'form':form})

@login_required
def tweet_edit(req, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = req.user)
    if req.method=="POST":
        form = TweetForm(req.POST, req.FILES, instance=tweet)

        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()
            return redirect('tweet_list')

    else:
        form = TweetForm(instance=tweet)
            
    return render(req, 'tweet_form.html',{'form':form})


@login_required
def tweet_delete(req, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=req.user)
    
    if req.method == "POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(req, 'tweet_confirm_delete.html',{'tweet':tweet})
            

def register(req):
    if req.method == "POST":
        form = UserRegistrationForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(req, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(req, 'registration/register.html', {'form':form})