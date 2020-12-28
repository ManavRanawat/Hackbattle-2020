from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import pickle
from . import disease_p,ct_scan,xray
from django.views.generic import CreateView
from django.core.mail import send_mail
from django.urls import reverse_lazy

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

@login_required
def aidoctor(request):
    return render(request,'users/ai-doctor.html')

# def chatsection_user(request,pk):
#     print(request)
#     if request.method=="POST":
#         hosp=get_object_or_404(Hospital,id=pk)
#         pat=Profile.objects.filter(user=request.user).first()
#         msg=request.POST.get("usermessage","")
#         if msg!="":
#             chat_obj=Chat(hospital=hosp,patient=pat,sender="Patient",message=msg)
#             chat_obj.save()
#     hosp=get_object_or_404(Hospital,id=pk)
#     # pat_id=request.user.id
#     pat=Profile.objects.filter(user=request.user).first()
#     chats=Chat.objects.filter(hospital=hosp,patient=pat).order_by('date')
#     return render(request,'users/chatsection_user.html',{'hospital':hosp,'chats':chats})

class ChatSectionUserView(LoginRequiredMixin,CreateView):
    template_name='users/chatsection.html'
    model=Chat
    fields=['message']
    
    def dispatch(self, request, *args, **kwargs):
        print(self.kwargs['usrtype'])
        if request.user.profile.is_hospital and self.kwargs['usrtype']=="hospital":
            return super().dispatch(request, *args, **kwargs)
        elif (not request.user.profile.is_hospital) and self.kwargs['usrtype']=="patient":
            return super().dispatch(request, *args, **kwargs)
        #above condition checks if the user is indeed the respective role he mentioned in the url
        messages.warning(request, f'You are not authorized for that!')
        return redirect('blog-home')

    def get_success_url(self):
        return reverse_lazy('chat', kwargs={'pk': self.kwargs['pk'],'usrtype':self.kwargs['usrtype']})

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["usrtype"]=self.kwargs['usrtype']
        if self.kwargs['usrtype']=="patient": #patient logged in,url me we passed hospital id
            hospId=self.kwargs['pk']
            context['curr_user']=self.request.user
        else: #hospital logged in,url me we passed patient id
            hospId=self.request.user.hospital.id
            uss=User.objects.filter(id=self.kwargs['pk']).first()
            context['curr_user']=uss
        print(hospId,context['usrtype'])
        # print(self.request.GET)
        hosp=get_object_or_404(Hospital,id=hospId)
        print("HI THERE")
        context['hospital']=hosp
        print(hosp.name)
        context['chats']=Chat.objects.filter(hospital=hosp,patient=context['curr_user'].profile).order_by('date')
        return context


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if self.kwargs['usrtype']=="patient": #patient logged in,url me we passed hospital id
            hospId=self.kwargs['pk']
            userID=self.request.user.profile.id
        else: #hospital logged in,url me we passed patient id
            hospId=self.request.user.hospital.id
            uss=User.objects.filter(id=self.kwargs['pk']).first()
            userID=uss.profile.id
        form.instance.hospital=get_object_or_404(Hospital,id=hospId)
        form.instance.patient=get_object_or_404(Profile,id=userID)
        if(self.kwargs['usrtype']=='hospital'):
            form.instance.sender='Hospital'
        else:
            form.instance.sender='Patient'
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

# def chatsection_hospital(request,pk):
#     if request.method=="POST":
#         patient=get_object_or_404(User,id=pk)
#         hosp=request.user.hospital
#         msg=request.POST.get("usermessage","")
#         if msg!="":
#             chat_obj=Chat(hospital=hosp,patient=patient.profile,sender="Hospital",message=msg)
#             chat_obj.save()
#     patient=get_object_or_404(User,id=pk)
#     # pat_id=request.user.id
#     hosp=request.user.hospital
#     chats=Chat.objects.filter(hospital=hosp,patient=patient.profile).order_by('date')
#     return render(request,'users/chatsection_hospital.html',{'patient':patient,'chats':chats})

def patientslist(request):
    chats=Chat.objects.filter(hospital=request.user.hospital)
    users=[]
    for chat in chats:
        if chat.patient not in users:
            users.append(chat.patient)
    return render(request,'users/patientslist.html',{'patients':users})




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

# def home(request):
#     return render(request, 'hospital/register.html')

def dashboard(request):
    hosp = Hospital.objects.all()
    return render(request,'users/hospitals.html',{'hospitals':hosp})


@login_required
def addspeciality(request):  
    if not request.user.profile.is_hospital:
        messages.warning(request, f'You are not authorized for adding speciality!')
        return redirect('hospitals')
    hospital=request.user.hospital
    existing=Speciality.objects.filter(username=hospital)
    aleard_added=[]
    for i in existing:
        aleard_added.append(i.speciality)
    print(aleard_added)
    if request.method=="POST" :
        if  request.POST.get('speciality') not in aleard_added:
            Speciality.objects.create(username=request.user.hospital,speciality=request.POST.get('speciality'))
    spec=SpecialityUpdateForm()
    existing=Speciality.objects.filter(username=hospital)
    return render(request,'users/addspeciality.html',{'existing':existing,'hospital':hospital,'form':spec})



############################

