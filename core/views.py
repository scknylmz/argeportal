from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.http import JsonResponse
from .forms import PersonelForm,NewsForm, ProjectsForm, AdamAyForm, IsPaketiekleForm, ArgetesvikForm, PatentekleForm, BildiriekleForm
from .models import Personel, News, Projects, DepartmentList, IsPaketiekle, AdamAy, ArgeTesvik, Patent, Bildiri
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv,datetime,xlwt
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Sum, F, Case, When, IntegerField, ExpressionWrapper, CharField
from django.db.models.functions import TruncMonth, TruncYear, TruncQuarter
from datetime import timedelta
from django.forms import modelformset_factory
import math, copy
from copy import deepcopy
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.template.defaulttags import register
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 



# Create your views here.
"""def index(request):
    news = News.objects.all()
    news1 = news.order_by('updateDate')[0]
    news2 = news.order_by('updateDate')[1]
    news3 = news.order_by('updateDate')[2]
    news4 = news.order_by('updateDate')[3]
    news5 = news.order_by('updateDate')[4]
    news6 = news.order_by('updateDate')[5]
    
    context = {
        "news" : news,
        "news1" : news1,
        "news2" : news2,
        "news3" : news3,
        "news4" : news4,
        "news5" : news5,
        "news6" : news6,
    }

    a= news.order_by('updateDate')[5]
    print(a)
    
    for x in a:
        d =x.title
        print(d)

    return render(request, 'core/index.html',context)"""

def index(request):
    today=datetime.date.today()
    personels_active=Personel.objects.filter(rdfinisDate__isnull=True)
    projects_active=Projects.objects.filter(ProjeDurumu=1)
    projects_finished=Projects.objects.filter(ProjeDurumu=2)
    projects_national=Projects.objects.filter(UlusalDestek=True)
    harcama = ArgeTesvik.objects.aggregate(outcome=Sum('argetotal'), income=Sum('hibe'), totaltesvik=Sum('ayliktesviktoplam'), avrtesvik=Avg('ayliktesvikyuzde'))
    argetesvik=ArgeTesvik.objects.all()
    argetesvik_thisyear=ArgeTesvik.objects.filter(date__year__gte=today.year)
    argetesvik_last3year=ArgeTesvik.objects.filter(date__year__gte=today.year-2)
    personel_dep = Personel.objects.filter(rdfinisDate__isnull=True).values('department','department__name').annotate(Count('department'))
    
    # Fikri Hak Dağılımı Chart
    fikrihak = Patent.objects.values('model').annotate(Count('model'))
    for i in fikrihak:
        i['model_display']=Patent(model=i['model']).get_model_display()
    
    # Yayın / Bildiri Chart
    bildiri = Bildiri.objects.values('typ').annotate(Count('typ'))
    for i in bildiri:
        i['bildiri_display']=Bildiri(typ=i['typ']).get_typ_display()
    print(bildiri)

    # Cinsiyet Dağılımları Chart
    personel_gender = Personel.objects.filter(rdfinisDate__isnull=True).values('gender').annotate(Count('gender'))
    for sex in personel_gender:
        sex['gender_display']=Personel(gender=sex['gender']).get_gender_display()
    

    # Görev Dağılımları Chart
    personel_respons = Personel.objects.filter(rdfinisDate__isnull=True).values('respons').annotate(Count('respons'))
    for respons in personel_respons:
        respons['respons_display'] = Personel(respons=respons['respons']).get_respons_display()
    
    # Eğitim Dağılımları Chart
    personel_education = Personel.objects.filter(rdfinisDate__isnull=True).values('graduated').annotate(Count('graduated'))
    for education in personel_education:
        education['education_display']=Personel(graduated=education['graduated']).get_graduated_display()
    
    context = {
        "personels_active" : personels_active,
        "projects_active" : projects_active,
        "projects_finished" : projects_finished,
        "projects_national" : projects_national,
        "harcama" : harcama,
        "argetesvik" : argetesvik,
        "argetesvik_thisyear" : argetesvik_thisyear,
        "personel_dep" : personel_dep,
        "personel_gender" : personel_gender,
        "personel_respons" : personel_respons,
        "personel_education" : personel_education,
        "argetesvik_last3year" : argetesvik_last3year,
        "fikrihak" : fikrihak,
        "bildiri" : bildiri,
    }

    return render(request, 'core/index.html',context)

