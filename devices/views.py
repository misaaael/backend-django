from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services.intelbras import IntelbrasService


@api_view(["POST"])
def list_devices(request):
    token = request.data.get("token", "")
    page = int(request.data.get("page", 1))
    page_size = int(request.data.get("pageSize", 10))
    origin = request.data.get("origin", "all")

    service = IntelbrasService()
    result = service.list_devices(
        token=token,
        page=page,
        page_size=page_size,
        origin=origin,
    )

    status_code = result.pop("status", 200)
    return Response(result, status=status_code)