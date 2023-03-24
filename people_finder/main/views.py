from django.shortcuts import render, redirect
from .form import NewUserForm, ProfileForm, SearchForm, SearchTable
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils.crypto import get_random_string
import re
from django.conf import settings
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from main.models import Profile, ListofInterests, Interest
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
import os
from pathlib import Path


def check_valid(request, dic):
    dic = dic.copy()
    dic["email"] = str(dic["email"]).lower()
    if re.fullmatch(".*@uap-bd.edu", dic["email"]):
        return True
    messages.error(
        request,
        mark_safe("Only the users from UAP are allowed. Use your UAP provided e-mail."),
    )
    return False


def confirm_email(email, password):
    body = f"Hello There!\nYour Cerdentials at UAP PEOPLE FINDER\nemail = {email}\npassword = {password}"
    subject = "Your Cerdentials at UAP PEOPLE"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [
        email,
    ]
    send_mail(subject, body, email_from, recipient_list)


# Create your views here.


def signup_request(request):
    if request.method == "POST":
        if check_valid(request, request.POST):
            password = get_random_string(8)
            d = request.POST.copy()
            d["password1"] = password
            d["password2"] = password
            d["username"] = str(d["email"]).lower()
            d["email"] = str(d["email"]).lower()
            request.POST = d
            form = NewUserForm(request.POST)
            if form.is_valid():
                confirm_email(d["email"], password)
                user = form.save()
                Profile.objects.create(username=user, first_name="", last_name="")
                messages.success(
                    request, "An e-mail was sent to you with the credentials!"
                )
            else:
                messages.error(
                    request, mark_safe("An account already exist with this e-mail.")
                )
        return redirect("main:signup")
    form = NewUserForm()
    return render(
        request=request,
        template_name="main/signup.html",
        context={"register_form": form},
    )


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.info(request, "You are now logged in.")
                # needs to be changed to profile page.
                return redirect("main:profile")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="main/login.html", context={"login_form": form}
    )


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:login")


@login_required(login_url="main:login")
def profile_request(request):
    if request.method == "POST":
        d = request.POST
        profile_obj = Profile.objects.get(
            username=User.objects.get(username=str(request.user))
        )
        profile_obj.first_name = d["first_name"]
        profile_obj.last_name = d["last_name"]
        if request.FILES.get("display_picture", None) != None:
            try:
                if 'default.png' not in profile_obj.display_picture.url:
                    os.remove(
                        str(
                            os.path.join(Path(__file__).resolve().parent.parent)
                            + profile_obj.display_picture.url
                        )
                    )
            except Exception as e:
                print("Exception in removing old profile image: ", e)
            profile_obj.display_picture = request.FILES["display_picture"]
        profile_obj.save()
        Interest.objects.filter(
            username=User.objects.get(username=str(request.user))
        ).delete()
        d = d.copy()
        for i in range(1, 4):
            Interest.objects.create(
                username=User.objects.get(username=str(request.user)),
                interest1=d[f"interest_{i}"],
                bio=d[f"interest_{i}_bio"],
                link=d[f"interest_{i}_link"],
            )

        messages.success(request, "Successfully updated profile info!")
        return redirect("main:profile")

    prefill_dict = model_to_dict(
        Profile.objects.get(username=User.objects.get(username=str(request.user)))
    )
    inter = Interest.objects.filter(
        username=User.objects.get(username=str(request.user))
    )

    for i, obj in zip(range(1, 4), inter):
        k = "interest_" + str(i)
        j = "interest_" + str(i) + "_bio"
        l = "interest_" + str(i) + "_link"
        prefill_dict[k] = obj.interest1
        prefill_dict[j] = obj.bio
        prefill_dict[l] = obj.link

    profile_form = ProfileForm(initial=prefill_dict)
    dp_url = prefill_dict["display_picture"].url
    print(dp_url)
    return render(
        request=request,
        template_name="main/profile.html",
        context={"profile_form": profile_form, "dp": dp_url},
    )


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": "103.198.137.87:8000",
                        "site_name": "UAP People finder",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [
                        str(user.email).lower(),
                    ]
                    try:
                        send_mail(subject, email, email_from, recipient_list)
                    except BadHeaderError:
                        messages.error(request, "There was an issue sending the mail.")
                        return redirect("password_reset")
                    messages.success(request, "Success!")
                    return redirect("password_reset_done")

    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="main/password/password_reset.html",
        context={"password_reset_form": password_reset_form},
    )


@login_required(login_url="main:login")
def password_reset_profile_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": "103.198.137.87:8000",
                        "site_name": "UAP People finder",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [
                        str(user.email).lower(),
                    ]
                    try:
                        send_mail(subject, email, email_from, recipient_list)
                    except BadHeaderError:
                        messages.error(request, "There was an issue sending the mail.")
                        return redirect("password_reset")
                    messages.success(request, "Success!")
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm(
        initial={"email": str(request.user).lower()}
    )
    password_reset_form.fields["email"].widget.attrs["readonly"] = True
    return render(
        request=request,
        template_name="main/password/password_reset_profile.html",
        context={"password_reset_form": password_reset_form},
    )


@login_required(login_url="main:login")
def search_request(request):
    search_form = SearchForm()
    if request.method == "POST":
        searchV = request.POST["search_text"]
        searchV = searchV.strip()
        if searchV:
            searchValue = User.objects.filter(email__icontains=searchV)
            if not (searchValue):
                searchValue = Profile.objects.filter(first_name__icontains=searchV)
            if not (searchValue):
                searchValue = Profile.objects.filter(last_name__icontains=searchV)

            tempObj = set()
            for user in searchValue:
                try:
                    obj = Profile.objects.get(username=user)
                    tempObj.add(obj)
                except Exception as msg:
                    print(msg)

            # table = SearchTable(tempObj)
            table = tempObj

            return render(
                request=request,
                template_name="main/search.html",
                context={"search_form": search_form, "table": table},
            )

    return render(
        request=request,
        template_name="main/search.html",
        context={"search_form": search_form},
    )

@login_required(login_url="main:login")
def view_profile(request, profile_id):
    if request.method == "POST":
        #Adding add friend, send message button for future releases.
        pass
    #Creating View Profile Context
    profile_obj = Profile.objects.filter(username=User.objects.filter(id=profile_id)[0])[0]
    d = dict()
    d['first_name'] = profile_obj.first_name
    d['last_name'] = profile_obj.last_name
<<<<<<< Updated upstream
    d['display_picture'] = profile_obj.display_picture


    inter = Interest.objects.filter(
        username=User.objects.get(username=User.objects.filter(id=profile_id)[0])
    )

    for i, obj in zip(range(1, 4), inter):
        k = "interest_" + str(i)
        j = "interest_" + str(i) + "_bio"
        l = "interest_" + str(i) + "_link"
        d[k] = obj.interest1
        d[j] = obj.bio
        d[l] = obj.link

=======
    d['display_picture'] = profile_obj.display_picture.url
>>>>>>> Stashed changes
    return render(request=request,
                    template_name="main/view_profile.html",
                    context={"profile":d},)