def argetesvik(request):
    today=datetime.date.today()
    harcama = ArgeTesvik.objects.aggregate(outcome=Sum('argetotal'), income=Sum('hibe'), totaltesvik=Sum('ayliktesviktoplam'), avrtesvik=Avg('ayliktesvikyuzde'))
    argetesvik_last=ArgeTesvik.objects.filter(date__year=today.year)
    argetesvik_last1=ArgeTesvik.objects.filter(date__year=today.year - 1)
    argetesvik_last3=ArgeTesvik.objects.filter(date__year__gte=today.year - 2)
    tesvikverileri = ArgeTesvik.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(tesvikverileri, 10)
    try:
        tesvikverileri = paginator.page(page)
    except PageNotAnInteger:
        tesvikverileri = paginator.page(1)
    except EmptyPage:
        tesvikverileri = paginator.page(paginator.num_pages)

    
    context = {
        "harcama" : harcama,
        "argetesvik_last" : argetesvik_last, 
        "argetesvik_last1" : argetesvik_last1,
        "argetesvik_last3" : argetesvik_last3,
        "tesvikverileri" : tesvikverileri,
    }
    return render(request,"core/argetesvik.html", context)

def argetesvikekle(request):
    if request.method == 'POST':
        form = ArgetesvikForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Kayıt Başarılı')
            return redirect('core:argetesvik')
    else:
        form = ArgetesvikForm()
        return render(request, "core/argetesvikekle.html", {"form":form})

def argetesvikduzenle(request, id):
    instance = get_object_or_404(ArgeTesvik, id=id)
    if request.method == 'POST':
        form = ArgetesvikForm(request.POST, instance = instance)
        if form.is_valid():
            form.save()
            messages.success(request,'Teşvik Verilerinin Güncellemesi Başarılı')
            return redirect('core:argetesvik')
    else:
        form = ArgetesvikForm(instance=instance)
        return render(request, 'core/argetesvikduzenle.html', {"form":form, "id":id})
    
def argetesviksil(request, id):
    deletedobject = ArgeTesvik.objects.get(id=id)
    deletedobject.delete()
    messages.success(request,"Kayıt Başarıyla Silindi")
    return redirect('core:argetesvik')

# --PATENT--FİKRİ MULKIYET--
def patent(request):
    patent = Patent.objects.all()
    bildiri = Bildiri.objects.all()
    patenBasvur = Patent.objects.filter(model=1,apldate__isnull=False).values('area').annotate(Count('area'))
    patenTescil = Patent.objects.filter(model=1,apldate__isnull=False, aprdate__isnull=False).values('area').annotate(Count('area'))
    modelBasvur = Patent.objects.filter(model=2,apldate__isnull=False).values('area').annotate(Count('area'))
    modelTescil = Patent.objects.filter(model=2,apldate__isnull=False, aprdate__isnull=False).values('area').annotate(Count('area'))
    bildiriTescil = Bildiri.objects.values('area').annotate(Count('area'))
    patentsum = Patent.objects.annotate(year=TruncYear('apldate')).values('year').annotate(ulusalp=Sum(Case(When(area=1, model=1, then=1),output_field=IntegerField())),uluslararasip=Sum(Case(When(area=2, model=1, then=1), output_field=IntegerField())),ulusalm=Sum(Case(When(area=1, model=2, then=1),output_field=IntegerField())),uluslararasim=Sum(Case(When(area=2, model=2, then=1), output_field=IntegerField())))
    bildirisum = Bildiri.objects.annotate(year=TruncYear('pubdate')).values('year').annotate(ulusalm=Sum(Case(When(area=1, typ=0, then=1),output_field=IntegerField())),uluslararasim=Sum(Case(When(area=2, typ=0, then=1), output_field=IntegerField())),ulusalb=Sum(Case(When(area=1, typ=1, then=1),output_field=IntegerField())),uluslararasib=Sum(Case(When(area=2, typ=1, then=1), output_field=IntegerField())),ulusalp=Sum(Case(When(area=1, typ=1, then=1),output_field=IntegerField())),uluslararasip=Sum(Case(When(area=2, typ=2, then=1), output_field=IntegerField())))
    page = request.GET.get('page', 1)
    paginator = Paginator(patent, 5)
    try:
        patent = paginator.page(page)
    except PageNotAnInteger:
        patent = paginator.page(1)
    except EmptyPage:
        patent = paginator.page(paginator.num_pages)

    context={
        "patent" : patent,
        "bildiri" : bildiri,
        "patenBasvur" : patenBasvur,
        "patenTescil" : patenTescil,
        "modelBasvur" : modelBasvur,
        "modelTescil" : modelTescil,
        "bildiriTescil" : bildiriTescil,
        "patentsum" : patentsum,
        "bildirisum" : bildirisum,
    }
    return render(request,"core/fikrimulkiyet.html", context)

