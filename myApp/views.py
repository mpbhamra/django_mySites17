from django.shortcuts import render,render_to_response
from django.http import  HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from pip._vendor.requests.api import request

from myApp.models import  Author, Book,Course,Topics,Student,ImagesTable
from myApp.forms import TopicForm, InterestForm, RegisterForm, UploadImageForm
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

# Create your views here.
def hello(request):
    return render(request,"mysite17/templates/test1.html",{})
def index (request):
    if (request.user.is_authenticated()):
        testuser = request.user;

    else:
        testuser = ""


    courselist = Course.objects.all()[:10];

    if 'counter' in request.COOKIES:
        counter = request.COOKIES['counter']
        counter = int(counter)
        counter +=1
        counter = str(counter)
        response = render(request, 'myapp/index.html', {'courselist': courselist, 'testuser': testuser,})
        response.set_cookie('counter', str(counter));
        return response
    else:
        response = render(request, 'myapp/index.html', {'courselist': courselist, 'testuser': testuser})
        counter = counter = str(1)
        response.set_cookie('counter', counter);
        return response

    '''response = HttpResponse();
    heading= '<p>'+'List of Courses'+'</p>'
    response.write(heading)
    for course in courselist:
        para = '<p>'+str(course)+'</p>'
        response.write(para);

    authorlist = Author.objects.order_by('birthdate').reverse()[:5]
    heading2 = '<p>' + 'List of Authors' + '</p>'
    response.write(heading2)
    for author in authorlist:
        para = '<p>Firstname: '+str(author.firstname) + ',   Birthdate: '+ str(author.birthdate) + '</p>'
        response.write(para);

    return (response)'''

    return render(request, 'myapp/index.html', {'courselist': courselist,'testuser':testuser})
def about(request):
    if (request.user.is_authenticated()):
        testuser = request.user;
    else:
        testuser = ""

    ''' response = HttpResponse();
    msg = '<p>“This is a Course Listing APP.” </p>'
    response.write(msg)
    return(response) '''
    return render(request, 'myapp/about.html',{'testuser':testuser})

def detail(request,course_no):
    courselist = Course.objects.get(course_no=course_no);
    '''response = HttpResponse()
    title = str(courselist.title)'''

    '''textbook = str(courselist.textbook)
    resmsg = '<p> the '+crs_no+' is named as '+title+' and has '+textbook+' as a reference book</p>'
    response.write(resmsg)
    return(response)'''
    return render(request,'myapp/detail.html',{'courselist':courselist})

def topic(request):
    if(request.user.is_authenticated()):
        testuser = request.user;
    else:
        testuser = ""

    topiclist = Topics.objects.all()[:10]
    return render(request, 'myapp/topic.html', {'topiclist':topiclist,'testuser':testuser})

    '''form=TopicForm(request.POST)
    return render(request,'myapp/post_edit.html',{'form':form})'''


def addtopic(request):
    if (request.user.is_authenticated()):
        testuser = request.user;
    else:
        testuser = ""

    topiclist = Topics.objects.all()
    if(request.method=='POST'):
        form = TopicForm(request.POST)
        if(form.is_valid()):
            topic = form.save(commit=False)
            topic.num_responses = 1
            topic.save()
            return HttpResponseRedirect('/myApp/topic')
    else:
        form = TopicForm()
        return render(request, 'myapp/addtopic.html',{'form':form, 'topiclist':topiclist,'testuser':testuser})


def topicdetail(request, topic_id):
    if (request.user.is_authenticated()):
        testuser = request.user;
    else:
        testuser = ""

    topicdetails = Topics.objects.get(id = topic_id)
    if(request.method=='POST'):
        form = InterestForm(request.POST)
        if(form.is_valid()):
            if(request.POST['interested'] == '1'):
                topicdetails.num_responses += 1;
                avg_age = (topicdetails.avg_age + int(request.POST['age']))/2
                topicdetails.avg_age = avg_age
                topicdetails.save()
        return render(request, 'myapp/topicdetail.html', {'topicdetails': topicdetails, 'form':form, 'testuser': testuser})
    else:
        form = InterestForm()
        return render(request, 'myapp/topicdetail.html', {'topicdetails': topicdetails, 'form':form, 'testuser':testuser})

def register(request):
    if (request.user.is_authenticated()):
        testuser = request.user;
        msg = "You are already registered"
    else:
        testuser = ''
        msg= ''

    #newstudent = Student.objects.all()
    if (request.method == 'POST'):
        form = RegisterForm(request.POST,request.FILES)
        if (form.is_valid()):
            newstudents = form.save(commit=False)
            newstudents.save()
            newstudents.set_password(newstudents.password)
            newstudents.save()
            return HttpResponseRedirect('/myApp/register',{'form':form, 'testuser': testuser,'msg':msg})
    else:
        form = RegisterForm()
        return render(request, 'myapp/register.html',{'form':form, 'testuser': testuser,'msg':msg})

def user_login(request):


    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        std = Student.objects.filter(username = username)
        user = authenticate(username=username,password=password)
        if(user):
            if(user.is_active):
                login(request,user)
                return HttpResponseRedirect(reverse('myApp:index'))
            else:
                return HttpResponseRedirect('Your Account is Disabled')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myApp:index')))

def mycourses(request):

    if (request.user.is_authenticated()):
        testuser = request.user;
    else:
        testuser = ""

    mycourse = Course.objects.filter(students__username = testuser)
    return render(request, 'myapp/mycourses.html',{'mycourse':mycourse, 'testuser':testuser})

def upload_form(request):
    saved  = False;
    if (request.user.is_authenticated()):
        testuser = request.user;
    else:
        testuser = ""

    if(request.method == 'POST'):
        form = UploadImageForm(request.POST,request.FILES)
        if(form.is_valid):
            imagestable = ImagesTable()
            usr = Student(testuser)
            imagestable.student = testuser
            imagestable.title = form['title']
            imagestable.picture = form['imgfile']
            imagestable.save()
            saved = True
            return HttpResponseRedirect(reverse('myApp:upload'), {'form': form, 'saved': saved})
    else:
        form = UploadImageForm()
        return render(request, 'myapp/upload.html', {'form': form, 'saved':saved})
def forgotpass(request):
    email = request.POST['email']
    passwords = Student.objects.get(email= email)

    send_mail('this is your password','this is your password {0}'.format(passwords.password),'kishan.krishna.patel44@gmail.com',email, fail_silently=False)
    return render(request, 'myapp/forgotpass.html')
