broker_url='redis://localhost:6379/0'
backend_url='redis://localhost:6379'
timezone = 'Europe/Oslo'

result_backend_transport_options = {
        'retry_policy': {
            'timeout': 5.0 }
}
visibility_timeout = 43200
