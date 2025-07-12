import factory
from django.contrib.auth import get_user_model

EmployeeModel = get_user_model()


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeModel
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'P@ssword123')
    is_active = True
    is_staff = False

    @factory.post_generation
    def post(obj, create, extracted, **kwargs):
        if create:
            obj.save()
