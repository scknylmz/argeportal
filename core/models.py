from django.db import models
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminDateWidget
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class DepartmentList(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

    class Meta:
        db_table = "DepartmentList"
        verbose_name_plural = "Departman Listesi"

class UniversityList(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

    class Meta:
        db_table = "UniversityList"
        verbose_name_plural = "Ar-Ge Universite"

class Personel(models.Model):

    graduatedList=[
        (0, "Diğer"),
        (1, "Lise"),
        (2, "Lise (Öğrenci)"),
        (3, "Ön Lisans"),
        (4, "Ön Lisans (Öğrenci)"),
        (5, "Lisans"),
        (6, "Lisans (Öğrenci)"),
        (7, "Yüksek Lisans"),
        (8, "Yüksek Lisans (Öğrenci)"),
        (9, "Doktora"),
        (10, "Doktora (Öğrenci)")
    ]

    def validate_digit_length(self, idName):
        if not (idName.isdigit() and len(idName) == 11):
            raise ValidationError('%(idName)s en az 11 karakter olmalıdır', params={'idName': idName}, )

    name = models.CharField(max_length=30, verbose_name="Adı")
    surName = models.CharField(max_length=20, verbose_name="Soyadı")
    email = models.EmailField(max_length=50, verbose_name="Email Adresi", default="abcdefg@supsan.com")
    gender = models.IntegerField(choices=((1,"Erkek"),(2,"Kadın")),default=1, verbose_name="Cinsiyet")
    birthDay=models.DateField(("Doğum Tarihi"), auto_now=False, auto_now_add=False)
    idName = models.CharField(max_length=11, verbose_name="T.C. Kimlik No", default='12345678911')
    country = CountryField(verbose_name="Uyruk", default='TR')
    sgNumber = models.IntegerField(null=True, blank=True, verbose_name="Sosyal Güvenlik Numarası")
    sNumber = models.IntegerField(null=True, blank=True, verbose_name="Sicil No")
    department = models.ForeignKey(DepartmentList, on_delete=models.SET_DEFAULT, verbose_name="Çalıştığı Departman", default=0, related_name="PersonelDepartman")
    respons = models.IntegerField(choices=((1,"Araştırmacı"),(2,"Teknisyen"),(3, "Destek Personeli")),default=1, verbose_name="Ar-Ge Görevi")
    startDate = models.DateField(null=True, blank=True, verbose_name="İşe Başlangıç Tarihi")
    finisDate = models.DateField(null=True, blank=True, verbose_name="İşten Ayrılış Tarihi")
    rdfinisDate = models.DateField(null=True, blank=True, verbose_name="Ar-Ge Ayrılış Tarihi")
    rdStartDate= models.DateField(null=True, blank=True, verbose_name="Ar-Ge Merkezi İşe Başlama Tarihi")
    graduated = models.IntegerField(choices=graduatedList, default=0, verbose_name="Tahsil Durumu")
    hschool = models.CharField(null=True, blank=True, max_length=50, verbose_name="Lise Adı",)
    hschooldist = models.CharField(null=True, blank=True, max_length=50, verbose_name="Lise Bölümü",)
    huschool = models.ForeignKey(UniversityList,on_delete=models.SET_DEFAULT, verbose_name="Universite (Ön Lisans)", default=1, related_name='onlisans')
    huschooldist = models.CharField(null=True, blank=True, max_length=50, verbose_name="Bölümü (Ön Lisans)",)
    university = models.ForeignKey(UniversityList,on_delete=models.SET_DEFAULT, verbose_name="Universite (Lisans)", default=1, related_name='lisans')
    universitydist = models.CharField(null=True, blank=True, max_length=50, verbose_name="Bölümü (Lisans)",)
    masteruniversity = models.ForeignKey(UniversityList,on_delete=models.SET_DEFAULT, verbose_name="Universite (Yüksek Lisans)", default=1,related_name='master')
    masteruniversitydist = models.CharField(null=True, blank=True, max_length=50, verbose_name="Bölümü (Yüksek Lisans")
    druniversity = models.ForeignKey(UniversityList,on_delete=models.SET_DEFAULT, verbose_name="Universite (Doktora)", default=1,related_name='doktora')
    druniversitydist = models.CharField(null=True, blank=True, max_length=50, verbose_name="Bölümü (Doktora")
    userImg = models.ImageField(upload_to='personels/img/', blank = True, null = True, verbose_name="Kullanıcı Profil Resmi")
    expensecenter = models.IntegerField(("Masraf Yeri"), choices=((4001,"4001"),(4002,"4002")), blank=True, null=True, default=4001)

    def __str__(self):
        return f"{self.name},{self.surName}"

    class Meta:
        db_table = "personel"
        verbose_name_plural = "Ar-Ge Personeller"

class News(models.Model):
    title = models.CharField(("Başlık"), max_length=100)
    body = models.TextField(("Gövde"), max_length=500)
    content = RichTextField()
    addedDate = models.DateField(("Haber Eklme Tarihi"),null = True, blank=True, default=timezone.now)
    updateDate = models.DateField(("Haber Güncelleme Tarihi"),null = True, blank=True, default=timezone.now)
    newsImg = models.ImageField(upload_to='news/img/', blank=True, null=True, verbose_name="Haber Görseli")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "Haberler"
        verbose_name_plural = "Ar-Ge Haberler"
        ordering=['-updateDate']

class Projects(models.Model):
    ProjeDurumu = models.IntegerField(("Proje Durumu:"), choices=((0,"Seçiniz"),(1,"Tamamlandı"),(2,"Devam Ediyor"),(3,"İptal")), default=0)
    ProjeKodu = models.CharField(("Proje Kodu:"), max_length=50)
    ProjeAdi= models.CharField(("Proje Adı:"), max_length=120)
    ProjeYurutucusu= models.ForeignKey(Personel, verbose_name=("Proje Yürütücüsü"), on_delete=models.CASCADE,blank=True,null=True, related_name="Proje_Y")
    ProjeBaslamaTarihi = models.DateField(("Proje Başlama Tarihi:"), null=True, blank=True)
    ProjeBitisTarihi= models.DateField(("Proje Bitiş Tarihi:"), null=True, blank=True)
    TamamlanmaYuzdesi = models.FloatField(("Projenin Tamamlanma Yüzdesi"),max_length=2,default=0, validators = [MinValueValidator(0), MaxValueValidator(100)])
    ProjeSuresiAdamAy=models.IntegerField(("Proje Adam Ay Süresi:"), null=True, blank=True)
    ProjeKonusu= models.TextField(("Proje Konusu:"), max_length=1000)
    ProjeOzeti= models.TextField(("Proje Özeti:"), max_length=1000)
    UlusalDestek= models.BooleanField(("Ulusal Destek Prgramı Var Mı?"), default=False)
    UlusalDestekTanim= models.CharField(("Ulusal Destek Adı:"), max_length=50, null=True, blank=True)
    OzKaynakTutar= models.DecimalField(("Öz Kaynaklarca Karşılanan tutar (TL):"), max_digits=10, decimal_places=2,null=True, blank=True)
    DestekTutari=models.DecimalField(("Destek Tutarı (TL):"), max_digits=10, decimal_places=2,null=True, blank=True)
    ToplamProjeButcesi= models.DecimalField(("Toplam Proje Bütçesi"), max_digits=10, decimal_places=2,null=True, blank=True)
    HizmetAlimiKonusu= models.CharField(("Hizmet Alımı Konusu:"), max_length=50, null=True, blank=True)
    HizmetAlimi=models.IntegerField(("Hizmet Alımı Yapılan Yer"),choices=((0,"Hizmet Alımı Yapılmadı"),(1,"Yurt İçi"),(2,"Yurt Dışı"),(3,"Her İkisi")), default=0)
    YurtIciHizmetAlimiTutari=models.IntegerField(("Yurt İçi Hizmet Alımı Tutarı (TL):"), default=0, null=True, blank=True)
    YurtDisiHizmetAlimiTutari=models.IntegerField(("Yurt Dışı Hizmet Alımı Tutarı (TL):"), default=0, null=True, blank=True)
    ProjeKonusunuBelirleyenIhtiyaclar=models.TextField(("Projenin Konusunu Belirleyen İhtiyaçlar:"),null=True, blank=True, max_length=5000)
    ProjeKapsamindaYapilacakFaaliyetler= models.TextField(("Proje Kapsamında Yapılacak Faaliyetler:"),null=True, blank=True, max_length=5000)
    ProjeninYenilikciYonuArgeNiteligi=models.TextField(("Projenin Yenilikçi Yönü ve AR-GE Niteliği:"),null=True, blank=True, max_length=5000)
    ProjeninBeklenenCiktilariFaydalari=models.TextField(("Projenin Beklenen Çıktıları:"),null=True, blank=True, max_length=5000)
    ProjePersonel= models.IntegerField(("Projedeki Personel Sayısı:"),null=True, blank=True)
    UniversiteSanayiIsbirligiProjesi=models.IntegerField(("Üniversite-Sanayi İşbirliği Mi?"), choices=((0,"Seçiniz"),(1,"Evet"),(2,"Hayır")),default=0)
    FirmalarArasiArgeIsbirligi=models.IntegerField(("Firmalar Arası Ar-Ge İşbirliği Mi?"), choices=((0,"Seçiniz"),(1,"Evet"),(2,"Hayır")),default=0)
    SipariseDayaliArgeProjesi=models.IntegerField(("Siparişe Dayalı Ar-Ge Projesi Mi?"), choices=((0,"Seçiniz"),(1,"Evet"),(2,"Hayır")),default=0)
    ProjeGuncellemeTarihi=models.DateField(("Projenin Güncelleme Tarihi:"),null=True, blank=True)
    PRojeCiktisi= models.IntegerField(("Projenin Çıktısı"),choices=((0,"Seçiniz"),(1,"Ticari Ürün"),(2,"Proses Geliştirme"),(3,"Bilgi Birikimi ve Yetkinlik Kazanımı")),default=0)
    projecalis = models.ManyToManyField(Personel, verbose_name=("Projede Çalışan Personeller:"),related_name="Proje_adam_ay", through="AdamAy")

    def __str__(self):
        return f"{self.ProjeKodu}"
    
    class Meta:
        db_table = "Projeler"
        verbose_name_plural = "Ar-Ge Projeler"

class IsPaketiekle(models.Model):
    projeKodu = models.ForeignKey(Projects, verbose_name=("Proje Kodu"), on_delete=models.CASCADE, null=True)
    isPaketino = models.IntegerField(("İş Paketi No:"), choices=((1,"IP.1"), (2,"IP.2"), (3,"IP.3"), (4,"IP.4"), (5,"IP.5"), (6,"IP.6")), default=1)
    isPaketiadi = models.CharField(("İş Paketi Başlığı"), max_length=100, default="İş Paketi Başlığı") 
    sorumlu = models.ForeignKey(Personel, verbose_name=("İş Paketi Sorumlusu"), on_delete=models.CASCADE, null=True)
    baslangicTarihi = models.DateField(("İş Paketi Başlangıcı"), null=True, blank=True)
    bitisTarihi = models.DateField(("İş Paketi Bitişi"), null=True, blank=True)
    tamamlanmaOranı = models.FloatField(("Projenin Tamamlanma Yüzdesi"),max_length=2,default=0, validators = [MinValueValidator(0), MaxValueValidator(100)])
    faaliyet = models.CharField(("Yapılacak Faaliyetler"), max_length=2000, null=True, blank=True)

    def __str__(self):
        return f"{self.projeKodu},{self.isPaketiadi}"
    
    class Meta:
        db_table = "IsPaketleri"
        verbose_name_plural = "Proje Ispaketleri"

class AdamAy(models.Model):
    projeKodu = models.ForeignKey(Projects, verbose_name=("Proje Kodu"), on_delete=models.CASCADE, null=True)
    projeAdamAy = models.ForeignKey(Personel, verbose_name=("Projede Çalışan Personel"), on_delete=models.CASCADE)
    tarih= models.DateField(("Dönem:"), null=True, blank=True)
    adamAylar = models.DecimalField(("Adam Ay:"), max_digits=2, decimal_places=2, default=0.0, validators = [MaxValueValidator(1.0 ,message="1.0 girilemez")])
    

    def __str__(self):
        return f"{self.projeKodu}"

    class Meta:
        db_table = "AdamAy"
        verbose_name_plural = "Adam Ay"



class ArgeTesvik(models.Model):
    date = models.DateField(("Dönem"), auto_now=False, auto_now_add=False)
    argetotal = models.DecimalField(("Toplam Arge Harcaması"), max_digits=10, decimal_places=2, default=0.0)
    hibe = models.DecimalField(("Nakit Alınan Hibe"), max_digits=10, decimal_places=2, default=0.0, null=True, blank=True)
    sgktesvik5746 = models.DecimalField(("5746 SGK Teşvik"), max_digits=10, decimal_places=2, default=0.0)
    gelirtesvik5746 = models.DecimalField(("5746 Gelir Teşvik"), max_digits=10, decimal_places=2, default=0.0)
    argeindirim = models.DecimalField(("Kurumlar-Geçici Ar-Ge İndirimi"), max_digits=10, decimal_places=2, default=0.0, null=True, blank=True)
    ayliktesviktoplam = models.DecimalField(("Toplam Ar-Ge Teşviği"), max_digits=10, decimal_places=2, default=0, editable=False)
    ayliktesvikyuzde = models.IntegerField(("Ar-Ge Teşviği Oran"),default=0, editable=False)
    
    @property
    def get_ayliktesviktoplam(self):
        return self.hibe + self.sgktesvik5746 + self.gelirtesvik5746 + self.argeindirim
    
    @property
    def get_ayliktesvikyuzde(self):
        return self.ayliktesviktoplam *100 / self.argetotal
    
    def save(self, *args, **kwargs):
        self.ayliktesviktoplam = self.get_ayliktesviktoplam
        self.ayliktesvikyuzde = self.get_ayliktesvikyuzde
        super(ArgeTesvik,self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.date}"

    class Meta:
        db_table = "ArgeTesvik"
        verbose_name_plural = "ArgeTesvik"

class Patent(models.Model):
    model = models.IntegerField(choices=((0,"Seçiniz"),(1,"Patent"),(2,"Faydalı Model")), default=0)
    area = models.IntegerField(choices=((0,"Seçiniz"),(1,"Ulusal"),(2,"Uluslar Arası")), default=0)
    code = models.CharField(("Buluş Kodu"), max_length=50)
    inventor = models.CharField(("Buluşçular"), max_length=50)
    topic = models.TextField(("Buluş Konusu"))
    consultant = models.CharField(("Patent Danışmanı"), max_length=50)
    apldate = models.DateField(("Başvuru Tarihi"), auto_now=False, auto_now_add=False)
    aprdate = models.DateField(("Tescil Tarihi"), auto_now=False, auto_now_add=False, null=True, blank=True)
    project = models.ForeignKey(Projects, verbose_name=("İlgili Proje Kodu"), on_delete=models.CASCADE, null=True, blank=True)
    situation = models.IntegerField(choices=((0,"Başvuru"),(1,"Belge Alındı"),(2,"Koruma Süresi Doldu"),(3,"Terk Edildi"),(4,"Reddedildi"),(5,"Ülke Aşaması")))
    detail = models.TextField(("Durum hk. Açıklama"), null=True, blank=True)
    file_patent = models.FileField(upload_to='patent/', max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = "Patent"
        verbose_name_plural = ("Patent")

    def __str__(self):
        return self.code

class Bildiri(models.Model):
    typ = models.IntegerField(choices=((0,"Makale"),(1,"Bildiri"),(2,"Poster")), default=0)
    area = models.IntegerField(choices=((0,"Seçiniz"),(1,"Ulusal"),(2,"Uluslar Arası")), default=0)
    name = models.CharField(max_length=250)
    location = models.CharField(("Yayınlanan Yer"), max_length=250)
    pubdate = models.DateField(("Yayınlanma Tarihi"), auto_now=False, auto_now_add=False)
    owner = models.CharField(("Yazarlar"), max_length=250)
    file_bildiri = models.FileField(upload_to='bildiri/files/', max_length=100, blank=True, null=True)

    class Meta:
        db_table = "Bildiri"
        verbose_name_plural = ("Bildiri")

    def __str__(self):
        return self.name






