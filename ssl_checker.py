"""
Основная логика проверки SSL-сертификатов
"""

import ssl
import socket
from datetime import datetime, timezone
from cryptography import x509
from cryptography.hazmat.backends import default_backend


class ProverkaSSLCert:
    """Класс для проверки SSL-сертификатов"""
    
    def poluchit_cert(self, hostname, port=443):
        """Получить SSL-сертификат с сайта"""
        try:
            # Убираем протокол если есть
            if hostname.startswith(('http://', 'https://')):
                hostname = hostname.split('://')[1]
            
            print(f"Подключение к {hostname} по {port} порту...")
            
            # Создание SSL контекста
            context = ssl.create_default_context()
            context.check_hostname = True             # Соответсвие имени хоста в сертификате
            context.verify_mode = ssl.CERT_REQUIRED   # Валидность сертификата
            
            # Подключение и получение сертификата
            with socket.create_connection((hostname, port), 10) as sock:   # Контекстный менеджер, закрывает соединение через 10 секунд
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert_bin = ssock.getpeercert(binary_form=True)         # Получение сертификата
                    
                    if cert_bin:
                        cert = x509.load_der_x509_certificate(cert_bin, default_backend()) # Преобразует бинарные данные в объект сертификата
                        print("Сертификат получен")
                        return cert
                    else:
                        print("Не удалось получить сертификат")
                        return None
        
        # Обработка заключений            
        except socket.timeout:            # Специальное исключение для таймаутов     
            print("Таймаут подключения")
            return None
        except Exception as e:            # Перехват любых других ошибок
            print(f"Ошибка: {e}")
            return None
    
    def proverit_srok(self, cert):
        """Проверить срок действия сертификата"""
        if not cert:
            return None
            
        now = datetime.now(timezone.utc)
        
        # Использование свойств
        nachalo = cert.not_valid_before_utc
        end = cert.not_valid_after_utc
        
        # Проверяем даты
        esli_prosrochen = end < now
        esli_rano = nachalo > now
        ostalos_dney = (end - now).days
        
        # Определение статуса
        if esli_prosrochen:
            status = "ПРОСРОЧЕН"
        elif esli_rano:
            status = "ЕЩЕ НЕ ДЕЙСТВИТЕЛЕН"
        else:
            status = "ДЕЙСТВИТЕЛЕН"
        
        # Форматирование информации
        from additionally import format_name
        vladelets = format_name(cert.subject)
        izdatel = format_name(cert.issuer)
        
        # Возврат словаря с результатами проверки
        return {
            'status': status,
            'ostalos_dney': ostalos_dney,
            's_kakogo': nachalo,
            'do_kakogo': end,
            'vladelets': vladelets,
            'izdatel': izdatel,
            'esli_prosrochen': esli_prosrochen,
            'esli_rano': esli_rano
        }
    
    def proverit_tsepochku(self, hostname, port=443):
        """Проверить цепочку сертификатов"""
        try:
            context = ssl.create_default_context()
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            
            with socket.create_connection((hostname, port), 10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    tsepochka_bin = ssock.getpeercertchain()
                    return len(tsepochka_bin) if tsepochka_bin else 0
                    
        except Exception:
            return 0
    
    def pokazat_info(self, hostname, proverit_tsepochku=False):
        """Показать информацию о сертификате"""
        print(f"\n{'='*50}")
        print(f"ПРОВЕРКА SSL: {hostname}")
        print(f"{'='*50}")
        
        # Нет сертификата
        cert = self.poluchit_cert(hostname)
        if not cert:
            print("Не удалось получить сертификат")
            return False
        
        # Нет информации
        info = self.proverit_srok(cert)
        if not info:
            print("Не удалось проанализировать сертификат")
            return False
        
        # Импорт результата
        from additionally import pokazat_rezultat
        pokazat_rezultat(info)
        
        # С цепочкой
        if proverit_tsepochku:
            dlina_chain = self.proverit_tsepochku(hostname)
            print(f"\nЦЕПОЧКА СЕРТИФИКАТОВ:")
            print(f"  Длина цепочки: {dlina_chain}")
        
        # Импорт рекомендаций
        from additionally import dat_rekomendaciyu
        dat_rekomendaciyu(info)
        
        print(f"\n{'='*50}")
        return True