from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegisterForm, KeywordForm, DateForm
from .models import UserInfo, Keyword, SearchedDate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime
from datetime import date
def home(request):
    #This view function is responsible for home url. 

    return render(request, 'users/home.html')
    
def userRegister(request):
    #This view function is responsible for sign up url.

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

def returnCurrentDate():
    #This function returns the current method 

    time = datetime.datetime.now()
    time = str(time)
    return time

def convertDate(date):
    #This function takes a date parameter and converts it to integer type.
    #Example: 2019-06-15 17:56.234 to 20190615
    
    time1=""
    for i in date:

        if(ord(i)==32):
            break
        else:
            if(ord(i)!=45):
                time1+=i
                   
   
    time1 = int(time1)
    return time1

def splitmonthfromDate(date):
    #This function takes a date parameter splits month from date and return month 
    #Example: 2019-06-15  to 06
    date = str(date)
    month = date[4] + date[5]
    return month

def monthCalculator(date):
    #This function returns the first and last date of previous month
    #Example: 2019-06-15 , returns 2019-05-01 and 2019-05-31
    mydict = {
        '1':31,
        '2':28,
        '3':31,
        '4':30,
        '5':31,
        '6':30,
        '7':31,
        '8':31,
        '9':30,
        '10':31,
        '11':30,
        '12':31
        }
    date = str(date)
    day = date[6] + date[7]
    
    month = date[4] + date[5]
    year = date[0]+date[1]+date[2]+date[3]
    day = int(day)
    month = int(month)
    month = month - 1
    month = str(month)
    day = str(day)
    dayFirst = "01"
    dayLast = mydict.get(month)
    if(len(month)!=2):
        month = '0'+month
    dayLast = str(dayLast)         
    date1st = year+month+dayFirst
    dateLast = year+month+dayLast
    li = []
    li.append(date1st)
    li.append(dateLast)
    return li   

def weekCalculator(date):
    #This function returns the first and last date of previous week
    #Example: 2019-06-15 , returns 2019-06-08 and 2019-06-01
    mydict = {
        '1':31,
        '2':28,
        '3':31,
        '4':30,
        '5':31,
        '6':30,
        '7':31,
        '8':31,
        '9':30,
        '10':31,
        '11':30,
        '12':31
        }
    date = str(date)
    day = date[6] + date[7]
    
    month = date[4] + date[5]
    year = date[0]+date[1]+date[2]+date[3]
    day = int(day)
    month = int(month)
    temp = day - 7
    if(temp<=0):
        month = month - 1
        month = str(month)
        day = mydict.get(month) + day - 7
    else:
        day = temp
    month = str(month)
    day = str(day)
    if(len(month)!=2):
        month = '0'+month
    if(len(day)!=2):
        day = '0'+day         
    date1 = year+month+day

    return date1 

def dayCalculator(date):
     #This function returns the date of previous day
    #Example: 2019-06-15 , returns 2019-06-14 
    mydict = {
        '1':31,
        '2':28,
        '3':31,
        '4':30,
        '5':31,
        '6':30,
        '7':31,
        '8':31,
        '9':30,
        '10':31,
        '11':30,
        '12':31
        }
    date = str(date)
    day = date[6] + date[7]
    month = date[4] + date[5]
    year = date[0]+date[1]+date[2]+date[3]
    day = int(day)
    month = int(month)
    day = day - 1
    if(day == 0):
        month = month -1
        month = str(month)
        day = mydict.get(month)
    else:
        day = day

    month = str(month)
    day = str(day)
    if(len(month)!=2):
        month = '0'+month
    if(len(day)!=2):
        day = '0'+day         
    date1 = year+month+day

    return date1 
       


@login_required
def saveKeyword(request):
   #This function is responsible for saving keywords which user searchs
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        
        if form.is_valid():
            c_user = request.user
            keyword = request.POST['keyword']
            a = returnCurrentDate()
            a = convertDate(a)
            
            #time = datetime.datetime.now()
            #time = str(time)
            searchKeyword = Keyword(keyword = keyword, date = a, user = c_user)
            searchKeyword.save()
            
            
            return redirect("https://www.google.com/search?q="+keyword) #Takes to the google's searched page

    else:
        form = KeywordForm()        

    

    return render(request, 'users/search.html', {'form': form})        