specialist={'Pediatrician':['Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid'],
'Cardiologist':['Chronic cholestasis', 'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia',  'Osteoarthristis', 'Arthritis'],
 'Gynecologist': ['Cervical spondylosis','(vertigo) Paroymsal  Positional Vertigo', 'Urinary tract infection'] ,
  'Internist':['Diabetes ', 'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine', 'hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Alcoholic hepatitis', 'Gastroenteritis', 'Paralysis (brain hemorrhage)'],
  'Dermatologist':['Acne', 'Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Peptic ulcer diseae', 'AIDS'],
  'Family Medicine':['Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)']
  }






d = pickle.load(open('symptoms_label.txt', 'rb'))
arr=d.keys()
a=[]


def disease(request):
    # disease_p.disease()
    result=[]
    if request.method=="POST":
        flag=0
        for i in arr:
            if i in request.POST:
                a.append(i)
                # print("i",i)
        if 'submit' in request.POST:
            flag=1
            
        print(a)
        if flag==1:
            result=disease_p.disease(a)
            if len(a)==0:
                messages.warning(request, f'You have not selected any symptoms!')
                return redirect('disease')
            elif len(a)==1:
                PatientRecord.objects.create(patient=request.user.profile,symptom1=a[0],symptom2=None,symptom3=None,symptom4=None,disease_detected=result[0])
            elif len(a)==2:
                PatientRecord.objects.create(patient=request.user.profile,symptom1=a[0],symptom2=a[1],symptom3=None,symptom4=None,disease_detected=result[0])
            elif len(a)==3:
                PatientRecord.objects.create(patient=request.user.profile,symptom1=a[0],symptom2=a[1],symptom3=a[2],symptom4=None,disease_detected=result[0])
            else:
                PatientRecord.objects.create(patient=request.user.profile,symptom1=a[0],symptom2=a[1],symptom3=a[2],symptom4=a[3],disease_detected=result[0])
            for i in range(0,len(a)):
                print(a)
                a.pop(0)

            
            # return redirect(request,'home_display/disease.html')
    if len(result)==0:  
        return render(request,'users/disease.html',{'arr':arr,'result':result,'a':a})
    else:
        
        res=""
        for i in specialist.keys():
            if result[0] in specialist[i]:
                res=i
                break
        # print("disease ka speciality",res)
        # obj=Speciality.objects.filter(speciality=res)
        # print(obj)
        # arr=obj.values()
        
        return render(request,'users/hospital_recommend.html',{'disease':result[0],'specialist':res})

class CTCreateView(LoginRequiredMixin, CreateView):
    model = ScanCT
    fields = ['ct_scan']
    # template_name = 'users/scan_ct.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        # print(form.instance.image_ct.url)
        return super().form_valid(form)

class XrayCreateView(LoginRequiredMixin, CreateView):
    model = ScanXRay
    fields = ['xray']
    # template_name = 'users/scan_xray.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        # print(form.instance.image_ct.url)
        return super().form_valid(form)

def report_ct(request):
    report=ScanCT.objects.filter(user=request.user).last()
    res=ct_scan.predict_ct(report.ct_scan.url)
    return render(request,'users/ct_report.html',{'result':res})

def report_xray(request):
    report=ScanXRay.objects.filter(user=request.user).last()
    res=ct_scan.predict_ct(report.xray.url)
    return render(request,'users/xray_report.html',{'result':res})


def hospital_recommend(request):
    print("recommend me aa raha hai")
    return render(request,'users/hospital_recommend.html')
#     # disease=PatientRecord.objects.filter(user=request.user).last()
#     # res=""
#     # for i in specialist.keys():
#     #     if disease in specialist[i]:
#     #         res=i
#     #         break
#     # print(res)


def suggestedspecialist(request,specialist):
    hospitalspecialities=Speciality.objects.filter(speciality=specialist)
    hospitals=[]
    for i in hospitalspecialities:
        hospitals.append(i.username)
    print(hospitals)
    if request.method=="POST":
        for hosp in hospitals:
            if hosp.name in request.POST:
                Appointment.objects.create(hname=hosp,patient=request.user.profile)
                messages.success(request, f'Appointment confirmed at hospital {hosp.name}!!')
                print('EMAILLLLLLLLLLLL')
                print(request.user.email+"  "+hosp.email)
                # sending mail to both
                body='You have an appointment from '+request.user.username
                send_mail('New Appoinment!',body,'submissionspit@gmail.com',[hosp.email])
                body='You have booked an appointment for '+hosp.name
                send_mail('Appointment Confirmation!',body,'submissionspit@gmail.com',[request.user.email])
                return redirect('blog-home')
    print(hospitals)
    return render(request,'users/bookappointment.html',{'hospitals':hospitals})



    #  Pediatrician ->
    # 'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid',

    # Cardiologist->
    # 'Chronic cholestasis', 'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia',  'Osteoarthristis', 'Arthritis',

    # Gynecologist->
    # 'Cervical spondylosis','(vertigo) Paroymsal  Positional Vertigo', 'Urinary tract infection',

    # Internist->
    # 'Diabetes ', 'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine', 'hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Alcoholic hepatitis', 'Gastroenteritis', 'Paralysis (brain hemorrhage)'

    # Dermatologist->
    # 'Acne', 'Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Peptic ulcer diseae', 'AIDS'

    # Family Medicine->
    # 'Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',

def records(request):
    user=request.user
    appointments=Appointment.objects.filter(patient=user.profile)
    return render(request,'users/records.html',{'appointments':appointments})