def patentekle(request):
    form = PatentekleForm()
    if request.method=='POST':
        form = PatentekleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Patent/Faydalı Model Kaydı Başarılı')
            return redirect('core:patent')
        else:
            messages.warning(request,'Kayıt Başarısız')
            return redirect('core:patentekle')
    else:
        return render(request, 'core/patentekle.html', {"form" : form})

def patentduzenle(request, id):
    instance = get_object_or_404(Patent, id=id)
    if request.method=='POST':
        form = PatentekleForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request,'Düzenleme Başarılı')
            return redirect('core:patent')
        else:
            messages.warning(request, 'Düzenleme Başarısız')
    else:
        form = PatentekleForm(instance=instance)
        return render(request,'core/patentduzenle.html', {"form" : form, "id" : id})

def patentsil(request, id):
    deletedobject = Patent.objects.get(id=id)
    deletedobject.delete()
    messages.success(request,'Kayıt Başarıyla Silindi')
    return redirect('core:patent')
    
    # -BİLDİRİ-

def bildiriekle(request):
    if request.method=='POST':
        form = BildiriekleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Kayıt Başarılı')
            return redirect('core:patent')
        else:
            messages.warning(request,'kayıt Başarısız')
    else:
        form = BildiriekleForm()
        return render(request,'core/bildiriekle.html', {"form" : form})

def bildiriduzenle(request, id):
    instance = get_object_or_404(Bildiri, id=id)
    if request.method=='POST':
        form = BildiriekleForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request,'Güncelleme Başarılı')
            return redirect('core:patent')
        else:
            messages.warning(request,'Güncelleme Başarısız')
    else:
        form = BildiriekleForm(instance=instance)
        return render(request,'core/bildiriduzenle.html', {"form": form, "id":id})

def bildirisil(request, id):
    deletedobject = Bildiri.objects.get(id=id)
    deletedobject.delete()
    messages.success(request,'Bildiri Başarıyla Silindi')
    return redirect('core:patent')

# --PERSONEL--
def personelMain(request):

    keyword = request.GET.get("keyword")
    print(keyword)

    if keyword:
        personels = Personel.objects.filter(name__contains = keyword)
        
        context = {
            "personels" : personels
        }

        return render(request, 'core/personelmain.html', context)
    
    personels = Personel.objects.order_by('name')
    personels_active=Personel.objects.filter(rdfinisDate__isnull=True)
    context = {
        "personels" : personels,
        "personels_active" : personels_active,
    }
    return render(request, 'core/personelmain.html', context)

@login_required(login_url="user:login")
def addPersonel(request):
        form = PersonelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request,"Kayıt Başarılı")
            return redirect('core:personelmain')
        return render(request, 'core/addpersonel.html', {"form":form})

