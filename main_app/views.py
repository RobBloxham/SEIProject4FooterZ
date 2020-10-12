from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Sneakers, Photo
import uuid
import boto3
from botocore.exceptions import ClientError

S3_BASE_URL='https://s3.us-west-1.amazonaws.com/'
BUCKET='footerz'


@login_required
def add_photo(request, sneakers_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, sneakers_id=sneakers_id)
            photo.save()
        except ClientError as e:
            print(e)
            print('An error occurred uploading file to S3')
    return redirect('detail', sneakers_id=sneakers_id)

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def sneakers_index(request):
  sneakers = Sneakers.objects.filter(user=request.user)
  return render(request, 'sneakers/index.html', { 'sneakers': sneakers })

@login_required
def sneakers_detail(request, sneakers_id):
  sneakers = Sneakers.objects.get(id=sneakers_id)
  return render(request, 'sneakers/detail.html', {
    'sneakers': sneakers,
  })

class SneakersCreate(LoginRequiredMixin, CreateView):
  model = Sneakers
  fields = ['name', 'brand', 'colorway', 'description', 'year']
  

  def form_valid(self, form):
    form.instance.user = self.request.user 
    return super().form_valid(form)

class SneakersUpdate(LoginRequiredMixin, UpdateView):
  model = Sneakers
  fields = ['name', 'brand', 'colorway', 'description', 'year']

class SneakersDelete(LoginRequiredMixin, DeleteView):
  model = Sneakers
  success_url = '/sneakers/'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)