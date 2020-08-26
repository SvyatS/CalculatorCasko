from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib import auth
from django.db import models
from .models import *
from .forms import *
import datetime
import json

def Cheking(data):
    if(data == 'on'):
        return True
    else:
        return False

class Info(View):
    def get(self, request):
        return render(request, "calculator/info.html")



class Delete_humans(View):
    def get(self, request):
        id = request.GET.getlist("data[]")
        print(id)
        drivers = []
        if(id[0]==''):
            id.remove('')
        for i in id:
            driver = Policyholder.objects.get(id = int(i))
            if(driver.status == "Помечено на удаление"):
                driver.status = "Черновик"
            else:
                driver.status = "Помечено на удаление"
            driver.save()
            # drivers.append(driver)
        drivers = []
        if(request.user.username == "admin"):
            drivers = Policyholder.objects.all()
        else:
            author = request.user
            drivers = Policyholder.objects.filter(admin = author)
        start = drivers[0]
        end = drivers[len(drivers) - 1]
        return render(request, 'calculator/home.html', context = {"drivers": drivers, 'start': start, 'end': end})

class Filter(View):
    def get(self, request):
        family = request.GET.get("data")
        print(family)
        if(request.user.username == "admin"):
            if(request.GET.get("data") == ""):
                drivers = Policyholder.objects.all()
            else:
                drivers = Policyholder.objects.filter(familyname__istartswith=family)
        else:
            author = request.user
            if(request.GET.get("data") == ""):
                drivers = Policyholder.objects.filter(admin = author)
            else:
                drivers = Policyholder.objects.filter(admin = author, familyname__istartswith=family)

        return render(request, 'calculator/home.html', context = {"drivers": drivers})



class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        if(request.user.username == "admin"):
            drivers = Policyholder.objects.all()
        else:
            author = request.user
            drivers = Policyholder.objects.filter(admin = author)

        paginator = Paginator(drivers, 15) # Show 25 contacts per page

        page = request.GET.get('page')
        try:
            drivers = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            drivers = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            drivers = paginator.page(paginator.num_pages)
        return render(request, 'calculator/home.html', context = {"drivers": drivers})


