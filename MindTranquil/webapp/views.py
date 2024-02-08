from django.shortcuts import render, redirect

from .forms import RegistrationForm, LoginUserForm

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

#register a new user
def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.preferred_mode = 'light'
            user.save()
            auth.login(request, user)
            return redirect('webapp:index')
    else:
        form = RegistrationForm()
    return render(request, 'webapp/register.html', {'form': form})

#login a user
def user_login(request):
    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('webapp:index')
    else:
        form = LoginUserForm()
    return render(request, 'webapp/login.html', {'form': form})

#logging out
def user_logout(request):
    auth.logout(request)
    return redirect('webapp:index')

# homepage
def index(request):
    context = {'user': request.user}
    return render(request, 'webapp/index.html', context=context)

#redirect to breathe
@login_required(login_url='webapp:login')
def breathe(request):
    return render(request, 'webapp/breathe.html')

#redirect to meditate
@login_required(login_url='webapp:login')
def meditate(request):
    return render(request, 'webapp/meditate.html')

#redirect to stats
@login_required(login_url='webapp:login')
def stats(request):
    return render(request, 'webapp/stats.html')

    
#API view for updating mode
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_mode_api(request):
    serializer = UserSerializer(instance=request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Preferred mode updated successfully'})
    else:
        return Response({'error': 'Invalid request method'}, status=400)

#redirect to music playing mode
@login_required(login_url='webapp:login')
def play_music(request):
    return render(request, 'webapp/play_music.html', context={'data': request.POST})