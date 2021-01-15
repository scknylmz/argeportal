from django import forms
from .models import Personel as Per
from .models import Personel,News,Projects, AdamAy, IsPaketiekle, ArgeTesvik, Patent, Bildiri
from django.contrib.admin.widgets import AdminDateWidget
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class PersonelForm(forms.ModelForm):
    class Meta:
        model = Personel
        exclude=()  
        widgets = {
            'startDate': forms.DateInput(attrs={'class': 'datepicker', 'id': 'startDate'}),
            'finisDate': forms.DateInput(attrs={'class': 'datepicker', 'id': 'finisDate'}),
            'rdStartDate': forms.DateInput(attrs={'class': 'datepicker', 'id': 'rdStartDate'}),
            'birthDay': forms.DateInput(attrs={'class': 'datepicker', 'id': 'birthDay'}),
        }
    def __init__(self, *args, **kwargs):
        super(PersonelForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Personel Adı'
        self.fields['surName'].widget.attrs['class'] = 'form-control'
        self.fields['surName'].widget.attrs['placeholder'] = 'Personel Soyadı'
        self.fields['gender'].widget.attrs['class'] = 'form-control'
        self.fields['gender'].widget.attrs['placeholder'] = 'Cinsiyet'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'E-Mail'
        self.fields['idName'].widget.attrs['class'] = 'form-control'
        self.fields['idName'].widget.attrs['placeholder'] = 'T.C. Kimlik No'
        self.fields['country'].widget.attrs['class'] = 'form-control'
        self.fields['country'].widget.attrs['placeholder'] = 'Uyurk'
        self.fields['sgNumber'].widget.attrs['class'] = 'form-control'
        self.fields['sgNumber'].widget.attrs['placeholder'] = 'Sosyal Güvenlik Numarası'
        self.fields['sNumber'].widget.attrs['class'] = 'form-control'
        self.fields['sNumber'].widget.attrs['placeholder'] = 'Sicil Numarası'
        self.fields['department'].widget.attrs['class'] = 'form-control'
        self.fields['department'].widget.attrs['placeholder'] = 'Departman Adı'
        self.fields['respons'].widget.attrs['class'] = 'form-control'
        self.fields['respons'].widget.attrs['placeholder'] = 'Ar-Ge Görevi'
        self.fields['graduated'].widget.attrs['class'] = 'form-control'
        self.fields['graduated'].widget.attrs['placeholder'] = 'Mezun Durumu'
        self.fields['hschool'].widget.attrs['class'] = 'form-control'
        self.fields['hschool'].widget.attrs['placeholder'] = 'Lise Adı'
        self.fields['hschooldist'].widget.attrs['class'] = 'form-control'
        self.fields['hschooldist'].widget.attrs['placeholder'] = 'Lisedeki Bölümü'
        self.fields['huschool'].widget.attrs['class'] = 'form-control'
        self.fields['huschool'].widget.attrs['placeholder'] = 'Yüksek Okul Adı'
        self.fields['huschooldist'].widget.attrs['class'] = 'form-control'
        self.fields['huschooldist'].widget.attrs['placeholder'] = 'Yüksek Okul Bölümü'
        self.fields['university'].widget.attrs['class'] = 'form-control'
        self.fields['university'].widget.attrs['placeholder'] = 'Üniversite Adı'
        self.fields['universitydist'].widget.attrs['class'] = 'form-control'
        self.fields['universitydist'].widget.attrs['placeholder'] = 'Üniversite Bölümü'
        self.fields['masteruniversity'].widget.attrs['class'] = 'form-control'
        self.fields['masteruniversity'].widget.attrs['placeholder'] = 'Yüksek Lisans Üni. Adı'
        self.fields['masteruniversitydist'].widget.attrs['class'] = 'form-control'
        self.fields['masteruniversitydist'].widget.attrs['placeholder'] = 'Yüksek Lisans Bölümü'
        self.fields['druniversity'].widget.attrs['class'] = 'form-control'
        self.fields['druniversity'].widget.attrs['placeholder'] = 'Doktora Üni. Adı'
        self.fields['druniversitydist'].widget.attrs['class'] = 'form-control'
        self.fields['druniversitydist'].widget.attrs['placeholder'] = 'Doktora Bölümü'
        self.fields['userImg'].widget.attrs['class'] = 'form-control'
        self.fields['userImg'].widget.attrs['placeholder'] = 'Profil Resmi'
        



class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        exclude=()  
        widgets = {
            'addedDate': forms.DateInput(attrs={'class': 'datepicker', 'id': 'addedDate'}),
            'updateDate': forms.DateInput(attrs={'class': 'datepicker', 'id': 'updateDate'}),
        }

class IsPaketiekleForm(forms.ModelForm):
    
    class Meta:
        model = IsPaketiekle
        exclude=()
        widgets = {
            'baslangicTarihi': forms.DateInput(attrs={'class': 'datepicker', 'id': 'baslangicTarihi'}),
            'bitisTarihi': forms.DateInput(attrs={'class': 'datepicker', 'id': 'bitisTarihi'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(IsPaketiekleForm, self).__init__(*args, **kwargs)
        self.fields['projeKodu'].widget.attrs['class'] = 'form-control'
        self.fields['projeKodu'].widget.attrs['placeholder'] = 'Projenin Durumu'
        self.fields['isPaketino'].widget.attrs['class'] = 'form-control'
        self.fields['isPaketino'].widget.attrs['placeholder'] = 'Projenin Durumu'
        self.fields['isPaketiadi'].widget.attrs['class'] = 'form-control'
        self.fields['isPaketiadi'].widget.attrs['placeholder'] = 'Projenin Durumu'
        self.fields['sorumlu'].widget.attrs['class'] = 'form-control'
        self.fields['sorumlu'].widget.attrs['placeholder'] = 'Projenin Durumu'
        self.fields['tamamlanmaOranı'].widget.attrs['class'] = 'form-control'
        self.fields['tamamlanmaOranı'].widget.attrs['placeholder'] = 'Projenin Durumu'
        self.fields['faaliyet'].widget.attrs['class'] = 'form-control'
        self.fields['faaliyet'].widget.attrs['placeholder'] = 'Projenin Durumu'


class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Projects
        exclude=[]
        widgets = {
            'ProjeBaslamaTarihi': forms.DateInput(attrs={'class': 'datepicker', 'id': 'ProjeBaslamaTarihi'}),
            'ProjeBitisTarihi': forms.DateInput(attrs={'class': 'datepicker', 'id': 'ProjeBitisTarihi'}),
            'ProjeGuncellemeTarihi': forms.DateInput(attrs={'class': 'datepicker', 'id': 'ProjeGuncellemeTarihi'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ProjectsForm, self).__init__(*args, **kwargs)
        self.fields['ProjeDurumu'].widget.attrs['class'] = 'form-control'
        self.fields['ProjeDurumu'].widget.attrs['placeholder'] = 'Projenin Durumu'
        self.fields['ProjeKodu'].widget.attrs['class'] = 'form-control'
        self.fields['ProjeKodu'].widget.attrs['placeholder'] = 'Proje Kodu'
        self.fields['ProjeAdi'].widget.attrs['class'] = 'form-control'
        self.fields['ProjeAdi'].widget.attrs['placeholder'] = 'Projenin Adı'
        self.fields['ProjeYurutucusu'].widget.attrs['class'] = 'form-control'
        self.fields['ProjeYurutucusu'].widget.attrs['placeholder'] = 'Proje Yürütücüsü'
        self.fields['ProjeBaslamaTarihi'].widget.attrs['placeholder'] = 'Proje Başlangıç Tarihi'
        self.fields['ProjeBitisTarihi'].widget.attrs['placeholder'] = 'Proje Bitiş Tarihi'
        self.fields['TamamlanmaYuzdesi'].widget.attrs['class'] = 'form-control'
        self.fields['TamamlanmaYuzdesi'].widget.attrs['placeholder'] = 'Projenin Tamamlanma Yüzdesi'
        self.fields['ProjeSuresiAdamAy'].widget.attrs['class'] = 'form-control'
        self.fields['ProjeSuresiAdamAy'].widget.attrs['placeholder'] = 'Proje Adam/Ay Sayısı'
        self.fields['ProjeKonusu'].widget.attrs['class'] = 'form-control'
        self.fields['ProjeKonusu'].widget.attrs['placeholder'] = 'Projenin Konusu'
        self.fields['ProjeOzeti'].widget.attrs['class'] = 'form-control'
        self.fields['ProjeOzeti'].widget.attrs['placeholder'] = 'Projenin Özeti'
        self.fields['UlusalDestek'].widget.attrs['class'] = 'form-control'
        self.fields['UlusalDestek'].widget.attrs['placeholder'] = 'Ulusal Destek Programı Var Mı?'
        self.fields['UlusalDestekTanim'].widget.attrs['class'] = 'form-control'
        self.fields['UlusalDestekTanim'].widget.attrs['placeholder'] = 'Ulusal Destek Tanımı'
        self.fields['OzKaynakTutar'].widget.attrs['class'] = 'form-control'
        self.fields['OzKaynakTutar'].widget.attrs['placeholder'] = 'Öz Kaynaklarca Karşılanan tutar (TL)'
        self.fields['DestekTutari'].widget.attrs['class'] = 'form-control'
        self.fields['DestekTutari'].widget.attrs['placeholder'] = 'Destek Tutarı (TL)'
        self.fields['ToplamProjeButcesi'].widget.attrs['class'] = 'form-control'
        self.fields['ToplamProjeButcesi'].widget.attrs['placeholder'] = 'Toplam Proje Bütçesi'
        self.fields['HizmetAlimiKonusu'].widget.attrs['class'] = 'form-control'
        self.fields['HizmetAlimiKonusu'].widget.attrs['placeholder'] = 'Hizmet Alımı Konusu'
        self.fields['HizmetAlimi'].widget.attrs['class'] = 'form-control'
        self.fields['HizmetAlimi'].widget.attrs['placeholder'] = 'Hizmet Alımı Yapılan Yer.'
        self.fields['YurtIciHizmetAlimiTutari'].widget.attrs['class'] = 'form-control'
        self.fields['YurtIciHizmetAlimiTutari'].widget.attrs['placeholder'] = 'Yurt İçi Hizmet Alımı Tutarı (TL)'
        self.fields['YurtDisiHizmetAlimiTutari'].widget.attrs['class'] = 'form-control'
        self.fields['YurtDisiHizmetAlimiTutari'].widget.attrs['placeholder'] = 'Yurt Dışı Hizmet Alımı Tutarı (TL)'
        self.fields['ProjeKonusunuBelirleyenIhtiyaclar'].widget.attrs['class'] = 'form-control'
        self.fields['ProjeKonusunuBelirleyenIhtiyaclar'].widget.attrs['placeholder'] = 'Projenin Konusunu Belirleyen İhtiyaçlar'
        self.fields['ProjeKapsamindaYapilacakFaaliyetler'].widget.attrs['class'] = 'form-control'
        self.fields['ProjeKapsamindaYapilacakFaaliyetler'].widget.attrs['placeholder'] = 'Proje Kapsamında Yapılacak Faaliyetler'
        self.fields['ProjeninYenilikciYonuArgeNiteligi'].widget.attrs['class'] = 'form-control'
        self.fields['ProjeninYenilikciYonuArgeNiteligi'].widget.attrs['placeholder'] = 'Projenin Yenilikçi Yönü ve AR-GE Niteliği'
        self.fields['ProjeninBeklenenCiktilariFaydalari'].widget.attrs['class'] = 'form-control'
        self.fields['ProjeninBeklenenCiktilariFaydalari'].widget.attrs['placeholder'] = 'Projenin Beklenen Çıktıları'
        self.fields['ProjePersonel'].widget.attrs['class'] = 'form-control'
        self.fields['ProjePersonel'].widget.attrs['placeholder'] = 'Projedeki Personel Sayısı'
        self.fields['UniversiteSanayiIsbirligiProjesi'].widget.attrs['class'] = 'form-control'
        self.fields['UniversiteSanayiIsbirligiProjesi'].widget.attrs['placeholder'] = 'Üniversite-Sanayi İşbirliği Mi?'
        self.fields['FirmalarArasiArgeIsbirligi'].widget.attrs['class'] = 'form-control'
        self.fields['FirmalarArasiArgeIsbirligi'].widget.attrs['placeholder'] = 'Firmalar Arası Ar-Ge İşbirliği Mi?'
        self.fields['SipariseDayaliArgeProjesi'].widget.attrs['class'] = 'form-control'
        self.fields['SipariseDayaliArgeProjesi'].widget.attrs['placeholder'] = 'Siparişe Dayalı Ar-Ge Projesi Mi?'
        self.fields['ProjeGuncellemeTarihi'].widget.attrs['placeholder'] = 'Projenin Güncelleme Tarihi:'
        self.fields['PRojeCiktisi'].widget.attrs['class'] = 'form-control'
        self.fields['PRojeCiktisi'].widget.attrs['placeholder'] = 'Projenin Çıktısı'

    projecalis = forms.ModelMultipleChoiceField(queryset=Personel.objects.all(),label=('Projede Çalışan Personeller'),widget=forms.CheckboxSelectMultiple)

class ArgetesvikForm(forms.ModelForm):
    class Meta:
        model = ArgeTesvik
        exclude = ["ayliktesviktoplam", "ayliktesvikyuzde"]
        widgets = {
            'date' : forms.DateInput(attrs={'class' : 'datepicker', 'id' : 'date'})
        }
    
    def __init__(self,*args, **kwargs):
        super(ArgetesvikForm, self).__init__(*args, **kwargs)
        self.fields['argetotal'].widget.attrs['class'] = 'form-control'
        self.fields['argetotal'].widget.attrs['placeholder'] = 'Ar-Ge Toplam Harcaması'
        self.fields['hibe'].widget.attrs['class'] = 'form-control'
        self.fields['hibe'].widget.attrs['placeholder'] = 'Alınan TEYDEB Hibeleri'
        self.fields['sgktesvik5746'].widget.attrs['class'] = 'form-control'
        self.fields['sgktesvik5746'].widget.attrs['placeholder'] = '5746 Arge SGK Teşviki'
        self.fields['gelirtesvik5746'].widget.attrs['class'] = 'form-control'
        self.fields['gelirtesvik5746'].widget.attrs['placeholder'] = '5746 Arge Gelir Vergisi'
        self.fields['argeindirim'].widget.attrs['class'] = 'form-control'
        self.fields['argeindirim'].widget.attrs['placeholder'] = 'Kurumlar/Geçici Arge Vergi İndirimi'

class AdamAyForm(forms.ModelForm):
    class Meta:
        model = AdamAy
        exclude=[]
        widgets = {'tarih': forms.DateInput(attrs={'class': 'datepicker', 'id': 'tarih'}),}


class PatentekleForm(forms.ModelForm):
    class Meta:
        model = Patent
        exclude =[]
        widgets = { 'apldate' : forms.DateInput(attrs={'class' : 'datepicker', 'id' : 'apldate'}),
                    'aprdate' : forms.DateInput(attrs={'class' : 'datepicker', 'id' : 'aprdate'})
                    }

    def __init__(self, *args, **kwargs):
        super(PatentekleForm, self).__init__(*args, **kwargs)
        self.fields['model'].widget.attrs['class'] = 'form-control'
        self.fields['model'].widget.attrs['placeholder'] = 'Tür Seçiniz'
        self.fields['area'].widget.attrs['class'] = 'form-control'
        self.fields['area'].widget.attrs['placeholder'] = 'Kapsam Seçiniz'
        self.fields['code'].widget.attrs['class'] = 'form-control'
        self.fields['code'].widget.attrs['placeholder'] = 'Paten/Model Başvuru Kodunu Giriniz'
        self.fields['inventor'].widget.attrs['class'] = 'form-control'
        self.fields['inventor'].widget.attrs['placeholder'] = 'Buluşçuları liste şeklinde yazınız'
        self.fields['topic'].widget.attrs['class'] = 'form-control'
        self.fields['topic'].widget.attrs['placeholder'] = 'Buluşun Konusunu Açıklayınız'
        self.fields['consultant'].widget.attrs['class'] = 'form-control'
        self.fields['consultant'].widget.attrs['placeholder'] = 'Alınan Danışmanlık Şirketini Yazınız'
        self.fields['project'].widget.attrs['class'] = 'form-control'
        self.fields['project'].widget.attrs['placeholder'] = 'Bağlı Olan Projeyi Giriniz'
        self.fields['situation'].widget.attrs['class'] = 'form-control'
        self.fields['situation'].widget.attrs['placeholder'] = 'Durumunu Giriniz'
        self.fields['detail'].widget.attrs['class'] = 'form-control'
        self.fields['detail'].widget.attrs['placeholder'] = 'Patent Hk. Gelişmeleri Yazınız'

class BildiriekleForm(forms.ModelForm):
    class Meta:
        model = Bildiri
        exclude = []
        widgets = {'pubdate' : forms.DateInput(attrs={'class' : 'datepicker', 'id' : 'pubdate'})}
    
    def __init__(self,*args, **kwargs):
        super(BildiriekleForm, self).__init__(*args, **kwargs)
        self.fields['typ'].widget.attrs['class'] = 'form-control'
        self.fields['typ'].widget.attrs['placeholder'] = 'Tip'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Adını Giriniz'
        self.fields['location'].widget.attrs['class'] = 'form-control'
        self.fields['location'].widget.attrs['placeholder'] = 'Yayınlanan Yer'
        self.fields['owner'].widget.attrs['class'] = 'form-control'
        self.fields['owner'].widget.attrs['placeholder'] = 'Yayın Sahibi'
        self.fields['file_bildiri'].widget.attrs['class'] = 'form-control'
        self.fields['file_bildiri'].widget.attrs['placeholder'] = 'Yayın Dosyası'
        


