from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages


@login_required(login_url='login')
@never_cache
def HomePage(request):
    return render (request,'home.html')


@never_cache
def signupPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')


        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')
        elif len(uname) < 3:
            messages.error(request, "Username must be at least 3 characters long")
            return redirect('signup')
        elif not uname.isalnum():
            messages.error(request, "Username should be alphanumeric")
            return redirect('signup')

        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup')
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render(request, 'signup.html')


@never_cache
def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username') 
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
        
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request,'login.html')


def LogoutPage(request):
    if 'username' in request.session:
        request.session.flush()
    logout(request)
    return redirect('login')

# ///////////////////////
def loginAdmin(request):
    if 'username' in request.session:
        return redirect('adminpage')

    if request.method == 'POST':
        username = request.POST.get('username')
        pasw = request.POST.get('password')
        user = authenticate(request,username=username,password=pasw)
        
        
        if user is not None and user.is_superuser:
            request.session['username'] = username
            return redirect('adminpage')
        else:messages.info(request,'Invalid Credentials !!')
    return render(request, 'adlogin.html')

@never_cache
def userData(request):
    
    emp = User.objects.all()

    context = {
        'emp':emp,
        }
    if 'username' in request.session:
        return render(request,'users.html', context)
    return redirect('admlogin')


def addEmp(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pas1 = request.POST.get('password1')
        pas2 = request.POST.get('password2')

    
        if pas1 != pas2:
            messages.error(request, 'Passwords do not match')
            return redirect('adminpage')
        elif len(uname) < 3:
            messages.error(request, 'Username must be at least 3 characters long')
            return redirect('adminpage')
        elif not uname.isalnum():
            messages.error(request, 'Username should be alphanumeric')
            return redirect('adminpage')

  
        my_user = User.objects.create_user(uname, email, pas1)
        my_user.save()

        return redirect('adminpage')

    return render(request, 'users.html')


def editEmp(request):
    emp = User.objects.all()
    
    context = {
        'emp':emp,
    }
    return render(request, 'users.html',context)



def updatEmp(request,id):
    if request.method == 'POST':
        username = request.POST.get('username')
        if not username.isalnum():
            messages.error(request, "Username should be correct format")
            return redirect('adminpage')
        
        email = request.POST.get('email')
        User.objects.filter(id=id).update(username=username,email=email)
        
        return redirect('adminpage')
    return redirect(request, 'users.html')

def delEmp(request,id):
    User.objects.filter(id=id).delete()
    return redirect('adminpage')

def signOut(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect('admlogin')