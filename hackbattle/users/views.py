from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm,HospitalUpdateForm
from .models import Profile,Chat,Hospital,Speciality
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            curr_user = User.objects.filter(username=form.cleaned_data.get('username')).first()
            is_hosp=form.cleaned_data.get('is_hospital')
            obj=Profile.objects.create(user=curr_user,is_hospital=is_hosp)
            if is_hosp:
                Hospital.objects.create(user=curr_user,email=form.cleaned_data.get('email'))
            # obj.save()
            print("SAVED")
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    prof=Profile.objects.filter(user=request.user).first()
    print(prof.is_hospital)
    if request.method == 'POST':
        if prof.is_hospital==True:
            print("HOSPITAL")
            h_form=HospitalUpdateForm(request.POST,instance=request.user.hospital)
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            if prof.is_hospital and h_form.is_valid():
                h_form.save()
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('profile')
            elif not prof.is_hospital:    
                u_form.save()
                # print()
                # Hospital.objects.filter(uid=)
                # print()
                # fields=['name','email','description','phone_no']
                # hosp_obj=Hospital()
                # hosp_obj.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('profile')
    else:
        if prof.is_hospital==True:
            h_form=HospitalUpdateForm(instance=request.user.hospital)
            print("HERE IN")
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    if prof.is_hospital:
        context['h_form']=h_form
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



# Create your views here.
# def register_hospital(request):
# 	if request.method=='POST':
# 		form=HospitalRegisterForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			username=form.cleaned_data.get('username')
# 			messages.success(request, f'YOUR ACCOUNT HAS BEEN CREATED ! YOU CAN NOW LOG IN  {username}!')
# 			return redirect('login')
# 	else:
# 		form=HospitalRegisterForm()
# 	return render(request, 'hospital/register.html',{ 'form': form })

def home(request):
    return render(request, 'hospital/register.html')

def dashboard(request):
    hosp = Hospital.objects.all()
    return render(request,'users/dashboard.html',{'hospitals':hosp})



