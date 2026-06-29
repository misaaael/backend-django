# Backend - Case Técnico Intelbras

Backend da aplicação desenvolvido em Django e Django REST Framework.

> Este repositório contém apenas o código da API.
>
> Para a documentação completa, arquitetura e instruções de execução da solução, consulte o repositório principal:
>
> **https://github.com/misaaael/case-intelbras**

---

## Tecnologias

- Python
- Django
- Cloudflare Turnstile

---

## Estrutura

```
backend/
├── config/
├── devices/
├── Dockerfile
├── requirements.txt
└── manage.py
```

---

## Executando individualmente

### Ambiente virtual

```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py runserver
```

### Docker

```bash
docker build -t backend-django .

docker run -p 8000:8000 backend-django
```

---

## API

Endpoint principal:

```
POST /api/devices/
```

A API atua como camada intermediária entre o frontend e a API da Intelbras e também realiza a validação do Cloudflare Turnstile antes de consultar a API da Intelbras quando habilitado por configuração.

---

## Documentação

Documentação completa da solução:

https://github.com/misaaael/case-intelbras
