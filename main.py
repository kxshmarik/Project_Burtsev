"""
Начало (командная строка)
"""

import sys
from ssl_checker import ProverkaSSLCert


def obrabotka_odin(sait, test_chain):
    """Обработка одного сайта"""
    proverka = ProverkaSSLCert()
    return proverka.pokazat_info(sait, test_chain)


def obrabotka_mnogo(saity):
    """ОБработка нескольких сайтов"""
    print(f"\nПАКЕТНАЯ ПРОВЕРКА {len(saity)} САЙТОВ:")
    print(f"{'='*50}")
    
    proverka = ProverkaSSLCert()
    vsego = 0
    ok = 0
    neok = 0
    
    for i, sajt in enumerate(saity, 1):
        print(f"\n{i}. {sajt}")
        vsego += 1
        
        cert = proverka.poluchit_cert(sajt)
        
        if cert:
            info = proverka.proverit_srok(cert)
            if info and not info['esli_prosrochen'] and not info['esli_rano']:
                print(f"     OK (осталось {info['ostalos_dney']} дней)")
                ok += 1
            else:
                print(f"     ПРОБЛЕМА")
                neok += 1
        else:
            print(f"     ОШИБКА")
            neok += 1
    
    # Статистика
    print(f"\n{'='*50}")
    print(f"СТАТИСТИКА:")
    print(f"  Всего проверено: {vsego}")
    print(f"  Всё хорошо: {ok}")
    print(f"  Осталось мало дней: {neok}")


def spravka():
    """Справка"""
    print("Использование в командной строке:")
    print("  python <путь>ssl_checker.py <сайт>")
    print("  python <путь>ssl_checker <сайт> --c")
    print("  python <путь>ssl_checker <сайт1> <сайт2> ...")
    print("Примеры:")
    print("  python /Users/Burtsev/Downloads/Project_Burtsev/ssl_checker google.com")
    print("  python /Users/Burtsev/Downloads/Project_Burtsev/ssl_checker github.com --c")
    print("  python /Users/Burtsev/Downloads/Project_Burtsev/ssl_checker ya.ru google.com yandex.ru")


def main():
    """Главная функция"""
    if len(sys.argv) < 2:
        spravka()
        return
    
    # Проверка флага цепочки
    proverit_tsepochku_flag = '--c' in sys.argv
    
    # Берем только сайты
    saity = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    
    if len(saity) == 1:
        obrabotka_odin(saity[0], proverit_tsepochku_flag)
    else:
        obrabotka_mnogo(saity)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПроверка прервана пользователем")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")