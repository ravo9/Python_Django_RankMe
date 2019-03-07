
REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER':
        'rank_me_api.serializers.PasswordResetSerializer',
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
