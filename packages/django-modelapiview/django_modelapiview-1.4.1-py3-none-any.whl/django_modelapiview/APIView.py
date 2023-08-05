from django.db.models import QuerySet
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import path
from django.http import HttpRequest, HttpResponse
from django.core.signing import BadSignature, SignatureExpired
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from typing import List, Tuple, Callable
from http import HTTPStatus

from django_routeview import RouteView, urlpatterns

from .responses import APIResponse, QuerySuccessful, CreationSuccessful, NotFound, NotAllowed, Conflict, InvalidToken
from .JSONMixin import JSONMixin
from .Token import Token
from .decorators import catch_exceptions


class APIView(RouteView):
    """
     Auto registered view on self.route path
     Describe the endpoints associated with a model


     `model:JSONMixin|django.db.Model`

     `queryset:django.db.QuerySet:optional` # Default to `model.objects.all()`

     `singular_name:str:optional` # Default to `model._meta.verbose_name or model.__name__`

     `plural_name:str:optional` # Default to `model._meta.verbose_name_plural or f"{model.__name__}s"`

     `enforce_authentification:bool:optional` Default to `False`

     `http_method_names:list[str]:optional` Default to `["head", "options", "get", "post", "put", "patch", "delete"]`
    """

    model:JSONMixin = None
    queryset:QuerySet = None
    singular_name:str = None
    plural_name:str = None
    enforce_authentification:bool = False
    http_method_names:List[str] = ["get", "post", "put", "patch", "delete", "head", "options"]
    query_parameters:List[Tuple[str, Callable[[QuerySet, object], QuerySet]]] = [
        ('order_by', lambda queryset, field_names: queryset.order_by(*field_names.split(",")) if field_names else queryset),
        ('limit', lambda queryset, limit: queryset[:int(limit)] if limit else queryset),
    ]

    _permissions_match_table = {
        'GET': "view",
        'PATCH': "change",
        'POST': "add",
        'PUT': "add",
        'DELETE': "delete"
    }

    def _init_properties(self) -> None:
        if self.__name__ == "APIView":
            return

        for cls in self.mro():
            self.http_method_names = [method_name for method_name, method in vars(cls).items() if hasattr(method, '__annotations__') and method_name != "dispatch" and method.__annotations__.get('return') == APIResponse]
            if self.http_method_names:
                break
            elif self.model is None:
                raise ValueError(f"NonModel-APIView {self.__name__} requires a custom implementation of one of : head, options, get, post, put, patch, delete")

        if self.name is None:
            self.name = self.__name__

        if self.model is not None:

            if self.route is None:
                self.route = self.plural_name or self.model._meta.verbose_name_plural or f"{self.model.__name__}s"

            if self.queryset is None:
                self.queryset = self.model.objects.all()

            if self.singular_name is None:
                self.singular_name = self.model._meta.verbose_name or self.model.__name__

            if self.plural_name is None:
                self.plural_name = self.model._meta.verbose_name_plural or f"{self.model.__name__}s"

        elif self.route is None:
            raise ValueError(f"NonModel-APIView {self.__name__} requires a user defined route")

    def _add_route_(self) -> None:
        if self.__name__ == "APIView":
            return

        if self.model is not None:
            self.route = f"{self.route.rstrip('/')}/"
            urlpatterns.extend((
                path(self.route, self.as_view(), name=self.name),
                path(f"{self.route}<int:id>", self.as_view(), name=self.name)
            ))
        else:
            urlpatterns.append(
                path(self.route, self.as_view(), name=self.name)
            )
            

    def _parse_parameters(self, request:HttpRequest, queryset:QuerySet) -> QuerySet:
        get_parameters = request.GET.dict()

        queries = {query[0]: get_parameters.pop(query[0], None) for query in self.query_parameters}

        for (filter_name, filter_value) in get_parameters.items():
            if "," in filter_value:
                queryset = queryset.filter((filter_name, filter_value.split(",")))
            else:
                queryset = queryset.filter((filter_name, filter_value))

        for (query_name, transform) in self.query_parameters:
            queryset = transform(queryset, queries.get(query_name))

        return queryset

    @catch_exceptions
    @csrf_exempt
    def dispatch(self, request:HttpRequest, id:int=None) -> APIResponse:
        headers = dict(request.headers)

        queryset = self._parse_parameters(request, self.queryset.filter(id=id) if id else self.queryset)

        if self.enforce_authentification:

            if not 'Authorization' in headers:
                return InvalidToken("Authentification required")

            token = Token(signed_data=headers['Authorization'].split(" ")[1])
            try:
                token.unsign()
            except BadSignature:
                return InvalidToken("Invalid signature")
            except SignatureExpired:
                return InvalidToken("Token expired")

            try:
                user = get_user_model().objects.get(id=token.uid)
            except (KeyError, ObjectDoesNotExist):
                return InvalidToken("Invalid body")

            if not user.has_perm(f'api.{self._permissions_match_table[request.method]}_{self.singular_name}') and not request.path_info.split("?")[0].strip("/").endswith(str(user.id)):
                return NotAllowed()

        return super().dispatch(request=request, queryset=queryset, id=id)

    def head(self, request:HttpRequest, *args, **kwargs) -> APIResponse:
        return HttpResponse()

    def options(self, request:HttpRequest, *args, **kwargs) -> APIResponse:
        return APIResponse(HTTPStatus.OK, "Available methods", self.http_method_names)

    def get(self, request:HttpRequest, queryset:QuerySet, id:int=None) -> APIResponse:
        """
         Retrieve specific or collection
        """
        if id:
            if not queryset.exists():
                return NotFound(f"No {self.singular_name} with id {id}")
            return QuerySuccessful(f"Retrieved {self.singular_name}", data=queryset.first().serialize(request))

        # Else if trying to get on collection
        return QuerySuccessful(f"Retrieved {self.plural_name}", data=[obj.serialize(request) for obj in queryset])

    def patch(self, request:HttpRequest, queryset:QuerySet, id:int=None) -> APIResponse:
        """
         Update specific
        """
        if id:
            if not queryset.exists():
                return NotFound(f"No {self.singular_name} with id {id}")
            return QuerySuccessful(f"Updated {self.singular_name}", self.model.deserialize(request.body.decode("utf-8"), id).serialize(request))

        # Else if trying to patch on collection
        return NotAllowed()

    def put(self, request:HttpRequest, queryset:QuerySet, id:int=None) -> APIResponse:
        """
         Emplace specific
        """
        if id:
            if queryset.exists():
                return Conflict(f"{id} already taken")
            return CreationSuccessful(f"Created {self.singular_name}", self.model.deserialize(request.body.decode("utf-8"), id).serialize(request))

        # Else if trying to put on collection
        return NotAllowed("You are trying to emplace on a collection. Instead use POST to create or use an id")

    def delete(self, request:HttpRequest, queryset:QuerySet, id:int=None) -> APIResponse:
        """
         Delete specific
        """
        if id:
            if not queryset.exists():
                return NotFound(f"No {self.singular_name} with id {id}")
            obj_serialized = queryset.first().serialize(request)
            queryset.delete()
            return QuerySuccessful(f"Deleted {self.singular_name}", obj_serialized)

        # Else if trying to delete on collection
        return NotAllowed()

    def post(self, request:HttpRequest, queryset:QuerySet, id:int=None) -> APIResponse:
        """
         Create specific in collection
        """
        if id:
            return NotAllowed("You are trying to create at a specific id. Instead use PUT to emplace or use no id")

        # Else if trying to post on collection
        return CreationSuccessful(f"Created {self.singular_name}", self.model.deserialize(request.body.decode("utf-8"), id).serialize(request))
