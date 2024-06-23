import factory
from django.contrib.auth import get_user_model

EmployeeModel = get_user_model()


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeModel
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    first_name = 'Test'
    last_name = 'User'
    is_staff = False

    @factory.post_generation
    def post(obj, create, extracted, **kwargs):
        if create:
            obj.save()
