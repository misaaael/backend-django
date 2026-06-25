import requests

from django.conf import settings


class IntelbrasService:
    def list_devices(self, token, page=1, page_size=10, origin="all"):
        if not token:
            return {
                "ok": False,
                "status": 401,
                "message": "Token não informado.",
                "items": [],
                "total": 0,
            }

        origin_map = {
            "all": "todos",
            "linked": "vinculado",
            "shared": "compartilhado",
        }

        url = (
            f"{settings.INTELBRAS_BASE_URL}"
            f"{settings.INTELBRAS_PRODUCTS_PATH}"
            "/listar-dispositivos/v1"
        )

        payload = {
            "tamanhoPagina": page_size,
            "pagina": page,
            "origem": origin_map.get(origin, "todos"),
        }

        try:
            response = requests.post(
                url,
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                },
                json=payload,
                timeout=15,
            )

            response.raise_for_status()

            response_data = response.json()

            api_status_code = response_data.get("statusCode")

            body = response_data.get("body", {})

            # A API pode retornar body como string ou como objeto
            if isinstance(body, str):
                body = {"msg": body}

            # Token inválido/expirado
            if response.status_code in (401, 403) or api_status_code in (401, 403):
                return {
                    "ok": False,
                    "status": 401,
                    "message": body.get(
                        "msg",
                        "Token inválido ou expirado.",
                    ),
                    "items": [],
                    "total": 0,
                }

            # Outros erros retornados pela API Intelbras
            if api_status_code and api_status_code != 200:
                return {
                    "ok": False,
                    "status": api_status_code,
                    "message": body.get(
                        "msg",
                        "Erro ao consultar a API Intelbras.",
                    ),
                    "items": [],
                    "total": 0,
                }

            data = body.get("data", [])

            devices = [
                {
                    "id": item.get("ns"),
                    "name": item.get("nome"),
                    "model": item.get("modelo"),
                    "online": item.get("status") == "online",
                    "shared": item.get("origem") == "compartilhado",
                    "version": item.get("versao"),
                    "serial": item.get("ns"),
                    "origin": item.get("origem"),
                    "isSubDevice": item.get("subdispositivo", False),
                    "parentDevice": item.get("dispositivoPai"),
                    "lastOnlineAt": item.get("ultimaVezOnline"),
                    "updateAvailable": item.get("atualizacaoDisponivel", False),
                }
                for item in data
            ]

            return {
                "ok": True,
                "status": 200,
                "items": devices,
                "total": len(devices),
                "page": page,
                "pageSize": page_size,
            }

        except requests.exceptions.RequestException:
            return {
                "ok": False,
                "status": 500,
                "message": "Erro ao consultar a API Intelbras.",
                "items": [],
                "total": 0,
            }

        except (ValueError, TypeError):
            return {
                "ok": False,
                "status": 500,
                "message": "Resposta inválida da API Intelbras.",
                "items": [],
                "total": 0,
            }