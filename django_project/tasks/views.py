from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from .models import BreedLike


def logout_view(request):
    logout(request)
    return redirect('index')


def index(request):
    return render(request, "index.html", {})


def breeds(request):
    return render(request, "breeds.html", {})


def care(request):
    return render(request, "care.html", {})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            return JsonResponse({'success': True})
        errors = {f: [str(e) for e in err] for f, err in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors}, status=400)
    return JsonResponse({}, status=400)


@require_POST
@login_required
def like_breed(request):
    breed_name = request.POST.get('breed_name')
    action = request.POST.get('action')

    if action not in ['like', 'dislike']:
        return JsonResponse({'status': 'error', 'message': 'Invalid action'})

    value = 1 if action == 'like' else -1

    like, created = BreedLike.objects.update_or_create(
        user=request.user,
        breed_name=breed_name,
        defaults={'value': value}
    )

    likes = BreedLike.objects.filter(breed_name=breed_name, value=1).count()
    dislikes = BreedLike.objects.filter(breed_name=breed_name, value=-1).count()

    return JsonResponse({
        'status': 'success',
        'likes': likes,
        'dislikes': dislikes,
        'user_vote': value
    })


@require_GET
def get_likes(request):
    breed_name = request.GET.get('breed_name')

    likes = BreedLike.objects.filter(breed_name=breed_name, value=1).count()
    dislikes = BreedLike.objects.filter(breed_name=breed_name, value=-1).count()

    return JsonResponse({
        'likes': likes,
        'dislikes': dislikes
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True})
        errors = {f: [str(e) for e in err] for f, err in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors}, status=400)
    return JsonResponse({}, status=400)