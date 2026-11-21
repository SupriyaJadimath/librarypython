
from django.shortcuts import render, redirect
from .models import Book,Member,IssueBook
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout

def home(request):
    return render(request, 'library/home.html')


def add_book(request):
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        author = request.POST.get('author')
        category = request.POST.get('category')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        Book.objects.create(
            book_name=book_name,
            author=author,
            category=category,
            quantity=quantity,
            price=price
        )

        return redirect('home')

    return render(request, 'library/add_book.html')



def view_books(request):
    search = request.GET.get('search')

    if search:
        books = Book.objects.filter(
            book_name__icontains=search
        ) | Book.objects.filter(
            author__icontains=search
        )
    else:
        books = Book.objects.all()

    return render(request, 'library/view_books.html', {
        'books': books,
        'search': search
    })


def edit_book(request, id):
    book = Book.objects.get(id=id)

    if request.method == 'POST':
        book.book_name = request.POST.get('book_name')
        book.author = request.POST.get('author')
        book.category = request.POST.get('category')
        book.quantity = request.POST.get('quantity')
        book.price = request.POST.get('price')

        book.save()

        return redirect('view_books')

    return render(request, 'library/edit_book.html', {'book': book})


def delete_book(request, id):
    book = Book.objects.get(id=id)
    book.delete()

    return redirect('view_books')


def dashboard(request):
    total_books = Book.objects.count()

    total_quantity = Book.objects.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    available_books = Book.objects.filter(
        quantity__gt=0
    ).count()

    return render(request, 'library/dashboard.html', {
        'total_books': total_books,
        'total_quantity': total_quantity,
        'available_books': available_books,
    })


def add_member(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        Member.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address
        )

        return redirect('view_members')

    return render(request, 'library/add_member.html')


def view_members(request):
    members = Member.objects.all()
    return render(request, 'library/view_member.html', {
        'members': members
    })



def issue_book(request):
    books = Book.objects.filter(quantity__gt=0)
    members = Member.objects.all()

    if request.method == 'POST':
        book_id = request.POST.get('book')
        member_id = request.POST.get('member')

        book = Book.objects.get(id=book_id)
        member = Member.objects.get(id=member_id)

        if book.quantity > 0:
            IssueBook.objects.create(
                book=book,
                member=member
            )

            book.quantity -= 1
            book.save()

            return redirect('view_books')

    return render(request, 'library/issue_book.html', {
        'books': books,
        'members': members
    })


def return_book(request):
    issued_books = IssueBook.objects.filter(is_returned=False)

    if request.method == 'POST':
        issue_id = request.POST.get('issue_id')

        issue = get_object_or_404(
            IssueBook,
            id=issue_id,
            is_returned=False
        )

        issue.is_returned = True
        issue.save()

        book = issue.book
        book.quantity += 1
        book.save()

        return redirect('return_book')

    return render(request, 'library/return_book.html', {
        'issued_books': issued_books
    })

def view_issued_books(request):
    issued_books = IssueBook.objects.select_related(
        'book', 'member'
    ).all().order_by('-issue_date')

    return render(request, 'library/view_issued_books.html', {
        'issued_books': issued_books
    })

def edit_member(request, id):
    member = get_object_or_404(Member, id=id)

    if request.method == 'POST':
        member.name = request.POST.get('name')
        member.email = request.POST.get('email')
        member.phone = request.POST.get('phone')
        member.address = request.POST.get('address')

        member.save()
        return redirect('view_members')

    return render(request, 'library/edit_member.html', {
        'member': member
    })

def delete_member(request, id):
    member = get_object_or_404(Member, id=id)

    if request.method == 'POST':
        member.delete()
        return redirect('view_members')

    return redirect('view_members')

def custom_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            return render(request, 'library/login.html', {
                'error': 'Invalid username or password!'
            })

    return render(request, 'library/login.html')

def register(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'library/register.html', {
                'error': 'Passwords do not match!'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'library/register.html', {
                'error': 'Username already exists!'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'library/register.html', {
                'error': 'Email already exists!'
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('custom_login')

    return render(request, 'library/register.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('custom_login')