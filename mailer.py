from pysendpulse.pysendpulse import PySendPulse


def send_join_mail(email, token):
    REST_API_ID = 'a1e29a8981861aa6795c007bab8d4e9b'
    REST_API_SECRET = '9353d6de906c9f455efb7ae05334c489'
    TOKEN_STORAGE = 'memcached'
    SPApiProxy = PySendPulse(REST_API_ID, REST_API_SECRET, TOKEN_STORAGE)
    email = {
        'subject': 'Подтверждение регистрации',
        'html': f'<p>Для подтверждения регистрации пройдите по ссылке: http://www.mp-scope.tech/confirm?token={token}</p>',
        'text': f'Для подтверждения регистрации пройдите по ссылке: http://www.mp-scope.tech/confirm?token={token}',
        'from': {'name': 'Команда MP-Scope', 'email': 'service@mp-scope.tech'},
        'to': [
            {'name': f'"{email}"', 'email': email}
        ]
    }
    SPApiProxy.smtp_send_mail(email)
    print("Sent", email, token)