@login_required
def storedKeyword(request):
   #This function is responsible for performs various operation on search history page
    
    c_user = request.user   #get the current user     
    li1 = []      # this list contains a keyword's total search count
    dictionary = {} # this dictionaries key is the keyword and value is the total number of search
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
    li4 = [] # this list contains unique id for dom elements
    li5 = [] # this list contains unique id for dom elements
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
    #From this below line portion 
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
    # to this upper this portion is responsible for the keywords searched by each user
    
    #From this below line portion
    c_time = returnCurrentDate()
    c_time = convertDate(c_time)
    p_day = dayCalculator(c_time)
    
    last_week_1st = weekCalculator(c_time)
    last_week_2nd = weekCalculator(last_week_1st)
    
    previous_post = Keyword.objects.filter(date = p_day)
    
    li12 = []
    y = set()
   
    for i in previous_post:
        
        if(i.user==c_user):
            li12.append(i.keyword)
       
           
        y.update(li12)
    s2 = ""
    
    if(len(y)==0):
        s2+="nothing"
    else:

        for i in y:
            s2+=i
            s2+=','

    
    li13 = []
    showDate=""
    s3 = ""
    z = set()
    for i in obj2:
        if(i.user == c_user):
            
            showDate = int(i.date)
            
            if(showDate>=int(last_week_2nd) and showDate<=int(last_week_1st)):
                li13.append(i.keyword)
            z.update(li13)    
    if(len(z)==0):
        s3+="nothing"
    else:

        for i in z:
            s3+=i
            s3+=','
            s3+=' '
    li14 = []
    li14 = monthCalculator(c_time)        
    dateFirst = li14[0]
    dateLast = li14[1]
    
    #splitmonthfromDate(dateFirst)
    
    #print(dateFirst))
    #print(dateLast)

    li15 = []
    showDate1=""
    s4 = ""
    z1 = set()
    for i in obj2:
        if(i.user == c_user):
            
            showDate1 = int(i.date)
            
            if(showDate1>=int(dateFirst) and showDate1<=int(dateLast)):
                li15.append(i.keyword)
            z1.update(li15) 
             
    if(len(z1)==0):
        s4+="nothing"
    else:

        for i in z1:
            s4+=i
            s4+=','
            s4+=' '

    li16 = []
    z12 = set()
   #To this upper line portion is responsible for yesterday, last week, last months searched keyword by current user
    
    #From this below portion 
    startDate = ""
    endDate = ""  
    t1 = 0
    t2 = 0
    
    if request.method == 'POST':
        form = DateForm(request.POST)
       
        if form.is_valid():
            startDate = convertDate(request.POST['startdate'])
            endDate = convertDate(request.POST['enddate'])
            sD = SearchedDate(startDate=startDate, endDate=endDate)
            sD.save()
            return redirect('date')
        else:
            
            messages.error(request, "Date should be like Year-Month-day")
            form = DateForm()       

    else:
        form = DateForm()  
    
   
     
    
    #for j in obj2:
        #if(j.user == c_user):
            #t3 = int(j.date)
            #if(t3>=int(t1) and t3<=int(t2)):
                #li16.append(j.keyword)
   
    #To this up line portion is responsible for showing the searched keyword by current user
    # between two dates. Everything is perfect but this block is not working


    return render(request, 'users/searchedKeywords.html', {'context1':li1, 'context2':li2, 
                                                           'context3':li3, 'context4':li4, 
                                                          'context5':li5, 'context8':li8, 
                                                           'context9':li9, 'context10':li10,
                                                           'context11':li11, 'context12':len(li3),
                                                           'context13':s2, 'context14':s3,
                                                           'context15':s4, 'form': form
                                                           })  


def specificKeywordwithDate(request):
    #This function fetches the searched keyword between two dates
    a1 = SearchedDate.objects.last()
    t1 = a1.startDate
    t2 = a1.endDate
    
    li1 = []
    z1 = set()
    s4=""
    c_user = request.user
    obj2 = obj2 = Keyword.objects.all()
    for j in obj2:
        if(j.user == c_user):

            t3 = int(j.date)
            
            if(t3>=int(t1) and t3<=int(t2)):
                
                li1.append(j.keyword)
            z1.update(li1) 

    if(len(z1)==0):
        s4+="nothing"
    else:

        for i in z1:
            s4+=i
            s4+=','
            s4+=' '            

    return render(request, 'users/dateKeywords.html', {'context16':s4})
