# Django_APIView

Implement a base generic view for handling model RESTful endpoints

## Usage

```py
# models.py

from django.db import models

from django_modelapiview import JSONMixin

class MyModel(JSONMixin, models.Model):
    """
    Declare your model as you usually do but
    add a json_fields list
    """

    json_fields:list[str] = ['text', 'image', 'fk', 'fk_reverse', 'm2m', 'my_method']

    text = models.TextField()
    image = models.ImageField()

    fk = models.ForeignKey(...)
    # fk_reverse
    m2m = models.ManyToManyField(...)

    def my_method(self):
        return "my custom value"
```

```py
# views.py

from django_modelapiview import APIView

from .models import MyModel

class MyView(APIView):
    # Required
    model:JSONMixin = MyModel # Your model
    route:str = "mymodels" # The url to access your collection

    # Optional
    queryset:QuerySet = MyModel.objects.all() # A custom base queryset (will be affected by query filters)
    singular_name:str = "my model" # Singular name of your model for reason message
    plural_name:str = "my models" # Plural name of your model for reason message
    http_method_names:list[str] = ['head', 'get', 'patch', 'post'] # The list of HTTP method names that this view will accept.
    enforce_authentification:bool = True # Should this model be restricted with Token access
    query_parameters:list[tuple[str, Callable[[QuerySet, object], QuerySet]]] = [
        ('order_by', lambda queryset, field_names: queryset.order_by(*field_names.split(",")) if field_names else queryset),
        ('limit', lambda queryset, limit: queryset[:int(limit)] if limit else queryset), # Should be last since sliced QuerySet can't be filtered anymore
    ]
```

```py
# urls.py

from django.urls import path, include

from . import views

urlpatterns = [
    path("", include("django_routeview")), # Django RouteView are used as based class for APIView in order to automatically register them
]
```

## Using base views

Django ModelAPIView provides 2 base views:
* LoginView: to handle authentification (using the default Django authentification system)
* URLsView: to list the urls availables

### Usage

```py
# urls.py

from django.urls import path

from django_modelapiview.views import LoginView, URLsView

urlpatterns = [
    ...
    path("login", LoginView.as_view(), name="login"),
    path("", URLsView.as_view(), name="urls")
]
```
