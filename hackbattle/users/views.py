from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from users.models import Profile,Chat,Hospital,Speciality
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

def aidoctor(request):
    return render(request,'users/ai-doctor.html')

def chatsection(request,pk):
    print(request)
    if request.method=="POST":
        hosp=get_object_or_404(Hospital,id=pk)
        pat=Profile.objects.filter(user=request.user).first()
        msg=request.POST.get("usermessage","")
        if msg!="":
            chat_obj=Chat(hospital=hosp,patient=pat,sender="Patient",message=msg)
            chat_obj.save()
    hosp=get_object_or_404(Hospital,id=pk)
    # pat_id=request.user.id
    pat=Profile.objects.filter(user=request.user).first()
    chats=Chat.objects.filter(hospital=hosp,patient=pat).order_by('date')
    return render(request,'users/chatsection.html',{'hospital':hosp,'chats':chats})


from .forms import HospitalRegisterForm 
# Create your views here.
def register_hospital(request):
	if request.method=='POST':
		form=HospitalRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			messages.success(request, f'YOUR ACCOUNT HAS BEEN CREATED ! YOU CAN NOW LOG IN  {username}!')
			return redirect('login')
	else:
		form=HospitalRegisterForm()
	return render(request, 'hospital/register.html',{ 'form': form })

def home(request):
    return render(request, 'hospital/register.html')

def hospitals(request):
    return render(request, 'hospital/register.html')



