from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Sneakers
import uuid
import boto3

S3_BASE_URL='https://s3-us-west-1.amazonaws.com/'
BUCKET='catcol'

# Define the home view
@login_required
def add_photo(request, cat_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, sneakers_id=sneakers_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', sneakers_id=sneakers_id)

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def sneakers_index(request):
  sneakers = Sneakers.objects.filter(user=request.user)
  # You could also retrieve the logged in user's cats like this
  # cats = request.user.cat_set.all()
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
  
  # This inherited method is called when a
  # valid cat form is being submitted
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
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
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)