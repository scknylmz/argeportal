from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
    path('', views.index, name="index"),
    path('personel/addpersonel/', views.addPersonel, name='addpersonel'),
    path('personel/personelmain/', views.personelMain, name='personelmain'),
    path('personel/personelmain/detail/<int:id>', views.personelDetail, name='personeldetail'),
    path('personel/personelmain/update/<int:id>', views.personelUpdate, name='personelupdate'),
    path('personel/personelmain/export', views.exportPersonel, name='exportPersonel'),
    path('personel/personelmain/exportperson/<int:id>', views.exportPerson, name='exportPerson'),
    path('personel/personalstable/', views.personalstable, name='personalstable'),
    path('charts/personel', views.chartPersonel, name='chartPersonel'),
    path('charts/projects', views.chartProjects, name='chartProjects'),
    path('chartPersonelview', views.chartPersonelview, name='chartPersonelview'),
    path('charts/', views.argePano, name="argepano"),
    path('news/', views.news, name='news'),
    path('news/newstable', views.newstable, name='newstable'),
    path('news/<int:id>', views.newsDetail, name='newsdetail'),
    path('news/addnews/', views.addNews, name='addnews'),
    path('news/update/<int:id>', views.updateNews, name='updatenews'),
    path('news/delete/<int:id>', views.deleteNews, name='deletenews'),
    path('projects/projectsmain', views.projectsMain, name="projectsmain"),
    path("projects/addproject",views.addproject, name="addproject"),
    path('projects/projectsmain/detail/<int:id>', views.projectDetail, name="projectdetail"),
    path('projects/projectsmain/update/<int:id>', views.projectUpdate, name="projectupdate"),
    path('projects/projectsmain/export', views.exportProjects, name='exportprojects'),
    path('projects/projectsmain/exportproject/<int:id>', views.exportProject, name='exportproject'),
    path('projects/projectstable/', views.projectstable, name='projectstable'),
    path('maintance/departmentstable/', views.departmentstable, name='departmentstable'),
    path('maintance/adddepartments/', views.adddepartments, name='adddepartments'),
    path('projects/adamaymain', views.adamayMain, name='adamaymain'),
    path('projects/adamaybase', views.adamayBase, name='adamaybase'),
    path('projects/addmanmonth/<int:id>', views.addManmonth, name='addmanmonth'),
    path('projects/addmanmonthid/<int:id>', views.addManmonthid, name='addmanmonthid'),
    path('projects/addispaketi/', views.addispaketi, name='addispaketi'),
    path('projects/projectsmain/projeispaketi/<int:id>', views.projeispaketi, name='projeispaketi'),
    path('projects/projectsmain/projeispaketi/update/<int:id>', views.projeispaketiupdate, name='projeispaketiupdate'),
    path('argetesvik/', views.argetesvik, name='argetesvik'),
    path('argetesvik/ekle', views.argetesvikekle, name='argetesvikekle'),
    path('argetesvik/duzenle/<int:id>', views.argetesvikduzenle, name='argetesvikduzenle'),
    path('argetesvik/sil/<int:id>', views.argetesviksil, name='argetesviksil'),
    path('fikrimulkiyet/', views.patent, name='patent'),
    path('patent/ekle', views.patentekle, name='patentekle'),
    path('patent/duzenle/<int:id>', views.patentduzenle, name='patentduzenle'),
    path('patent/sil/<int:id>', views.patentsil, name='patentsil'),
    path('bildiri/ekle', views.bildiriekle, name='bildiriekle'),
    path('bildiri/duzenle/<int:id>', views.bildiriduzenle, name='bildiriduzenle'),
    path('bildiri/sil/<int:id>', views.bildirisil, name='bildirisil'),
    path('api/data', views.apiData, name='apiData'),
    
    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)