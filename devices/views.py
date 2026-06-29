from rest_framework.decorators import api_view
from rest_framework.response import Response
from devices.services.turnstile import validate_turnstile
from .services.intelbras import IntelbrasService


@api_view(["POST"])
def list_devices(request):
    turnstile_token = request.data.get("turnstileToken", "")

    is_valid_captcha = validate_turnstile(
        token=turnstile_token,
        remote_ip=request.META.get("REMOTE_ADDR"),
    )

    if not is_valid_captcha:
        return Response(
            {
                "ok": False,
                "message": "Falha na verificação de segurança. Tente novamente.",
                "items": [],
                "total": 0,
            },
            status=403,
        )

    token = request.data.get("token", "")
    origin = request.data.get("origin", "all")

    try:
        page = int(request.data.get("page", 1))
        page_size = int(request.data.get("pageSize", 10))
    except (TypeError, ValueError):
        return Response(
            {
                "ok": False,
                "message": "Parâmetros de paginação inválidos.",
                "items": [],
                "total": 0,
            },
            status=400,
        )

    service = IntelbrasService()
    result = service.list_devices(
        token=token,
        page=page,
        page_size=page_size,
        origin=origin,
    )

    status_code = result.pop("status", 200)
    return Response(result, status=status_code)