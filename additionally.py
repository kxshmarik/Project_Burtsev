"""
Вспомогательные функции
"""

from cryptography import x509


def format_name(name):
    """Форматировать имя для вывода"""
    try:
        result = ""
        for attr in name:
            # Берем только первые части, чтобы не перегружать вывод
            nazvanie = attr.oid._name
            znachenie = attr.value
            
            # Сокращаем длинные значения
            if len(znachenie) > 30:
                znachenie = znachenie[:27] + "..."
            
            result += f"{nazvanie}={znachenie}, "
        return result.rstrip(", ")
    except:
        return "Неизвестно"


def format_data(data_s_time):
    """Форматировать дату без часового пояса"""
    try:
        # Убираем часовой пояс для более крпаткого и понятного вывода
        return str(data_s_time).split('+')[0]
    except:
        return str(data_s_time)


def pokazat_rezultat(info):
    """Показать результат проверки"""
    print(f"\nОСНОВНАЯ ИНФОРМАЦИЯ:")
    print(f"  Владелец: {info['vladelets']}")
    print(f"  Издатель: {info['izdatel']}")
    
    print(f"\nСРОК ДЕЙСТВИЯ:")
    print(f"  Действителен с: {format_data(info['s_kakogo'])}")
    print(f"  Действителен до: {format_data(info['do_kakogo'])}")
    print(f"  Осталось дней: {info['ostalos_dney']}")
    
    print(f"\nСТАТУС: {info['status']}")


def dat_rekomendaciyu(info):
    """Рекомендацию по сертификату"""
    print(f"\nРЕКОМЕНДАЦИЯ:")
    
    if info['esli_prosrochen']:
        print(f"  Сертификат необходимо обновить!")
    elif info['ostalos_dney'] < 7:
        print(f"  Очень мало дней ({info['ostalos_dney']}), нужно обновить")
    elif info['ostalos_dney'] < 30:
        print(f"  Мало дней ({info['ostalos_dney']}), скоро нужно будет обновить")
    else:
        print(f"  Все хорошо, еще много дней ({info['ostalos_dney']})")