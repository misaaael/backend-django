# Backend Django — Casa Inteligente

Backend desenvolvido em Django e Django REST Framework para o case técnico da Intelbras. A aplicação atua como uma camada intermediária entre o frontend React e a API da plataforma Open Casa Inteligente, recebendo um token temporário informado pelo usuário e consultando os dispositivos vinculados à conta.

## Tecnologias

* Python
* Django
* Django REST Framework
* django-cors-headers
* python-dotenv
* requests
* SQLite para desenvolvimento local

## Funcionalidades

* Endpoint para listagem de dispositivos
* Integração com a API real da Intelbras
* Filtro por origem dos dispositivos:

  * todos
  * vinculados
  * compartilhados
* Paginação conforme contrato da API Intelbras
* Tratamento de token ausente ou inválido
* Tratamento de erros de comunicação com a API externa
* Normalização da resposta para consumo pelo frontend

## Estrutura principal

```text
backend/
├── config/
│   ├── settings.py
│   └── urls.py
├── devices/
│   ├── services/
│   │   └── intelbras.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
└── .env.example
```

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```env
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
INTELBRAS_BASE_URL=
INTELBRAS_TOKEN=
```

Observação: o token temporário usado para consultar os dispositivos é enviado pelo frontend na requisição. A variável `INTELBRAS_TOKEN` pode ser mantida apenas como referência local, se necessário.

## Como executar localmente

Crie e ative o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute as verificações do Django:

```bash
python manage.py check
```

Inicie o servidor:

```bash
python manage.py runserver
```

Por padrão, o backend ficará disponível em:

```text
http://127.0.0.1:8000
```

## Endpoint disponível

### Listar dispositivos

```http
POST /api/devices/
```

Body esperado:

```json
{
  "token": "token-temporario",
  "page": 1,
  "pageSize": 20,
  "origin": "all"
}
```

Valores aceitos para `origin`:

```text
all
linked
shared
```

Resposta normalizada:

```json
{
  "ok": true,
  "items": [],
  "total": 0,
  "page": 1,
  "pageSize": 20,
  "hasNextPage": false
}
```

## Decisões técnicas

O backend foi criado para isolar a comunicação com a API da Intelbras e evitar que o frontend precise conhecer detalhes do contrato externo, como nomes de campos, payload em português e formato da resposta.

A API da Intelbras não retorna o total geral de dispositivos na resposta. Por isso, o backend expõe `hasNextPage` com base na quantidade de itens retornados na página atual. Essa decisão evita exibir no frontend um total artificial ou incorreto.

## Melhorias futuras

* Adicionar testes automatizados para views e service
* Criar Dockerfile e docker-compose
* Adicionar CI para lint e testes
* Melhorar logs estruturados da integração externa
* Adicionar observabilidade com métricas e tracing
* Separar configurações por ambiente
* Implementar cache quando fizer sentido para reduzir chamadas externas
