import copy
from typing import Any, List
from requests import Request, Response

from rest_framework import routers

from typing import Any, List, TYPE_CHECKING

from rest_framework import viewsets

if TYPE_CHECKING:
    BaseViewMixinBaseClass = viewsets.GenericViewSet
else:
    BaseViewMixinBaseClass = object


class BulkRouter(routers.SimpleRouter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.routes: List[routers.Route] = copy.deepcopy(self.routes)
        self.routes[0].mapping.update({"patch": "partial_bulk_update"})
        self.routes[0].mapping.update({"put": "bulk_update"})


class SingleResourceMixin(BaseViewMixinBaseClass):
    pagination_class = None

    def list(self, _: Request, *__: Any, **___: Any) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SingleResourceUpdateMixin(BaseViewMixinBaseClass):
    def bulk_update(self, request: Request, *_: Any, **kwargs: Any) -> Response:
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_bulk_update(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        kwargs["partial"] = True
        return self.bulk_update(request, *args, **kwargs)
