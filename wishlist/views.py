import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from wishlist.models import BarangWishlist
from .forms import Input_Form

@login_required(login_url='/wishlist/login/')
def show_wishlist(request):
    data_barang_wishlist = BarangWishlist.objects.all()
    context = {
        'list_barang': data_barang_wishlist,
        'nama': 'Rahma',
        'last_login': request.COOKIES['last_login'],
    }
    return render(request, "wishlist.html", context)

def show_wishlist_ajax(request):
    context = {
        'nama': 'Rahma',
        'last_login': request.COOKIES['last_login'],
    }
    return render(request, "wishlist_ajax.html", context)

data = BarangWishlist.objects.all()

def show_xml(request):
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('wishlist:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) # melakukan login terlebih dahulu
            response = HttpResponseRedirect(reverse("wishlist:show_wishlist")) # membuat response
            response.set_cookie('last_login', str(datetime.datetime.now())) # membuat cookie last_login dan menambahkannya ke dalam response
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)
    
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('wishlist:login'))
    response.delete_cookie('last_login')
    return response

# fungsi membuat task
def tambah_barang(request):
    # memvalidasi input
    if request.method == 'POST':
        task_form = Input_Form(request.POST)
        if task_form.is_valid():
            barang_nama = request.POST.get('nama')
            barang_harga = request.POST.get('harga')
            barang_deskripsi = request.POST.get('deskripsi')
            
            # membuat objek baru berdasarkan model dan menyimpannya ke database
            barang = BarangWishlist(nama=barang_nama, harga=barang_harga, deskripsi=barang_deskripsi)
            barang.save()
            
            # mengembalikan ke halaman yang menampilkan tasks
            context = {
                "task_user" : request.user,
                "last_login": request.COOKIES['last_login']  
            }
            return render(request, 'wishlist_ajax.html', context)  
        else:
            task_form = Input_Form()
            messages.info(request, 'Fill out all fields to proceed')
    return render(request, 'wishlist_ajax.html')  