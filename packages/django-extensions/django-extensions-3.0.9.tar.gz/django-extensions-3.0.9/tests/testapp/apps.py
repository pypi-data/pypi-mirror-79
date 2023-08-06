# -*- coding: utf-8 -*-
from django.apps import AppConfig


class TestAppConfig(AppConfig):
    name = 'tests.testapp'

    # def ready(self):
    #     from django.core.checks import Error, register

    #     @register()
    #     def example_check(app_configs, **kwargs):
    #         errors = []
    #         # ... your check logic here
    #         if True:
    #             errors.append(
    #                 Error(
    #                     'an error',
    #                     hint='A hint.',
    #                     obj="Bas",
    #                     id='myapp.E001',
    #                 )
    #             )
    #         return errors
