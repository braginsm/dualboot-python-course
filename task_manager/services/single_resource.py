import copy
from typing import Any, List

from rest_framework import routers


class BulkRouter(routers.SimpleRouter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.routes: List[routers.Route] = copy.deepcopy(self.routes)
        self.routes[0].mapping.update({"patch": "partial_bulk_update"})
        self.routes[0].mapping.update({"put": "bulk_update"})
