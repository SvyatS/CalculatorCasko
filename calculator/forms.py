# Объявляем поля формы <Страховой расчёт> для страницы ----- http://127.0.0.1:8000/options/
# Поля перечислены в порядке следования на странице
# Задаем для каждого поля характеристики (длина, макс., мин....)


from django import forms
from .models import *
import datetime

class UserForm(forms.ModelForm):
    class Meta:
        model = Policyholder
        choices1 = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13))
        choices2 = ((100000, 100000), (300000, 300000), (500000, 500000), (1000000, 1000000))
        choices3 = (("Водительское", "Водительское"), ("Переднее правое", "Переднее правое"), ("Оба передних", "Оба передних"), ("Все задние", "Все задние"), ("Все", "Все"))
        fields = ['name',                                              # Страхователь,            Имя
                  'familyname',                                        # Страхователь,            Фамилия
                  'father_name',                                       # Страхователь,            Отчество

                  'brand',                                             # Транспортное средство,   Марка
                  'model',                                             # Транспортное средство,   Модель
                  'car_year',                                          # Транспортное средство,   Год выпуска
                  'insurance_amount',                                  # Транспортное средство,   Страховая сумма
                  'class_master',                                      # Транспортное средство,   Класс автомастерской

                  'driver_age',                                        # Водители,                Возраст
                  'experience',                                        # Водители,                Стаж
                  'number_of_drivers',                                 # Водители,                Число водителей
                  'kmb',                                               # Водители,                КМБ

                  'accident_caused_by_third_parties',                  # Страховые риски,         ДТП по вине третьих лиц
                  'accident_caused_by_drivers_of_the_insured_car',     # Страховые риски,         ДТП по вине водителей застрахованного ТС
                  'damage',
                  'broken_glass',                                      # Страховые риски,         Бой стекол ТС
                  'unlawful_actions_of_third_parties',                 # Страховые риски,         Противоправные действия третьих лиц
                  'hijacking',                                         # Страховые риски,         Хищение
                  'total_damage',

                  'at_a_time',                                         # Варианты оплаты,         Единовременно
                  'number_of_payments',                                # Варианты оплаты,         Рассрочка

                  'insurance_period',                                  # Варианты оплаты,         Срок страхования
                  'prize_kf',                                          # Варианты оплаты,         Коэффициент соотношения выплат к премиям
                  'anderright_kf',                                     # Варианты оплаты,         Андереррайтерский коэффициент
                  'insurance_liability',
                  'insurance_prize_osago',                             # Добровольное страхование гражданской ответственности,    Страховая премия по ОСАГО
                  'insurance_accident',
                  'insurance_places']

        widgets = {
        # 'status': forms.RadioSelect(attrs={'class':'form-control'}),
        'name'                 : forms.TextInput(attrs={'class':'form-control'}),
        'familyname'           : forms.TextInput(attrs={'class':'form-control'}),
        'father_name'          : forms.TextInput(attrs={'class':'form-control'}),
        'brand'                : forms.TextInput(attrs={'class':'form-control'}),
        'model'                : forms.TextInput(attrs={'class':'form-control'}),
        'car_year'             : forms.NumberInput(attrs={'class':'form-control', 'min': '1960', 'max': str(datetime.datetime.now().year), "onKeyPress":"cislo()"}),
        'insurance_amount'     : forms.NumberInput(attrs={'class':'form-control', 'min': '100000', 'max': '20000000', "onKeyPress":"cislo()"}),
        'class_master'         : forms.Select(choices= ((2, 2), (3, 3)), attrs={'class':'form-control', 'style': 'width: 70px;'}),
        'driver_age'           : forms.NumberInput(attrs={'class':'form-control', 'min': '18', 'max': '100',   "onKeyPress":"cislo()"}),
        'experience'           : forms.NumberInput(attrs={'class':'form-control', 'min': '0', 'max': '82',     "onKeyPress":"cislo()"}),
        'number_of_drivers'    : forms.NumberInput(attrs={'class':'form-control', 'min': '0', 'max': '10',     "onKeyPress":"cislo()"}),
        'kmb'                  : forms.NumberInput(attrs={'class':'form-control', 'min': '0.5', 'max': '2.45'}),
        'accident_caused_by_third_parties'             : forms.CheckboxInput(attrs={'class':'qwe'}),
        'accident_caused_by_drivers_of_the_insured_car': forms.CheckboxInput(attrs={'class':'qwe'}),
        'damage'                                       : forms.CheckboxInput(attrs={'class':'qwe'}),
        'broken_glass'                                 : forms.CheckboxInput(attrs={'class':'qwe'}),
        'unlawful_actions_of_third_parties'            : forms.CheckboxInput(attrs={'class':'qwe'}),
        'hijacking'            : forms.CheckboxInput(attrs={'class':'qwe'}),
        'total_damage'         : forms.CheckboxInput(),
        'at_a_time'            : forms.RadioSelect(choices= (("Единовременно", "Единовременно"), ("Рассрочка", "Рассрочка")), attrs={'class':'form-check-input'}),
        'number_of_payments'   : forms.NumberInput(attrs={'class':'form-control', 'min': '1', 'max': '10', 'value': '1', "onKeyPress":"cislo()"}),
        'insurance_period'     : forms.Select(choices=choices1, attrs={'class':'form-control', "placeholder": ".col-xs-2"}),
        'prize_kf'             : forms.NumberInput(attrs={'class':'form-control', 'min': '0.1', 'max': '2', 'value': '1', "onKeyPress":"cislo()"}),
        'anderright_kf'        : forms.NumberInput(attrs={'class':'form-control', 'min': '0.5', 'max': '10', 'value': '1'}),
        'insurance_liability'  : forms.Select(choices=choices2, attrs={'class':'form-control'}),
        'insurance_prize_osago': forms.NumberInput(attrs={'class':'form-control', 'min': '0', 'max': '1000000', 'required': False, 'value': 0, "onKeyPress":"cislo()"}),
        'insurance_accident'   : forms.NumberInput(attrs={'class':'form-control', 'min': '0', 'max': '1000000', 'required': False, 'value': 0, "onKeyPress":"cislo()"}),
        'insurance_places'     : forms.Select(choices=choices3, attrs={'class':'form-control', 'style': 'width: 230px;'})
        }