def Payment_check(request, data):
    data.car_year = int(data.car_year)
    data.insurance_amount = int(data.insurance_amount)
    data.class_master = int(data.class_master)
    data.driver_age = int(data.driver_age)
    data.experience = int(data.experience)
    data.number_of_drivers = int(data.number_of_drivers)
    data.kmb = float(data.kmb)
    data.number_of_payments = int(data.number_of_payments)
    data.insurance_period = int(data.insurance_period)
    data.prize_kf = float(data.prize_kf)
    data.anderright_kf = float(data.anderright_kf)
    data.insurance_liability = int(data.insurance_liability)
    data.insurance_prize_osago = int(data.insurance_prize_osago)
    data.insurance_accident = int(data.insurance_accident)

    age_car = datetime.datetime.now().year - data.car_year

    if(int(data.class_master) == 2):
        KM = 1
    else:
        if(age_car > 5):
            KM = 1.3
        else:
            KM = 1
    prise_car = int(data.insurance_amount)
    age_driver = int(data.driver_age)
    exp = int(data.experience)
    TB_wear = 0
    TB = 0
    if(prise_car>999999):
        if(age_car <= 3):
            TB = 6
        elif(age_car > 3 and age_car <=5):
            TB = 7.6
            TB_wear = 6.4
        elif(age_car > 5 and age_car <=7):
            TB = 11
            TB_wear = 7.8
        elif(age_car >= 8):
            TB_wear = 11
    elif(prise_car>650000 and prise_car<1000000):
        if(age_car <= 3):
            TB = 6.7
        elif(age_car > 3 and age_car <=5):
            TB = 8.1
            TB_wear = 7.1
        elif(age_car > 5 and age_car <=7):
            TB = 11
            TB_wear = 7.6
        elif(age_car >= 8):
            TB_wear = 11
    elif(prise_car>300000 and prise_car<=650000):
        if(age_car <= 3):
            TB = 8
        elif(age_car > 3 and age_car <=5):
            TB = 9
            TB_wear = 8.1
        elif(age_car > 5 and age_car <=7):
            TB = 12
            TB_wear = 8.4
        elif(age_car >= 8):
            TB_wear = 13.1
    elif(prise_car<=300000):
        if(age_car <= 3):
            TB = 9.3
        elif(age_car > 3 and age_car <=5):
            TB = 11
            TB_wear = 9
        elif(age_car > 5 and age_car <=7):
            TB = 14.3
            TB_wear = 11
        elif(age_car >= 8):
            TB_wear = 12.6

    if(age_driver<=22):
        if(exp<=3):
            KVS = 1.45
        elif(exp == 4):
            KVS = 1.2
    elif(age_driver>22 and age_driver<=30):
        if(exp<=3):
            KVS = 1.35
        elif(exp>3 and exp<=10):
            KVS = 1
        elif(exp>10):
            KVS = 0.95
    elif(age_driver>30):
        if(exp<=3):
            KVS = 1.3
        elif(exp>3 and exp<=10):
            KVS = 0.95
        elif(exp>=11):
            KVS = 0.9

    if(int(data.number_of_drivers)<=4):
        KD = 1
    else:
        KD = 1.2

    if(data.kmb>=2.3 and data.kmb<=2.45):
        KKL = 1.55
    elif(data.kmb>=1.4 and data.kmb<2.3):
        KKL = 1.20
    elif(data.kmb>=0.95 and data.kmb<1.4):
        KKL = 1
    elif(data.kmb>=0.8 and data.kmb<0.95):
        KKL = 0.95
    elif(data.kmb>=0.7 and data.kmb<0.8):
        KKL = 0.90
    elif(data.kmb>=0.5 and data.kmb<0.7):
        KKL = 0.85

    if(data.number_of_payments == 1):
        KR = 0.95
    elif(data.number_of_payments <=3 and data.number_of_payments >=2):
        KR = 1
    elif(data.number_of_payments >3 and data.number_of_payments <=6):
        KR = 1.1
    elif(data.number_of_payments >6 and data.number_of_payments <=10):
        KR = 1.12

    if(data.insurance_period<12):
        arr = {1: 0.34, 2: 0.4, 3: 0.46, 4: 0.52, 5: 0.58, 6: 0.64, 7: 0.7, 8: 0.76, 9: 0.82, 10: 0.88, 11: 0.94}
        KKR = arr[data.insurance_period]
    else:
        KKR = 1

    if(data.prize_kf>=0.1 and data.prize_kf<=0.3):
        KBM = 1
    elif(data.prize_kf>0.3 and data.prize_kf<=0.7):
        KBM = 1.05
    elif(data.prize_kf>0.7 and data.prize_kf<=1):
        KBM = 1.1
    elif(data.prize_kf>1 and data.prize_kf<=1.5):
        KBM = 1.2
    elif(data.prize_kf>1.5 and data.prize_kf<=2):
        KBM = 1.3

    number_rates = []
    context = {}
    risks = 1
    if(not data.damage):
        risks *= 1.1
    if(not data.accident_caused_by_third_parties):
        risks *= 1.25
    if(not data.accident_caused_by_drivers_of_the_insured_car):
        risks *= 1.52
    if(not data.broken_glass):
        broken_glass = 1.2
    if(not data.unlawful_actions_of_third_parties):
        risks *= 1.1
    if(not data.hijacking):
        risks *= 1.085
    if(data.accident_caused_by_third_parties or data.accident_caused_by_drivers_of_the_insured_car or data.broken_glass or data.unlawful_actions_of_third_parties or data.hijacking or data.damage):
        rates_auto = round(TB * KVS * KD * KKR * KM * KKL *KR*data.anderright_kf/risks, 2)
        full_auto = round(TB * KVS * KD * KKR * KM * KKL *KR*data.anderright_kf, 2)
        full_prise = round(prise_car/100 * full_auto, 2)
        prise_auto = round(prise_car/100 * rates_auto, 2)
        rates_wear_auto = round(TB_wear * KVS * KD * KKR * KM * KKL *KR*data.anderright_kf/risks, 2)
        prise_wear_auto = round(prise_car/100 * rates_wear_auto, 2)

        franz_auto = [[round(prise_car*0.01, 2), round(rates_auto*0.85, 2), round(prise_auto*0.85, 2)],
                    [round(prise_car*0.03, 2), round(rates_auto*0.75, 2), round(prise_auto*0.75, 2)],
                    [round(prise_car*0.05, 2), round(rates_auto*0.70, 2), round(prise_auto*0.7, 2)],
                    [round(prise_car*0.10, 2), round(rates_auto*0.60, 2), round(prise_auto*0.6, 2)],
                    [round(prise_car*0.25, 2), round(rates_auto*0.50, 2), round(prise_auto*0.5, 2)],
                    [round(prise_car*0.50, 2), round(rates_auto*0.45, 2), round(prise_auto*0.45, 2)]]

        number_rates.append('auto')
        franz_wear_auto = [[round(rates_wear_auto*0.85, 2), round(prise_wear_auto*0.85, 2)],
                    [round(rates_wear_auto*0.75, 2), round(prise_wear_auto*0.75, 2)],
                    [round(rates_wear_auto*0.70, 2), round(prise_wear_auto*0.70, 2)],
                    [round(rates_wear_auto*0.60, 2), round(prise_wear_auto*0.60, 2)],
                    [round(rates_wear_auto*0.50, 2), round(prise_wear_auto*0.50, 2)],
                    [round(rates_wear_auto*0.45, 2), round(prise_wear_auto*0.45, 2)]]
        risks = [data.accident_caused_by_third_parties,
                 data.accident_caused_by_drivers_of_the_insured_car,
                 data.damage,
                 data.unlawful_actions_of_third_parties,
                 data.broken_glass,
                 data.hijacking]
        total_damage = [round(rates_auto*0.3, 2), round(prise_auto*0.3, 2), round(prise_wear_auto*0.3, 2)]
        if(total_damage[0]<1.9):
            total_damage[0] = 1.9
        context['total_damage'] = total_damage
        context['prise_car'] = prise_car
        context['number_rates'] = number_rates
        context['name'] = data.name
        context['father_name'] =  data.father_name
        context['familyname'] = data.familyname
        context['brand'] = data.brand
        context['model'] = data.model
        context['car_year'] = data.car_year
            # context['cars'] = user_form
        context['rates'] = rates_auto
        context['prise'] = prise_auto
        context['rates_wear'] = rates_wear_auto
        context['prise_wear'] = prise_wear_auto
        context['franz'] = franz_auto
        context['franz_wear'] = franz_wear_auto
        context['tb'] = TB
        context['kvs'] = KVS
        context['kd'] = KD
        context['kkl'] = KKL
        context['kkr'] = KKR
        context['kr'] = KR
        context['km'] = KM
        context['ander'] = data.anderright_kf
        context['risks'] = risks
            #context['REMOTE_USER'] = request.META["REMOTE_USER"]
            # context['REMOTE_USER'] = HttpRequest.REMOTE_USER

    if(prise_car >= 500000 and prise_car <= 7000000 and age_car <= 10 and data.number_of_drivers <= 4 and data.kmb >=0.5 and data.kmb <= 0.8):
        number_rates.append('new')

        accident_caused_by_third_parties = 1
        accident_caused_by_drivers_of_the_insured_car = 1
        damage = 1
        broken_glass = 1
        unlawful_actions_of_third_parties = 1
        hijacking = 1
        New_risks = 1
        if(data.damage):
            damage = 1.15
            New_risks *= damage
        if(data.accident_caused_by_third_parties):
            accident_caused_by_third_parties = 1.33
            New_risks *= accident_caused_by_third_parties
        if(data.accident_caused_by_drivers_of_the_insured_car):
            accident_caused_by_drivers_of_the_insured_car = 1.45
            New_risks *= accident_caused_by_drivers_of_the_insured_car
        if(data.broken_glass):
            broken_glass = 1.15
            New_risks *= broken_glass
        if(data.unlawful_actions_of_third_parties):
            unlawful_actions_of_third_parties = 1.05
            New_risks *= unlawful_actions_of_third_parties
        if(data.hijacking):
            hijacking = 1.05
            New_risks *= hijacking
        if(age_car <= 3):
            if(prise_car >= 1000000 and prise_car <= 7000000):
                if(data.kmb >= 0.5 and data.kmb <= 0.65):
                    TB_new = 3.5
                    base_tb = 1.18
                elif(data.kmb >= 0.7 and data.kmb <= 0.8):
                    TB_new = 4
                    base_tb = 1.36

            if(prise_car >= 850000 and prise_car <= 999999):
                TB_new = 4
                base_tb = 1.36
        elif(age_car > 3 and age_car <= 5):
            if(data.kmb >= 0.5 and data.kmb <= 0.65):
                TB_new = 4.5
                base_tb = 1.52
            elif(data.kmb >= 0.7 and data.kmb <= 0.8):
                TB_new = 5
                base_tb = 1.69
        print(round(New_risks, 2))
        if(round(New_risks, 2) == 2.81):
            context['rates_new'] = TB_new
            context['prise_new'] = round(prise_car/100 * TB_new, 2)
        else:
            context['rates_new'] = round(base_tb * damage * accident_caused_by_third_parties * accident_caused_by_drivers_of_the_insured_car * broken_glass * unlawful_actions_of_third_parties * hijacking , 1)
            context['prise_new'] = round(prise_car/100 * base_tb * damage * accident_caused_by_third_parties * accident_caused_by_drivers_of_the_insured_car * broken_glass * unlawful_actions_of_third_parties * hijacking, 2)

    if(prise_car >= 500000 and age_car <= 10):
        number_rates.append('tele')
        prise_auto_tele = round(full_prise * full_auto, 2)
        prise = [round(full_prise*0.95, 2),
                     round(full_prise*0.95/2, 2),
                     round(full_prise*0.95/2/5, 2),
                     round(full_prise*0.95/2*0.5, 2),
                     round(full_prise*0.95/2*0.5/5, 2),
                    round((full_prise*0.95/2)+(full_prise*0.95/2*0.5), 2)]

        rates = round(prise[5]/prise_car*100, 2)
        context['start_tele'] = round(prise_auto*0.95, 2)
        context['prise_auto_tele'] = prise_auto
        context['prise_tele'] = prise
        context['rates_tele'] = rates
        context['new_user'] = data
    if(prise_car >= 300000 and age_car <= 5 and data.experience >= 5 and data.driver_age >= 25 and data.insurance_period == 12):
        number_rates.append('luck')
        context['prise_luck'] = round(full_prise * 1.15 / 2, 2)
        context['rates_luck'] = round(full_prise * 1.15 / 2 * 100 / prise_car, 2)
        context['new_user'] = data
    if(prise_car >= 300000 and age_car <= 7 and data.experience >= 5 and data.insurance_period == 12):
        number_rates.append('dia')
        #print("rate_dia = "+str(rate_dia))
        prise_rate = []
            #prise_dia = round(self.prise_car/100 * self.TB * self.KVS * self.KD * self.KBM * self.KKR * self.KR * 1.15 / 2, 2)
            # context['prise_dia'] = rate_dia

        if(prise_car > 300000 and prise_car < 600000):
            prise_rate.append([15000, 5000, prise_car * full_auto/100 - 5000])

        if(prise_car > 300000 and prise_car < 1200000):
            prise_rate.append([20000, 10000, prise_car * full_auto/100 - 10000])

        if(prise_car > 800001 and prise_car < 3000000):
            prise_rate.append([25000, 15000, prise_car * full_auto/100 - 15000])

        if(prise_car > 1000001 and prise_car < 3000000):
            prise_rate.append([40000, 20000, prise_car * full_auto/100 - 20000])

        if(prise_car > 1200001 and prise_car < 5500001):
            prise_rate.append([50000, 30000, prise_car * full_auto/100 - 30000])
        context['insurance_prize_osago'] = data.insurance_prize_osago
        osago_prise = []
        osago_prise.append(data.insurance_prize_osago*0.4)
        osago_prise.append(data.insurance_prize_osago*0.6)
        osago_prise.append(data.insurance_prize_osago*0.8)
        context['osago_prise'] = osago_prise
        context['prise_rate'] = prise_rate
        context['new_user'] = data
    if(data.insurance_prize_osago != 0):
        voluntary = []
        number_rates.append('voluntary')
        voluntary.append(data.insurance_liability)
        if(voluntary[0] == 100000):
            voluntary.append("полис ОСАГО х 0,40 х 1,6")
            voluntary.append(data.insurance_prize_osago)
            voluntary.append(data.insurance_prize_osago*0.4*1.6)
        elif(voluntary[0] == 300000):
            voluntary.append("полис ОСАГО х 0,60 х 1,6")
            voluntary.append(data.insurance_prize_osago)
            voluntary.append(data.insurance_prize_osago*0.6*1.6)
        elif(voluntary[0] == 500000):
            voluntary.append("полис ОСАГО х 0,80 х 1,6")
            voluntary.append(data.insurance_prize_osago)
            voluntary.append(data.insurance_prize_osago*0.8*1.6)
        elif(voluntary[0] == 1000000):
            voluntary.append("полис ОСАГО х 1,0 х 1,6")
            voluntary.append(data.insurance_prize_osago)
            voluntary.append(data.insurance_prize_osago*1.6)
        context['voluntary'] = voluntary
    if(data.insurance_accident != 0):
        health = []
        health.append(data.insurance_places)
        number_rates.append('health')
        if(data.insurance_places == "Водительское" or data.insurance_places == "Переднее правое"):
            health.append(0.65)
            health.append(0.55)
            health.append(data.insurance_accident)
            if(data.insurance_accident > 50000):
                health.append(data.insurance_accident*0.55/100)
            else:
                health.append(data.insurance_accident*0.65/100)
        elif(data.insurance_places == "Оба передних"):
            health.append(1.3)
            health.append(1.1)
            health.append(data.insurance_accident)
            if(data.insurance_accident > 50000):
                health.append(data.insurance_accident*1.1/100)
            else:
                health.append(data.insurance_accident*1.3/100)
        elif(data.insurance_places == "Все задние"):
            health.append(1.95)
            health.append(1.65)
            health.append(data.insurance_accident)
            if(data.insurance_accident > 50000):
                health.append(data.insurance_accident*1.65/100)
            else:
                health.append(data.insurance_accident*1.95/100)
        elif(data.insurance_places == "Все"):
            health.append(2.93)
            health.append(2.48)
            health.append(data.insurance_accident)
            if(data.insurance_accident > 50000):
                health.append(data.insurance_accident*2.48/100)
            else:
                health.append(data.insurance_accident*2.93/100)
        context['health'] = health
            # context['rates_dia'] = round(self.prise_car/100 * self.TB * self.KVS * self.KD * self.KBM * self.KKR * self.KR * 1.15 / 2 * 100 / self.bound_cars_form.cleaned_data['insurance_amount'], 2)
    # return render(request, 'calculator/answer.html', context)
    # return render(request, 'calculator/NoRate.html')
    return context