@login_required(login_url="user:login")
def addNews(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Kayıt Başarılı")
            return redirect('core:news')
    else:
        form = NewsForm()
    return render(request, 'core/addnews.html', {"form":form})

@login_required(login_url="user:login")
def personelDetail(request, id):
    #print(id)
    person= Personel.objects.get(id=id)
    manmonth = AdamAy.objects.filter(projeAdamAy_id__id = id, tarih__isnull=True).values('projeAdamAy').annotate(total=Count('projeKodu_id'))
    manmonthsum = AdamAy.objects.filter(projeAdamAy_id__id = id).aggregate(Sum('adamAylar'))
    # person = Personel.objects.all()
    # a = person.order_by('id')[0]
    print(manmonth)
    context = {
        "person" : person,
        "manmonth" : manmonth,
        "manmonthsum" : manmonthsum,
    }
    return render(request,"core/detailperson.html", context)

@login_required(login_url="user:login")
def personelUpdate(request,id):
    person = get_object_or_404(Personel, id=id)
    if request.method=='POST':
        form = PersonelForm(request.POST, request.FILES, instance=person)
        context ={
            'form':form,
            'person':person
        }
        if form.is_valid():
            form.save()
            context ={
                'form':form,
                'person':person
            }
            return redirect('core:personelmain')
        else:  
            return render (request, 'core/updatepersonel.html', context)
    else:
        form = PersonelForm(instance=person)
        context={
            'form':form,
            'person':person
        }
        return render(request,'core/updatepersonel.html' , context)

@login_required(login_url="user:login")
def updateNews(request, id):
    news = get_object_or_404(News, id=id)
    if request.method=='POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        context ={
            'form':form
        }
        if form.is_valid():
            form.save()
            context ={
                'form':form
            }
            return redirect('core:news')
        else:  
            return render (request, "core/updatenews.html", context)
    else:
        form = NewsForm(instance=news)
        context={
            'form':form
        }
        return render(request,'core/updatenews.html' , context)

def news(request):
    keyword = request.GET.get("keyword")
    print(keyword)

    if keyword:
        news = News.objects.filter(body__contains = keyword)
        
        context = {
            "news" : news
        }
        
        return render(request, 'core/news.html',context)
    
    news = News.objects.all()
    context = {
        "news":news
    }
    return render(request,'core/news.html',context)

def newsDetail(request,id):
    news = get_object_or_404(News,id=id)
    context = {
        "news" : news
    }
    return render(request,'core/newsdetail.html',context)

@login_required(login_url="user:login")
def deleteNews(request,id):
    news = get_object_or_404(News, id = id)
    news.delete()

    messages.success(request,"Haber Silindi")

    return render(request,'core/news.html')

@login_required(login_url="user:login")
def exportPersonel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Personel_List.xls"'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Ad','Soy Ad','Email','Cinsiyet','Doğum Tarihi', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        
    font_style = xlwt.XFStyle()

    rows = Personel.objects.all().values_list('name','surName','email','gender','birthDay')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
        
    wb.save(response)
    return response


@login_required(login_url="user:login")
def exportPerson(request,id):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Personel_Detay.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('User')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Ad','Soy Ad','Email','Cinsiyet','Doğum Tarihi', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        
    font_style = xlwt.XFStyle()

    rows = Personel.objects.filter(id=id).values_list('name','surName','email','gender','birthDay')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
        
    wb.save(response)
    return response

