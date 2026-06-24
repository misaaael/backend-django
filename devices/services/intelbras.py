class IntelbrasService:
    def list_devices(self, token, page=1, page_size=10, origin="all"):
        if not token:
            return {
                "ok": False,
                "status": 401,
                "message": "Token inválido ou expirado.",
                "items": [],
                "total": 0,
            }

        devices = [
            {
                "id": i,
                "name": f"Dispositivo {i}",
                "model": ["iM5 SC", "iM7 OUT", "EWS 1001", "EG 200", "RG 1200"][i % 5],
                "mac": f"AA:BB:CC:{i:02d}:00:FF",
                "online": i % 3 != 0,
                "shared": i % 4 == 0,
            }
            for i in range(1, 48)
        ]

        if origin == "shared":
            devices = [d for d in devices if d["shared"]]
        elif origin == "linked":
            devices = [d for d in devices if not d["shared"]]

        total = len(devices)
        start = (page - 1) * page_size
        end = start + page_size

        return {
            "ok": True,
            "status": 200,
            "items": devices[start:end],
            "total": total,
            "page": page,
            "pageSize": page_size,
        }