def Payment(request, data):
        # self.new_user = self.data.save(commit = False)
        # self.new_user = self.data
    age_car = datetime.datetime.now().year - data.cleaned_data['car_year']
    if(data.cleaned_data['class_master'] == 2):
        KM = 1
    else:
        if(age_car > 5):
            KM = 1.3
        else:
            KM = 1
    prise_car = data.cleaned_data['insurance_amount']
    age_driver = data.cleaned_data['driver_age']
    exp = data.cleaned_data['experience']
    TB_wear = 0
    TB = 0
    if(prise_car>999999):
        if(age_car <= 3):
            TB = 6
        elif(age_car > 3 and age_car <=5):
            TB = 7.6
            TB_wear = 6.4
        elif(age_car > 5 and age_car <=7):
            TB = 11
            TB_wear = 7.8
        elif(age_car >= 8):
            TB_wear = 11
    elif(prise_car>650000 and prise_car<1000000):
        if(age_car <= 3):
            TB = 6.7
        elif(age_car > 3 and age_car <=5):
            TB = 8.1
            TB_wear = 7.1
        elif(age_car > 5 and age_car <=7):
            TB = 11
            TB_wear = 7.6
        elif(age_car >= 8):
            TB_wear = 11
    elif(prise_car>300000 and prise_car<=650000):
        if(age_car <= 3):
            TB = 8
        elif(age_car > 3 and age_car <=5):
            TB = 9
            TB_wear = 8.1
        elif(age_car > 5 and age_car <=7):
            TB = 12
            TB_wear = 8.4
        elif(age_car >= 8):
            TB_wear = 13.1
    elif(prise_car<=300000):
        if(age_car <= 3):
            TB = 9.3
        elif(age_car > 3 and age_car <=5):
            TB = 11
            TB_wear = 9
        elif(age_car > 5 and age_car <=7):
            TB = 14.3
            TB_wear = 11
        elif(age_car >= 8):
            TB_wear = 12.6

    if(age_driver<=22):
        if(exp<=3):
            KVS = 1.45
        elif(exp == 4):
            KVS = 1.2
    elif(age_driver>22 and age_driver<=30):
        if(exp<=3):
            KVS = 1.35
        elif(exp>3 and exp<=10):
            KVS = 1
        elif(exp>10):
            KVS = 0.95
    elif(age_driver>30):
        if(exp<=3):
            KVS = 1.3
        elif(exp>3 and exp<=10):
            KVS = 0.95
        elif(exp>=11):
            KVS = 0.9

    if(data.cleaned_data['number_of_drivers']<=4):
        KD = 1
    else:
        KD = 1.2

    if(data.cleaned_data['kmb']>=2.3 and data.cleaned_data['kmb']<=2.45):
        KKL = 1.55
    elif(data.cleaned_data['kmb']>=1.4 and data.cleaned_data['kmb']<2.3):
        KKL = 1.20
    elif(data.cleaned_data['kmb']>=0.95 and data.cleaned_data['kmb']<1.4):
        KKL = 1
    elif(data.cleaned_data['kmb']>=0.8 and data.cleaned_data['kmb']<=0.9):
        KKL = 0.95
    elif(data.cleaned_data['kmb']>=0.7 and data.cleaned_data['kmb']<=0.75):
        KKL = 0.90
    elif(data.cleaned_data['kmb']>=0.5 and data.cleaned_data['kmb']<=0.65):
        KKL = 0.85

    if(data.cleaned_data['number_of_payments'] == 1):
        KR = 0.95
    elif(data.cleaned_data['number_of_payments']<=3 and data.cleaned_data['number_of_payments']>=2):
        KR = 1
    elif(data.cleaned_data['number_of_payments']>3 and data.cleaned_data['number_of_payments']<=6):
        KR = 1.1
    elif(data.cleaned_data['number_of_payments']>6 and data.cleaned_data['number_of_payments']<=10):
        KR = 1.12

    if(data.cleaned_data['insurance_period']<12):
        arr = {1: 0.34, 2: 0.4, 3: 0.46, 4: 0.52, 5: 0.58, 6: 0.64, 7: 0.7, 8: 0.76, 9: 0.82, 10: 0.88, 11: 0.94}
        KKR = arr[data.cleaned_data['insurance_period']]
    else:
        KKR = 1

    if(data.cleaned_data['prize_kf']>=0.1 and data.cleaned_data['prize_kf']<=0.3):
        KBM = 1
    elif(data.cleaned_data['prize_kf']>0.3 and data.cleaned_data['prize_kf']<=0.7):
        KBM = 1.05
    elif(data.cleaned_data['prize_kf']>0.7 and data.cleaned_data['prize_kf']<=1):
        KBM = 1.1
    elif(data.cleaned_data['prize_kf']>1 and data.cleaned_data['prize_kf']<=1.5):
        KBM = 1.2
    elif(data.cleaned_data['prize_kf']>1.5 and data.cleaned_data['prize_kf']<=2):
        KBM = 1.3

    number_rates = []
    context = {}
    risks = 1
    if(not data.cleaned_data['damage']):
        risks *= 1.1
    if(not data.cleaned_data['accident_caused_by_third_parties']):
        risks *= 1.25
    if(not data.cleaned_data['accident_caused_by_drivers_of_the_insured_car']):
        risks *= 1.52
    if(not data.cleaned_data['broken_glass']):
        broken_glass = 1.2
    if(not data.cleaned_data['unlawful_actions_of_third_parties']):
        risks *= 1.1
    if(not data.cleaned_data['hijacking']):
        risks *= 1.085
    if(data.cleaned_data['accident_caused_by_third_parties'] or data.cleaned_data['accident_caused_by_drivers_of_the_insured_car'] or data.cleaned_data['broken_glass'] or data.cleaned_data['unlawful_actions_of_third_parties'] or data.cleaned_data['hijacking'] or data.cleaned_data['damage']):
        rates_auto = round(TB * KVS * KD * KKR * KM * KKL *KR*data.cleaned_data['anderright_kf']/risks, 2)
        full_auto = round(TB * KVS * KD * KKR * KM * KKL *KR*data.cleaned_data['anderright_kf'], 2)
        full_prise = round(prise_car/100 * full_auto, 2)
        prise_auto = round(prise_car/100 * rates_auto, 2)
        rates_wear_auto = round(TB_wear * KVS * KD * KKR * KM * KKL *KR*data.cleaned_data['anderright_kf']/risks, 2)
        prise_wear_auto = round(prise_car/100 * rates_wear_auto, 2)

        franz_auto = [[round(prise_car*0.01, 2), round(rates_auto*0.85, 2), round(prise_auto*0.85, 2)],
                    [round(prise_car*0.03, 2), round(rates_auto*0.75, 2), round(prise_auto*0.75, 2)],
                    [round(prise_car*0.05, 2), round(rates_auto*0.70, 2), round(prise_auto*0.7, 2)],
                    [round(prise_car*0.10, 2), round(rates_auto*0.60, 2), round(prise_auto*0.6, 2)],
                    [round(prise_car*0.25, 2), round(rates_auto*0.50, 2), round(prise_auto*0.5, 2)],
                    [round(prise_car*0.50, 2), round(rates_auto*0.45, 2), round(prise_auto*0.45, 2)]]

        number_rates.append('auto')
        franz_wear_auto = [[round(rates_wear_auto*0.85, 2), round(prise_wear_auto*0.85, 2)],
                    [round(rates_wear_auto*0.75, 2), round(prise_wear_auto*0.75, 2)],
                    [round(rates_wear_auto*0.70, 2), round(prise_wear_auto*0.70, 2)],
                    [round(rates_wear_auto*0.60, 2), round(prise_wear_auto*0.60, 2)],
                    [round(rates_wear_auto*0.50, 2), round(prise_wear_auto*0.50, 2)],
                    [round(rates_wear_auto*0.45, 2), round(prise_wear_auto*0.45, 2)]]
        risks = [data.cleaned_data['accident_caused_by_third_parties'],
                 data.cleaned_data['accident_caused_by_drivers_of_the_insured_car'],
                 data.cleaned_data['damage'],
                 data.cleaned_data['unlawful_actions_of_third_parties'],
                 data.cleaned_data['broken_glass'],
                 data.cleaned_data['hijacking']]
        total_damage = [round(rates_auto*0.3, 2), round(prise_auto*0.3, 2), round(prise_wear_auto*0.3, 2)]
        if(total_damage[0]<1.9):
            total_damage[0] = 1.9

        context['total_damage'] = total_damage
        context['prise_car'] = prise_car
        context['number_rates'] = number_rates
        context['name'] = data.cleaned_data['name']
        context['father_name'] =  data.cleaned_data['father_name']
        context['familyname'] = data.cleaned_data['familyname']
        context['brand'] = data.cleaned_data['brand']
        context['model'] = data.cleaned_data['model']
        context['car_year'] = data.cleaned_data['car_year']
            # context['cars'] = user_form
        context['rates'] = rates_auto
        context['prise'] = prise_auto
        context['rates_wear'] = rates_wear_auto
        context['prise_wear'] = prise_wear_auto
        context['franz'] = franz_auto
        context['franz_wear'] = franz_wear_auto
        context['tb'] = TB
        context['kvs'] = KVS
        context['kd'] = KD
        context['kkl'] = KKL
        context['kkr'] = KKR
        context['kr'] = KR
        context['km'] = KM
        context['ander'] = data.cleaned_data['anderright_kf']
        context['risks'] = risks

            #context['REMOTE_USER'] = request.META["REMOTE_USER"]
            # context['REMOTE_USER'] = HttpRequest.REMOTE_USER

    if(prise_car >= 500000 and prise_car <= 7000000 and age_car <= 10 and data.cleaned_data['number_of_drivers'] <= 4 and data.cleaned_data['kmb'] >=0.5 and data.cleaned_data['kmb'] <= 0.8):
        number_rates.append('new')

        accident_caused_by_third_parties = 1
        accident_caused_by_drivers_of_the_insured_car = 1
        damage = 1
        broken_glass = 1
        unlawful_actions_of_third_parties = 1
        hijacking = 1

        if(data.cleaned_data['damage']):
            damage = 1.15
        if(data.cleaned_data['accident_caused_by_third_parties']):
            accident_caused_by_third_parties = 1.33
        if(data.cleaned_data['accident_caused_by_drivers_of_the_insured_car']):
            accident_caused_by_drivers_of_the_insured_car = 1.45
        if(data.cleaned_data['broken_glass']):
            broken_glass = 1.15
        if(data.cleaned_data['unlawful_actions_of_third_parties']):
            unlawful_actions_of_third_parties = 1.05
        if(data.cleaned_data['hijacking']):
            hijacking = 1.05

        if(age_car <= 3):
            if(prise_car >= 1000000 and prise_car <= 7000000):
                if(data.cleaned_data['kmb'] >= 0.5 and data.cleaned_data['kmb'] <= 0.65):
                    TB_new = 3.5
                    base_tb = 1.18
                elif(data.cleaned_data['kmb'] >= 0.7 and data.cleaned_data['kmb'] <= 0.8):
                    TB_new = 4
                    base_tb = 1.36

            if(prise_car >= 850000 and prise_car <= 999999):
                TB_new = 4
                base_tb = 1.36
        elif(age_car > 3 and age_car <= 5):
            if(data.cleaned_data['kmb'] >= 0.5 and data.cleaned_data['kmb'] <= 0.65):
                TB_new = 4.5
                base_tb = 1.52
            elif(data.cleaned_data['kmb'] >= 0.7 and data.cleaned_data['kmb'] <= 0.8):
                TB_new = 5
                base_tb = 1.69


        context['rates_new'] = round(base_tb * damage * accident_caused_by_third_parties * accident_caused_by_drivers_of_the_insured_car * broken_glass * unlawful_actions_of_third_parties * hijacking , 1)
        context['prise_new'] = round(prise_car/100 * base_tb * damage * accident_caused_by_third_parties * accident_caused_by_drivers_of_the_insured_car * broken_glass * unlawful_actions_of_third_parties * hijacking, 2)

    if(prise_car >= 500000 and age_car <= 10):
        number_rates.append('tele')
        prise_auto_tele = round(full_prise, 2)
        prise = [round(full_prise*0.95, 2),
                     round(full_prise*0.95/2, 2),
                     round(full_prise*0.95/2/5, 2),
                     round(full_prise*0.95/2*0.5, 2),
                     round(full_prise*0.95/2*0.5/5, 2),
                    round((full_prise*0.95/2)+(full_prise*0.95/2*0.5), 2)]

        rates = round(prise[5]/prise_car*100, 2)
        context['start_tele'] = round(full_prise*0.95, 2)
        context['prise_auto_tele'] = full_prise
        context['prise_tele'] = prise
        context['rates_tele'] = rates
        context['new_user'] = data
    if(prise_car >= 300000 and age_car <= 5 and data.cleaned_data['experience'] >= 5 and data.cleaned_data['driver_age'] >= 25 and data.cleaned_data['insurance_period'] == 12):
        number_rates.append('luck')
        context['prise_luck'] = round(full_prise * 1.15 / 2, 2)
        context['rates_luck'] = round(full_prise * 1.15 / 2 * 100 / prise_car, 2)
        context['new_user'] = data
    if(prise_car >= 300000 and age_car <= 7 and data.cleaned_data['experience'] >= 5 and data.cleaned_data['insurance_period'] == 12):
        number_rates.append('dia')
        prise_rate = []
            #prise_dia = round(self.prise_car/100 * self.TB * self.KVS * self.KD * self.KBM * self.KKR * self.KR * 1.15 / 2, 2)
            # context['prise_dia'] = rate_dia
        if(prise_car > 300000 and prise_car < 600000):
            prise_rate.append([15000, 5000, prise_car * full_auto/100 - 5000])

        if(prise_car > 300000 and prise_car < 1200000):
            prise_rate.append([20000, 10000, prise_car * full_auto/100 - 10000])

        if(prise_car > 800001 and prise_car < 3000000):
            prise_rate.append([25000, 15000, prise_car * full_auto/100 - 15000])

        if(prise_car > 1000001 and prise_car < 3000000):
            prise_rate.append([40000, 20000, prise_car * full_auto/100 - 20000])

        if(prise_car > 1200001 and prise_car < 5500001):
            prise_rate.append([50000, 30000, prise_car * full_auto/100 - 30000])

        context['insurance_prize_osago'] = data.cleaned_data['insurance_prize_osago']
        osago_prise = []
        osago_prise.append(data.cleaned_data['insurance_prize_osago']*0.4)
        osago_prise.append(data.cleaned_data['insurance_prize_osago']*0.6)
        osago_prise.append(data.cleaned_data['insurance_prize_osago']*0.8)
        context['osago_prise'] = osago_prise
        context['prise_rate'] = prise_rate
        context['new_user'] = data

        if(data.cleaned_data['insurance_prize_osago'] != 0):
            voluntary = []
            number_rates.append('voluntary')
            voluntary.append(data.cleaned_data['insurance_liability'])
            if(voluntary[0] == 100000):
                voluntary.append("полис ОСАГО х 0,40 х 1,6")
                voluntary.append(data.cleaned_data['insurance_prize_osago'])
                voluntary.append(data.cleaned_data['insurance_prize_osago']*0.4*1.6)
            elif(voluntary[0] == 300000):
                voluntary.append("полис ОСАГО х 0,60 х 1,6")
                voluntary.append(data.cleaned_data['insurance_prize_osago'])
                voluntary.append(data.cleaned_data['insurance_prize_osago']*0.6*1.6)
            elif(voluntary[0] == 500000):
                voluntary.append("полис ОСАГО х 0,80 х 1,6")
                voluntary.append(data.cleaned_data['insurance_prize_osago'])
                voluntary.append(data.cleaned_data['insurance_prize_osago']*0.8*1.6)
            elif(voluntary[0] == 1000000):
                voluntary.append("полис ОСАГО х 1,0 х 1,6")
                voluntary.append(data.cleaned_data['insurance_prize_osago'])
                voluntary.append(data.cleaned_data['insurance_prize_osago']*1.6)
            context['voluntary'] = voluntary
        if(data.cleaned_data['insurance_accident'] != 0):
            health = []
            health.append(data.cleaned_data['insurance_places'])
            number_rates.append('health')
            if(data.cleaned_data['insurance_places'] == "Водительское" or data.cleaned_data['insurance_places'] == "Переднее правое"):
                health.append(0.65)
                health.append(0.55)
                health.append(data.cleaned_data['insurance_accident'])
                if(data.cleaned_data['insurance_accident'] > 50000):
                    health.append(data.cleaned_data['insurance_accident']*0.55/100)
                else:
                    health.append(data.cleaned_data['insurance_accident']*0.65/100)
            elif(data.cleaned_data['insurance_places'] == "Оба передних"):
                health.append(1.3)
                health.append(1.1)
                health.append(data.cleaned_data['insurance_accident'])
                if(data.cleaned_data['insurance_accident'] > 50000):
                    health.append(data.cleaned_data['insurance_accident']*1.1/100)
                else:
                    health.append(data.cleaned_data['insurance_accident']*1.3/100)
            elif(data.cleaned_data['insurance_places'] == "Все задние"):
                health.append(1.95)
                health.append(1.65)
                health.append(data.cleaned_data['insurance_accident'])
                if(data.cleaned_data['insurance_accident'] > 50000):
                    health.append(data.cleaned_data['insurance_accident']*1.65/100)
                else:
                    health.append(data.cleaned_data['insurance_accident']*1.95/100)
            elif(data.cleaned_data['insurance_places'] == "Все"):
                health.append(2.93)
                health.append(2.48)
                health.append(data.cleaned_data['insurance_accident'])
                if(data.cleaned_data['insurance_accident'] > 50000):
                    health.append(data.cleaned_data['insurance_accident']*2.48/100)
                else:
                    health.append(data.cleaned_data['insurance_accident']*2.93/100)
            context['health'] = health
            # context['rates_dia'] = round(self.prise_car/100 * self.TB * self.KVS * self.KD * self.KBM * self.KKR * self.KR * 1.15 / 2 * 100 / self.bound_cars_form.cleaned_data['insurance_amount'], 2)
    # return render(request, 'calculator/answer.html', context)
    # return render(request, 'calculator/NoRate.html')
    return context

