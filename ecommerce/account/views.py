from django.shortcuts import render,redirect

from django.contrib.sites.shortcuts import get_current_site
from .token import  user_tokenizer_generate

from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm, LoginForm, UpdateUserForm
from django.contrib.auth.forms import User
from payment.forms import ShippingForm

from payment.models import ShippingAddress

from django.contrib import messages



def register(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            user = form.save()

            user.is_active = False

            user.save()

            # Email verification template
            current_site = get_current_site(request)
            subject = 'Account Verification Email'
            html_content = render_to_string('account/registration/email-verification.html',{

                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':user_tokenizer_generate.make_token(user),
            })

            text_content = strip_tags(html_content)
            
            # Create the email
            email = EmailMultiAlternatives(
                subject=subject, 
                body=text_content, 
                from_email='vinayaksoni.dev@gmail.com',
                to=[user.email]
            )
            
            email.attach_alternative(html_content, "text/html")
            
            email.send()

            # user.email_user(subject=subject, message=message)
    
            request.session['email'] = user.email
            return redirect('email-verification-sent')

        
    context = {'form':form}

    return render(request, 'account/registration/register.html',context=context)

def email_verification(request, uidb64, token):

    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    # Success
    if user and user_tokenizer_generate.check_token(user,token):
        user.is_active = True
        user.save()
        return redirect('email-verification-success', unique_id = unique_id)

    # Failed
    else:
        return redirect('email-verification-failed')

def email_verification_sent(request):
    email = request.session.get('email')
    return render(request,'account/registration/email-verification-sent.html',{'email':email})

def email_verification_success(request, unique_id):
    user = User.objects.get(pk=unique_id)
    return render(request,'account/registration/email-verification-success.html',{'user':user})

def email_verification_failed(request):
    return render(request,'account/registration/email-verification-failed.html')



def user_login(request):
    
    form = LoginForm()

    if request.method == 'POST':
        
        form = LoginForm(request, data = request.POST)

        if form.is_valid():
            
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                auth.login(request , user)

                return redirect('dashboard')

    context = {'form' : form}

    return render(request, 'account/my-login.html', context=context)


def user_logout(request):
    auth.logout(request)

    messages.success(request,"Logout successful!")

    return redirect("store")

@login_required(login_url = 'user-login')
def dashboard(request):
    return render(request, 'account/dashboard.html')


@login_required(login_url = 'user-login')
def update_account(request):

    user_form = UpdateUserForm(instance=request.user)
    
    # updating username and email
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance = request.user)

        if user_form.is_valid():
            user_form.save()

            messages.info(request,"Account updated")

            return redirect('dashboard')

    

    context = {'user_form':user_form}

    return render(request, 'account/update-account.html',context=context)



@login_required(login_url='user-login')
def delete_account(request):

    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':

        user.delete()

        messages.error(request,"Account deleted")

        return redirect('store')

    

    return render(request, 'account/delete-account.html')


# Shipping view

@login_required(login_url='user-login')
def manage_shipping(request):
    
    try:

        # Account with shipping address
        shipping = ShippingAddress.objects.get(user=request.user.id)

    except ShippingAddress.DoesNotExist:

        # Account with no shipping address
        shipping = None

    form = ShippingForm(instance=shipping)

    if request.method == 'POST':

        form = ShippingForm(request.POST, instance=shipping)

        if form.is_valid():

            # Assign user foreign key

            shipping_user = form.save(commit=False)
            shipping_user.user = request.user

            shipping_user.save()

            return redirect('dashboard')

    context = {'form':form}
    
    return render(request,'account/manage-shipping.html', context=context)

