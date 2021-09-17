from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegisterForm, KeywordForm
from .models import UserInfo, Keyword
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime
def home(request):
    return render(request, 'users/home.html')
    
def userRegister(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST,request.FILES)
        #print(form.errors)
        #print(form.is_valid())
        if form.is_valid():
            
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            
            full_name = request.POST['full_name']
            
            email = request.POST['email']
            
            u_name = request.POST['username']
            password = request.POST['password2']
            #p_hash = make_password(password)  ##to make hash password
            #print(uploaded_image)
            userInfo = UserInfo.objects.create(
                                 full_name=full_name, 
                                 
                                 email=email, 
                                 username = u_name 
                                 )
            #userInfo2 = User(username = u_name, email=email, password = p_hash)
            
            userInfo.save()
            #userInfo2.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
        
    return render(request, 'users/userRegister.html', {'form': form})


@login_required
def saveKeyword(request):
   
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        
        if form.is_valid():
            c_user = request.user
            keyword = request.POST['keyword']
            time = datetime.datetime.now()
            time = str(time)
            searchKeyword = Keyword(keyword = keyword, date = time, user = c_user)
            searchKeyword.save()
            
            
            return redirect("https://www.google.com/search?q="+keyword)

    else:
        form = KeywordForm()        

    

    return render(request, 'users/search.html', {'form': form})        

@login_required
def storedKeyword(request):
   
    
    c_user = request.user        
    li1 = []
    dictionary = {}
    obj1 = Keyword.objects.filter(user = c_user)
    for i in obj1:
        li1.append(i.keyword)
    cnt =0 
    temp =0       
    for i in range(0,len(li1)):
        cnt = 0
        for j in range(i,len(li1)):
            
            
            if(li1[i]==li1[j]):
                
                cnt += 1
        if li1[i] in dictionary.keys():
            if (cnt>temp):
                dictionary[li1[i]] = cnt
                temp = cnt;  

        else:
            dictionary[li1[i]] = cnt
            temp = cnt;
    li2 = []
    li3 = []
    li4 = []
    li5 = []
    ans = 0
    for key, value in dictionary.items() :
        #li4.append(str(ans))
        li4.append(ans)
        li2.append(key)
        li3.append(value)
        ans +=1
    for i in range(0,len(li4)):
        i = i+97
        li5.append(chr(i))

    obj2 = Keyword.objects.all()
    li6 = []
    li7 = []
    li8 = []
    li9 = []
    li10 = []
    li11 = []
    temp1 = -1
    x=set()
    mydict = {}
    users = User.objects.all()
    for i in users:
        li10.append(temp1)
        li9.append(i.username)
        temp1-=1
    
    for i in range(0,len(li10)):
        i = 90-i
        li11.append(chr(i))

    for i in users:
        s1=""
        s1= i.username
        
        li7.clear()
        x.clear()
        li6 = Keyword.objects.filter(user = i)
        for j in li6:
            li7.append(j.keyword)
        s1+= " searched this keywords: "
        x.update(li7)
        if(len(x)!=0):
            for d in x:
                s1+=d
                s1+=", "
            li8.append(s1)
        else:
            s2 = i.username+" searched nothing"
            li8.append(s2)    
     
    
         

    return render(request, 'users/searchedKeywords.html', {'context1':li1, 'context2':li2, 
                                                           'context3':li3, 'context4':li4, 
                                                          'context5':li5, 'context8':li8, 
                                                           'context9':li9, 'context10':li10,
                                                           'context11':li11, 'context12':len(li3)})  