class OptionsCreate(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserForm()
        context = {'user_form': user_form}

        return render(request, 'calculator/options.html', context)

    def post(self, request):
        self.data = UserForm(request.POST)
        if(self.data.is_valid()):
            if(not Cheking(request.POST.get("accident_caused_by_third_parties"))
                and not Cheking(request.POST.get("accident_caused_by_drivers_of_the_insured_car"))
                and not Cheking(request.POST.get("damage"))
                and not Cheking(request.POST.get("broken_glass"))
                and not Cheking(request.POST.get("unlawful_actions_of_third_parties"))
                and Cheking(request.POST.get("hijacking"))
                and not Cheking(request.POST.get("total_damage"))):
                return HttpResponse("<h1>Ошибка: выбрано только хищение</h1>")
            if(not Cheking(request.POST.get("accident_caused_by_third_parties"))
                and not Cheking(request.POST.get("accident_caused_by_drivers_of_the_insured_car"))
                and not Cheking(request.POST.get("damage"))
                and not Cheking(request.POST.get("broken_glass"))
                and not Cheking(request.POST.get("unlawful_actions_of_third_parties"))
                and not Cheking(request.POST.get("hijacking"))
                and not Cheking(request.POST.get("total_damage"))):
                return HttpResponse("<h1>Ошибка: Ничего не выбрано</h1>")
            if(self.data.cleaned_data['number_of_payments'] == 1):
                self.data.cleaned_data['at_a_time'] = True
                self.data.cleaned_data['installment_plan'] = False
            else:
                self.data.cleaned_data['at_a_time'] = False
                self.data.cleaned_data['installment_plan'] = True
            # author = self.data.save(commit = False)
            # author.admin = request.user
            # author.date = datetime.datetime.now()
            # author.save()
            # self.data.save()
            if("Payment" in request.POST):
                context = Payment(request, self.data)
                return render(request, 'calculator/answer.html', context)
            elif("SavePay" in request.POST):
                insuranse = Policyholder.objects.create(
                status = "Черновик",
                name = self.data.cleaned_data["name"],
                familyname = self.data.cleaned_data["familyname"],
                father_name = self.data.cleaned_data["father_name"],
                driver_age = self.data.cleaned_data["driver_age"],
                experience = self.data.cleaned_data["experience"],
                admin = request.user,
                brand = self.data.cleaned_data["brand"],
                model = self.data.cleaned_data["model"],
                number_of_drivers = self.data.cleaned_data["number_of_drivers"],
                kmb = self.data.cleaned_data["kmb"],
                date = datetime.datetime.now(),
                car_year = self.data.cleaned_data["car_year"],
                insurance_amount = self.data.cleaned_data["insurance_amount"],
                class_master = self.data.cleaned_data["class_master"],
                accident_caused_by_third_parties = Cheking(self.data.cleaned_data["accident_caused_by_third_parties"]),
                accident_caused_by_drivers_of_the_insured_car = Cheking(self.data.cleaned_data["accident_caused_by_drivers_of_the_insured_car"]),
                damage = Cheking(self.data.cleaned_data["damage"]),
                broken_glass = Cheking(self.data.cleaned_data["broken_glass"]),
                unlawful_actions_of_third_parties = Cheking(self.data.cleaned_data["unlawful_actions_of_third_parties"]),
                hijacking = Cheking(self.data.cleaned_data["hijacking"]),
                total_damage = Cheking(self.data.cleaned_data["total_damage"]),
                at_a_time = self.data.cleaned_data['at_a_time'],
                installment_plan = self.data.cleaned_data['installment_plan'],
                number_of_payments = self.data.cleaned_data["number_of_payments"],
                insurance_period = self.data.cleaned_data["insurance_period"],
                prize_kf = self.data.cleaned_data["prize_kf"],
                anderright_kf = self.data.cleaned_data["anderright_kf"],
                insurance_liability = self.data.cleaned_data["insurance_liability"],
                insurance_prize_osago = self.data.cleaned_data["insurance_prize_osago"],
                insurance_accident = self.data.cleaned_data["insurance_accident"],
                insurance_places = self.data.cleaned_data["insurance_places"],
                )

                Record.objects.create(admin = request.user,
                                      action = "Редактирование записи",
                                      date = datetime.datetime.now(),
                                      act_id = Policyholder.objects.get(id=insuranse.id))
                # insuranse.save()
                bound_form = UserForm()
                context = {'user_form': bound_form,
                            'data': insuranse,
                            'user_id': insuranse.id
                            }
                return HttpResponse("<h4>Успешно сохранено</h4>")
                # return HttpResponse("<h4>Успешно сохранено</h4>")
        else:
            context = {'options_user_form': data}
            return render(request, 'calculator/options.html', context)



class Check_record(LoginRequiredMixin, View):
    def get(self, request, id):
        # num = request.GET.get('num')
        # num = request.META['QUERY_STRING'][4:].split()
        print(id)
        data = Policyholder.objects.get(id=id)
        bound_form = UserForm()
        context = {'user_form': bound_form,
                    'data': data,
                    'user_id': id
                    }
        return render(request, 'calculator/edit.html', context)

    def post(self, request, id):
        if(not Cheking(request.POST.get("accident_caused_by_third_parties"))
            and not Cheking(request.POST.get("accident_caused_by_drivers_of_the_insured_car"))
            and not Cheking(request.POST.get("damage"))
            and not Cheking(request.POST.get("broken_glass"))
            and not Cheking(request.POST.get("unlawful_actions_of_third_parties"))
            and Cheking(request.POST.get("hijacking"))
            and not Cheking(request.POST.get("total_damage"))):
            return HttpResponse("<h1>Ошибка: выбрано только хищение</h1>")

        if(not Cheking(request.POST.get("accident_caused_by_third_parties"))
            and not Cheking(request.POST.get("accident_caused_by_drivers_of_the_insured_car"))
            and not Cheking(request.POST.get("damage"))
            and not Cheking(request.POST.get("broken_glass"))
            and not Cheking(request.POST.get("unlawful_actions_of_third_parties"))
            and not Cheking(request.POST.get("hijacking"))
            and not Cheking(request.POST.get("total_damage"))):
            return HttpResponse("<h1>Ошибка: Ничего не выбрано</h1>")

        data = Policyholder.objects.get(id=id)
        data.name = request.POST.get("name")
        data.familyname = request.POST.get("familyname")
        data.father_name = request.POST.get("father_name")
        data.brand = request.POST.get("brand")
        data.model = request.POST.get("model")
        data.car_year = request.POST.get("car_year")
        data.insurance_amount = request.POST.get("insurance_amount")
        data.class_master = request.POST.get("class_master")
        data.driver_age = request.POST.get("driver_age")
        data.experience = request.POST.get("experience")
        data.number_of_drivers = request.POST.get("number_of_drivers")
        data.kmb = request.POST.get("kmb")
        data.accident_caused_by_third_parties = Cheking(request.POST.get("accident_caused_by_third_parties"))
        data.accident_caused_by_drivers_of_the_insured_car = Cheking(request.POST.get("accident_caused_by_drivers_of_the_insured_car"))
        data.damage = Cheking(request.POST.get("damage"))
        data.broken_glass = Cheking(request.POST.get("broken_glass"))
        data.unlawful_actions_of_third_parties = Cheking(request.POST.get("unlawful_actions_of_third_parties"))
        data.hijacking = Cheking(request.POST.get("hijacking"))
        data.total_damage = Cheking(request.POST.get("total_damage"))
        data.number_of_payments = request.POST.get("number_of_payments")

        if(data.number_of_payments == 1):
            data.at_a_time = True
        else:
            data.at_a_time = False

        data.insurance_period = request.POST.get("insurance_period")
        data.prize_kf = request.POST.get("prize_kf")
        data.anderright_kf = request.POST.get("anderright_kf")
        data.insurance_liability = request.POST.get("insurance_liability")
        data.insurance_prize_osago = request.POST.get("insurance_prize_osago")
        data.insurance_accident = request.POST.get("insurance_accident")
        data.insurance_places = request.POST.get("insurance_places")
        if("Payment" in request.POST):
            context = Payment_check(request, data)
            context['user_id'] = id
            return render(request, 'calculator/answer.html', context)
        elif("UpdatePay" in request.POST):
            Record.objects.create(admin = request.user,
                                  action = "Редактирование записи",
                                  date = datetime.datetime.now(),
                                  act_id = Policyholder.objects.get(id=id))
            data.save()
            return HttpResponse("<h4>Успешно сохранено</h4>")
        # data = UserForm(request.POST)
        # context = {'user_form': data}
        # return render(request, 'calculator/options.html', context)
    # data.save()
# def Check_Record(request, id):
#     print(id)
#     data = Policyholder.objects.get(id=19)
#     bound_form = UserForm()
#     context = {'user_form': bound_form,
#                 'data': data,
#                 }
#     return render(request, 'calculator/options.html', context)
