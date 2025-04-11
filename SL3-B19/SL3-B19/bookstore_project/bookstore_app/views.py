from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Book
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('book_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        price = request.POST['price']
        Book.objects.create(title=title, author=author, price=price)
        return redirect('book_list')
    return render(request, 'add_book.html')

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

@login_required
def add_to_cart(request, book_id):
    cart = request.session.get('cart', [])
    if book_id not in cart:
        cart.append(book_id)
        request.session['cart'] = cart
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = request.session.get('cart', [])
    books = Book.objects.filter(id__in=cart)
    return render(request, 'cart.html', {'books': books})