def chartPersonel(request):
    def getKey(dict):
        list=[]
        for i in dict.keys():
            list.append(i)
        return list

    def getValue(dict):
        list=[]
        for i in dict.values():
            list.append(i)
        return list

    query_all=Personel.objects.all()
    queryset = Personel.objects.filter(rdfinisDate__isnull=True)
    queryset_start = Personel.objects.filter(rdStartDate__lte=("2018-1-1"))
    female=[]
    male=[]

    for i in queryset:
        if i.gender == 1:
            male.append(i.name)
        else:
            female.append(i.name)

    label_gender = ['Erkek', 'Kadın']
    data_gender = [len(male),len(female)]
    
    respons={}
    list=range(1,4)
    for i in list:
        x = queryset.filter(respons=i)
        if i == 1:
            respons['Araştırmacı']=len(x)
        if i == 2:
            respons['Teknisyen']=len(x)
        if i ==3:
            respons['Destek Personeli']=len(x)
    label_respons=getKey(respons)
    data_respons=getValue(respons)

    gradic={}
    list=range(0,11)
    for i in list:
        x = queryset.filter(graduated=i)
        if i == 0:
            gradic['Diğer']=len(x)
        if i == 1:
            gradic['Lise']=len(x)
        if i == 2:
            gradic['Lise (Öğrenci)']=len(x)
        if i == 3:
            gradic['Ön Lisans']=len(x)
        if i == 4:
            gradic['Ön Lisans (Öğrenci)']=len(x)
        if i == 5:
            gradic['Lisans']=len(x)
        if i == 6:
            gradic['Lisans (Öğrenci)']=len(x)
        if i == 7:
            gradic['Yüksek Lisans']=len(x)
        if i == 8:
            gradic['Yüksek Lisans (Öğrenci)']=len(x)
        if i == 9:
            gradic['Doktora']=len(x)
        if i == 10:
            gradic['Doktora (Öğrenci)']=len(x)

    label_edu=getKey(gradic)
    data_edu=getValue(gradic)

    label_count=[]
    data_count=[]
    worker={}
    
    todays_date=datetime.date.today()
    start_Date=datetime.datetime(2018,4,1)
    delta= (((((todays_date.year-start_Date.year)*12+(todays_date.month-start_Date.month))-1)//3)+1) # 12
    print(range(0,delta))
    s = datetime.date(2020,6,19)
    f = datetime.date(2020,9,17)
    x=len(queryset_start)

    for i in range(0,delta):
        start_Date1=start_Date+timedelta(days=90*i)
        start_Date0=start_Date+timedelta(days=90*(i-1))
        y=len((Personel.objects.filter(rdfinisDate__range=(start_Date0,start_Date1))))
        z=len((Personel.objects.filter(rdStartDate__range=(start_Date0,start_Date1))))
        x=x-y+z
        worker[start_Date1.strftime("%Y-%m")] = x
    
    label_worker=(getKey(worker))
    data_worker=(getValue(worker))

    label_count=getKey(gradic)
    data_count=getValue(gradic)


    context = {

        'label_edu': label_edu,
        'data_edu' : data_edu,
        'label_gender': label_gender,
        'data_gender' : data_gender,
        'label_respons' : label_respons,
        'data_respons' : data_respons,
        'label_worker' : label_worker,
        'data_worker' : data_worker,
    }
    return render(request, "core/chartpersonel.html", context)

def chartPersonelview(request):
    pass
    
   # return JsonResponse(context, safe=False)



"""
def exportPersonel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Personel_List.csv"'

    writer = csv.writer(response)
    writer.writerow(['Ad','Soy Ad','Email','Cinsiyet','Doğum Tarihi',])

    personels = Personel.objects.all().values_list('name','surName','email','gender','birthDay')

    for person in personels:
        writer.writerow(person)
    
    return response
"""

# PROJE VIEWS

def projectsMain(request):
    projects = Projects.objects.all()
    projects_goon = Projects.objects.filter(ProjeDurumu=2)
    avg_projects=Projects.objects.filter(ProjeDurumu=2).aggregate(Avg('TamamlanmaYuzdesi'))['TamamlanmaYuzdesi__avg']
    
    context ={
        "projects" : projects,
        "avg_projects" : avg_projects,
        "projects_goon" : projects_goon,
    }
    return render(request,"core/projectsmain.html",context)

def addproject(request):
    user_count = Personel.objects.all().count()
    user_countmod = math.ceil(user_count/4)
    liste = str(user_countmod)
    liste2 = str(user_countmod*2)
    liste3 = str(user_countmod*3)
    liste4 = str(user_countmod*4)
    
    if request.method == 'POST':
        form = ProjectsForm(request.POST)
        context ={
            'form':form
        }
        if form.is_valid():
            form.save()
            context ={
                'form':form
            }
            return redirect('core:index')
        else:
            return render (request, 'core/addproject.html')
    else:
        form = ProjectsForm()
        context = {
            'form':form,
            'liste' : liste,
            'liste2' : liste2,
            'liste3' : liste3,
            'liste4' : liste4,
        }
    return render(request,"core/addproject.html", context )

def projectDetail(request, id):
    ispaketi = IsPaketiekle.objects.filter(projeKodu__id=id)
    project = Projects.objects.get(id=id)
    query = project.projecalis.values('name', 'surName').annotate(count=Count('adamay'),user_img = F('userImg'), rdStartDate=F('rdStartDate') )
    
    context={
        "ispaketi" : ispaketi,
        "project" : project,
        "query" : query
    }
    return render(request,"core/projectdetail.html", context)

def projectUpdate(request, id):
    project = get_object_or_404(Projects, id=id)
    user_count = Personel.objects.all().count()
    user_countmod = math.ceil(user_count/4)
    liste = str(user_countmod)
    liste2 = str(user_countmod*2)
    liste3 = str(user_countmod*3)
    liste4 = str(user_countmod*4)

    if request.method=='POST':
        form = ProjectsForm(request.POST,instance=project)
        context ={
            'form':form,
            'liste' : liste,
            'liste2' : liste2,
            'liste3' : liste3,
            'liste4' : liste4,
        }
        if form.is_valid():
            form.save()
            context ={
                'form':form,
                'liste' : liste,
                'liste2' : liste2,
                'liste3' : liste3,
                'liste4' : liste4,
                }
            return redirect('core:projectdetail', id=id)
        else:  
            return render (request, 'core/updateproject.html', context)
    else:
        form = ProjectsForm(instance=project)
        project = Projects.objects.get(id=id)
        context={
            'form':form,
            'list': list,
            'liste' : liste,
            'liste2' : liste2,
            'liste3' : liste3,
            'liste4' : liste4,
            'project' : project
        }
        return render(request,'core/updateproject.html' , context)

def addispaketi(request):
    if request.method=='POST':
        form =IsPaketiekleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"İş Paketi Eklenmiştir...")
        else:
            messages.warning(request,"İş Paketi Eklerken Beklenmedik bir Hata Oluştu")
        return redirect('core:projectdetail', id=id)
    else:
        form = IsPaketiekleForm()
        context = {
            "form" : form,
        }
        return render(request, "core/addispaketi.html", context)
    
def projeispaketiupdate(request, id):
    query = IsPaketiekle.objects.get(id=id)
    if request.method=='POST':
        form=IsPaketiekleForm(request.POST, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,"Güncelleme Başarılı")
        else:
            return redirect("core:index")
            print(form.errors)
        return redirect('core:projeispaketi', id=query.projeKodu_id)

    else:
        form=IsPaketiekleForm(instance=query)
        context={
            "form":form,
            "query" : query,
        }
        return render(request, "core/projeispaketiupdate.html", context)
    

def projeispaketi(request, id):
    querylist = IsPaketiekle.objects.filter(projeKodu__id=id)
    project = Projects.objects.get(id=id)
    context = {
        "querylist" : querylist,
        "project" : project
    }
    return render(request,"core/projeispaketi.html", context)
def exportProject(request):
    pass

def exportProjects(request):
    pass

def projectstable(request):
    projects = Projects.objects.all()

    context = {
        "projects" : projects
    }
    return render(request,"core/projectstable.html", context)
    
def personalstable(request):
    personal = Personel.objects.all()

    context = {
        "personal" : personal
    }
    return render(request,"core/personalstable.html", context)


def argePano(request):
    return render(request,"core/argepano.html")

def chartProjects(request):
    pass

def newstable(request):
    news = News.objects.all()
    context = {
        "news" : news
    }
    return render(request,"core/newstable.html", context)

def departmentstable(request):
    departments = DepartmentList.objects.all()
    context = {
        "departments" : departments
    }
    return render(request,"core/departmentstable.html", context)

def adddepartments(request):
    pass

def adamayMain(request):
    projects = Projects.objects.filter(ProjeDurumu=2)
    contex = {
        "projects" : projects,
        }
    return render(request,'core/adamaymain.html', contex)

def adamayBase(request):
    keyword = request.GET.get("keyword")
    x = Personel.objects.filter(rdfinisDate__isnull=True).aggregate(count=Count('id'))['count']
    if keyword:
        year = (keyword.split("-")[0]) 
        month = (keyword.split("-")[1])
        queryset = AdamAy.objects.filter(tarih__year__gte=year,
                                        tarih__year__lte=year,
                                        tarih__month__gte=month,
                                        tarih__month__lte=month).values('projeAdamAy__name','projeAdamAy__surName')\
                                            .annotate(total_manmonth=Sum('adamAylar'), user_img = F('projeAdamAy__userImg'),user_respons = F('projeAdamAy__respons'), id= F("projeAdamAy__id"),total_project=Count('projeKodu', distinct=True)).order_by('total_manmonth')
        querysetlist = AdamAy.objects.filter(tarih__year__gte=year,
                                    tarih__year__lte=year,
                                    tarih__month__gte=month,
                                    tarih__month__lte=month)\
                                        .annotate(user_number = F('projeAdamAy__sNumber'),expensecenter = F('projeAdamAy__expensecenter'), pyp_oge= F("projeKodu__ProjeKodu"), oran= F("adamAylar")*100, isim=F("projeAdamAy_id__name"), soyisim=F("projeAdamAy_id__surName"))
        ratio = AdamAy.objects.filter(tarih__year__gte=year,
                                    tarih__year__lte=year,
                                    tarih__month__gte=month,
                                    tarih__month__lte=month).aggregate(totalmanmonth=Sum('adamAylar') / x )
        print(ratio)

        context={ 
            'queryset' : queryset,
            "querysetlist" : querysetlist,
            'year' : year,
            'month' : month,
            'ratio' : ratio,
        }
        return render(request, 'core/adamaybase.html', context)
    else:
        today=datetime.date.today()
        queryset = AdamAy.objects.filter(tarih__year__gte=today.year,
                                        tarih__year__lte=today.year,
                                        tarih__month__gte=today.month,
                                        tarih__month__lte=today.month).values('projeAdamAy__name','projeAdamAy__surName')\
                                            .annotate(total_manmonth=Sum('adamAylar'), user_img = F('projeAdamAy__userImg'),user_respons = F('projeAdamAy__respons'), id= F("projeAdamAy__id"),total_project=Count('projeKodu', distinct=True)).order_by('total_manmonth')
        querysetlist = AdamAy.objects.filter(tarih__year__gte=today.year,
                                    tarih__year__lte=today.year,
                                    tarih__month__gte=today.month,
                                    tarih__month__lte=today.month)\
                                        .annotate(user_number = F('projeAdamAy__sNumber'),expensecenter = F('projeAdamAy__expensecenter'), pyp_oge= F("projeKodu__ProjeKodu"), oran= F("adamAylar")*100, isim=F("projeAdamAy_id__name"), soyisim=F("projeAdamAy_id__surName"))
        ratio = AdamAy.objects.filter(tarih__year__gte=today.year,
                                    tarih__year__lte=today.year,
                                    tarih__month__gte=today.month,
                                    tarih__month__lte=today.month).aggregate(totalmanmonth=Sum('adamAylar') / x * 100)
        context={ 
            'queryset' : queryset,
            "querysetlist" : querysetlist,
            'today' : today,
            "year" : today.year,
            'month' : today.month,
            'ratio' : ratio,
        }
        return render(request, 'core/adamaybase.html',context)

def addManmonth(request,id):
    person = Personel.objects.get(id=id)
    AdamayFormset = modelformset_factory(AdamAy, fields=["tarih","adamAylar"], widgets = {'tarih': forms.DateInput(attrs={'class': 'datepicker', })}, extra=0)
    formset = AdamayFormset(queryset=AdamAy.objects.filter(projeKodu_id__id=id,tarih__isnull=True,projeAdamAy__rdfinisDate__isnull=True))
    if request.method=='POST':
        formset = AdamayFormset(request.POST,
        queryset=AdamAy.objects.filter(projeKodu_id__id=id,tarih__isnull=True,projeAdamAy__rdfinisDate__isnull=True))
        for form in formset.forms:
            if form.is_valid():
                if form['tarih'].value():
                    adamAy = form.save(commit=False)
                    last_id = AdamAy.objects.last()
                    new_id = last_id.id + 1
                    adamAy.id = new_id
                    adamAy.save()
                    query = AdamAy.objects.get(id=new_id)
                    messages.success(request, f'{query.projeAdamAy} İçin Adam Ay Eklendi')
                else:
                    messages.info(request,'Bu Formda Dönem Alanına Tarih Girmediğiniz İçin Kaydedilemedi')
            else:
                messages.warning(request,'Formda Hata: Adam Ay Oranı 1den Büyük Olabilir')     
        return redirect('core:adamaybase')
    else:
        today=datetime.date.today()
        lastmonthdate = today - timedelta(days=30)
        lastmonth = AdamAy.objects.filter(tarih__year__gte=today.year,
                                        tarih__year__lte=today.year,
                                        tarih__month__gte=today.month,
                                        tarih__month__lte=today.month).values('projeAdamAy__name','projeAdamAy__surName')\
                                            .annotate(total_manmonth=Sum('adamAylar'), user_img = F('projeAdamAy__userImg'), id= F("projeAdamAy__id"),total_project=Count('projeKodu', distinct=True)).order_by('total_manmonth')
        last1month = AdamAy.objects.filter(tarih__year__gte=lastmonthdate.year,
                                        tarih__year__lte=lastmonthdate.year,
                                        tarih__month__gte=lastmonthdate.month,
                                        tarih__month__lte=lastmonthdate.month).values('projeAdamAy__name','projeAdamAy__surName')\
                                            .annotate(total_manmonth=Sum('adamAylar'), user_img = F('projeAdamAy__userImg'), id= F("projeAdamAy__id"),total_project=Count('projeKodu', distinct=True)).order_by('total_manmonth')
        context={
            "formset":formset, 
            "person":person, 
            "lastmonth":lastmonth, 
            "last1month":last1month,
            "today" : today,
            "lastmonthdate" : lastmonthdate,
        }

        return render(request,"core/addmanmonth.html", context)

def addManmonthid(request, id):
    keyword = request.GET.get("keyword")
    person = Personel.objects.get(id=id)
    AdamayFormset = modelformset_factory(AdamAy, fields=["adamAylar",], extra=0, )
    if keyword:
        year = (keyword.split("-")[0]) 
        month = (keyword.split("-")[1])
        query = AdamAy.objects.filter(tarih__year__gte=year,
                                            tarih__year__lte=year,
                                            tarih__month__gte=month,
                                            tarih__month__lte=month,projeAdamAy_id__id=id).aggregate(Sum("adamAylar"))
        if request.method=='POST':
            print('POST')
            formset = AdamayFormset(request.POST, queryset = AdamAy.objects.filter(
                                            tarih__year__gte=year,
                                            tarih__year__lte=year,
                                            tarih__month__gte=month,
                                            tarih__month__lte=month,
                                            projeAdamAy_id__id=id),
                                            )
            for form in formset.forms:
                if form.is_valid():
                    form.save()
                    messages.success(request, "Bu Personel İçin Adam/Ay Oranları Güncellendi...")
                else:
                    messages.warning(request, "Adam/Ay Oranları Güncellenemedi Tekrar Girdiğiniz Değerleri Kontrol Edin...")
            return redirect('core:addmanmonthid', id=id)
        else:
            formset = AdamayFormset(queryset = AdamAy.objects.filter(tarih__year__gte=year,
                                            tarih__year__lte=year,
                                            tarih__month__gte=month,
                                            tarih__month__lte=month,projeAdamAy_id__id=id
                                            ),)
            return render(request,"core/addmanmonthid.html",{"formset":formset, "query":query, "person":person})
    else:
        formset = AdamayFormset(queryset = AdamAy.objects.filter(projeAdamAy_id__id=id))
        return render(request,"core/addmanmonthid.html", {"formset" : formset, "person":person})

# DENEME SAYFASI=>
def deneme(request):
    if request.method == 'POST':
        form = AdamAyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Kayıt Başarılı")
            return redirect('core:news')
    else:
        form = AdamAyForm()
    return render(request, 'core/deneme.html', {"form":form})



def apiData(request):
    data = {
        "sales" : 100,
        "customers" : 10,
    }
    return JsonResponse(data)


