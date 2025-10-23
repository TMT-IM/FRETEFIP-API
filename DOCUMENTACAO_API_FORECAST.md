# API de Projeções de Frete - Documentação para Desenvolvedores

Bem-vindo à API de Projeções de Frete! Esta API permite que você obtenha previsões de preços de frete utilizando modelos de machine learning para rotas específicas no Brasil.

## Índice

- [Introdução](#introdução)
- [Começando](#começando)
- [Autenticação](#autenticação)
- [Endpoints](#endpoints)
- [Exemplos de Uso](#exemplos-de-uso)
- [Tratamento de Erros](#tratamento-de-erros)
- [Limites e Quotas](#limites-e-quotas)
- [Perguntas Frequentes](#perguntas-frequentes)

---

## Introdução

### O que é a API de Projeções de Frete?

A API de Projeções de Frete utiliza modelos de machine learning para prever preços de frete para rotas específicas no Brasil. Com ela, você pode:

- Obter previsões de preços para até **24 meses** à frente
- Consultar múltiplas combinações de produtos, veículos e carrocerias
- Receber **4 previsões por mês** (dias 1, 10, 15 e 25)
- Integrar facilmente em seu sistema via REST API

### Como funciona?

1. Você fornece: origem, destino, produtos, veículos e carrocerias
2. A API busca automaticamente: UFs, mesorregiões e distâncias
3. O modelo de machine learning processa e gera as previsões
4. Você recebe: JSON com todas as previsões e estatísticas

---

## Começando

### URL Base

```
https://fretefip.up.railway.app/api/forecast
```

### Obtendo seu Token de API

Para usar a API, você precisa de um token de autenticação. Entre em contato com o administrador do sistema para obter seu token pessoal.

> O token será único para você e estará associado a um limite diário de requisições.

### Teste de Conectividade

Antes de começar, teste se a API está online:

```bash
curl https://fretefip.up.railway.app/api/forecast/health
```

**Resposta esperada:**

```json
{
  "status": "online",
  "service": "Freight Forecast API",
  "timestamp": "2025-10-23T14:30:00",
  "version": "1.0.0",
  "limits": {
    "max_months_ahead": 24,
    "predictions_per_month": 4
  }
}
```

---

## Autenticação

Todas as requisições (exceto `/health`) requerem autenticação via token Bearer.

### Método 1: Header Authorization (Recomendado)

```bash
curl -H "Authorization: Bearer SEU_TOKEN_AQUI" \
     https://fretefip.up.railway.app/api/forecast/predict
```

### Método 2: Query Parameter

```bash
curl "https://fretefip.up.railway.app/api/forecast/predict?token=SEU_TOKEN_AQUI"
```

---

## Endpoints

### 1. Health Check

Verifica se a API está online (não requer autenticação).

**Endpoint:**
```
GET /api/forecast/health
```

**Resposta:**

```json
{
  "status": "online",
  "service": "Freight Forecast API",
  "timestamp": "2025-10-23T14:30:00",
  "version": "1.0.0",
  "limits": {
    "max_months_ahead": 24,
    "predictions_per_month": 4
  }
}
```

---

### 2. Previsão de Frete

Gera previsões de preço de frete para uma rota específica.

**Endpoint:**
```
POST /api/forecast/predict
GET  /api/forecast/predict
```

#### Parâmetros Obrigatórios

| Parâmetro | Tipo | Descrição | Exemplo |
|-----------|------|-----------|---------|
| `origem` | string | Nome da cidade de origem | "SINOP" |
| `destino` | string | Nome da cidade de destino | ITAITUBA" |
| `produto` ou `produtos` | string ou array | Produto(s) a transportar | ["SOJA", "MILHO"] |
| `veiculo` ou `veiculos` | string ou array | Tipo(s) de veículo | ["RODOTREM", "BITREM"] |
| `carroceria` ou `carrocerias` | string ou array | Tipo(s) de carroceria | ["CAÇAMBA", "GRANELEIRO"] |

#### Parâmetros Opcionais

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `months_ahead` | integer | 12 | Número de meses à frente (1-24) |

> **Nota:** Os nomes de cidades e produtos devem estar padronizadas conforme planilhas de apoio. O modelo consegue projetar até 24 meses, mas sugerimos limitar a 12 meses.

#### Exemplo de Requisição (POST)

```json
{
  "origem": "SINOP",
  "destino": "ITAITUBA",
  "produtos": ["SOJA"],
  "veiculos": ["RODOTREM"],
  "carrocerias": ["GRANELEIRO"],
  "months_ahead": 12
}
```

#### Exemplo de Resposta

```json
{
  "success": true,
  "forecast_data": [
    {
      "date": "2025-11-01T12:00:00",
      "produto": "SOJA",
      "veiculo": "RODOTREM",
      "carroceria": "GRANELEIRO",
      "preco_previsto": 259.27,
      "km": 977.00
    },
    {
      "date": "2025-11-10T12:00:00",
      "produto": "SOJA",
      "veiculo": "RODOTREM",
      "carroceria": "GRANELEIRO",
      "preco_previsto": 266.34,
      "km": 977.00
    }
    // ... mais 46 previsões (4 por mês × 12 meses)
  ],
  "statistics": {
    "min_price": 196.43,
    "max_price": 320.58,
    "avg_price": 274.58,
    "total_predictions": 48
  },
  "route_info": {
    "origem": "SINOP",
    "destino": "ITAITUBA",
    "uf_origem": "MT",
    "uf_destino": "PA",
    "km": 977.00
  },
  "request_parameters": {
    "origem": "SINOP",
    "destino": "ITAITUBA",
    "produtos": ["SOJA"],
    "veiculos": ["RODOTREM"],
    "carrocerias": ["GRANELEIRO"],
    "months_ahead": 12
  },
  "metadata": {
    "total_predictions": 48,
    "predictions_per_month": 4,
    "max_allowed_months": 24
  },
  "timestamp": "2025-10-23T14:30:00"
}
```

---

## Exemplos de Uso

### Python (Código Completo)

Utilize o arquivo `exemplo_uso_api_forecast.py` fornecido junto com esta documentação. Ele contém um cliente completo que funciona tanto com GET quanto POST.

**Uso básico:**

```python
from exemplo_uso_api_forecast import ForecastAPIClient

# Inicializar cliente
API_URL = "https://fretefip.up.railway.app/api/forecast/predict"
TOKEN = "seu_token_aqui"
client = ForecastAPIClient(API_URL, TOKEN)

# Fazer consulta
dados = {
    "origem": "SINOP",
    "destino": "ITAITUBA",
    "produtos": ["SOJA"],
    "veiculos": ["RODOTREM"],
    "carrocerias": ["GRANELEIRO"],
    "months_ahead": 12
}

resultado = client.consultar_projecoes(dados)

if resultado and resultado.get('success'):
    previsoes = resultado['forecast_data']
    stats = resultado['statistics']

    print(f"Total de previsões: {len(previsoes)}")
    print(f"Preço médio: R$ {stats['avg_price']:.2f}")
    print(f"Preço mínimo: R$ {stats['min_price']:.2f}")
    print(f"Preço máximo: R$ {stats['max_price']:.2f}")

    # Listar todas as previsões
    for forecast in previsoes:
        data = forecast['date']
        preco = forecast['preco_previsto']
        print(f"{data}: R$ {preco:,.2f}")
```

---

### Python (Requisição Simples com requests)

```python
import requests

url = "https://fretefip.up.railway.app/api/forecast/predict"
headers = {
    "Authorization": "Bearer SEU_TOKEN_AQUI",
    "Content-Type": "application/json"
}
data = {
    "origem": "RONDONOPOLIS",
    "destino": "PARANAGUA",
    "produtos": ["SOJA"],
    "veiculos": ["RODOTREM"],
    "carrocerias": ["GRANELEIRO"],
    "months_ahead": 6
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    print(f"Sucesso! Total de previsões: {result['metadata']['total_predictions']}")
    print(f"Preço médio: R$ {result['statistics']['avg_price']:.2f}")
else:
    print(f"Erro {response.status_code}: {response.json().get('message')}")
```

---

### JavaScript/Node.js (fetch)

```javascript
const url = 'https://fretefip.up.railway.app/api/forecast/predict';
const token = 'SEU_TOKEN_AQUI';

const data = {
  origem: 'BRASILIA',
  destino: 'GOIANIA',
  produtos: ['Carga Geral'],
  veiculos: ['Truck'],
  carrocerias: ['Baú'],
  months_ahead: 6
};

fetch(url, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
})
  .then(response => response.json())
  .then(result => {
    if (result.success) {
      console.log('Total de previsões:', result.metadata.total_predictions);
      console.log('Preço médio: R$', result.statistics.avg_price.toFixed(2));

      // Processar previsões
      result.forecast_data.forEach(forecast => {
        console.log(`${forecast.date}: R$ ${forecast.preco_previsto.toFixed(2)}`);
      });
    }
  })
  .catch(error => console.error('Erro:', error));
```

---

### cURL (POST)

```bash
curl -X POST https://fretefip.up.railway.app/api/forecast/predict \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "origem": "SINOP",
    "destino": "RONDONOPOLIS",
    "produtos": ["MILHO"],
    "veiculos": ["BITREM"],
    "carrocerias": ["GRANELEIRO"],
    "months_ahead": 12
  }'
```

---

### cURL (GET)

```bash
curl "https://fretefip.up.railway.app/api/forecast/predict?token=SEU_TOKEN_AQUI&origem=BRASILIA&destino=GOIANIA&produto=Soja&veiculo=Carreta&carroceria=Graneleiro&months_ahead=6"
```

---

## Tratamento de Erros

A API retorna códigos HTTP padrão e mensagens de erro em JSON.

### 401 Unauthorized

**Causa:** Token não fornecido.

```json
{
  "error": true,
  "message": "Token de API não fornecido"
}
```

**Solução:** Inclua o token no header `Authorization` ou como query parameter `token`.

---

### 403 Forbidden

**Causa:** Token inválido, expirado ou limite diário excedido.

```json
{
  "error": true,
  "message": "Token inválido, expirado ou limite excedido"
}
```

**Solução:**
- Verifique se o token está correto
- Verifique se o token não expirou
- Aguarde até o próximo dia se o limite foi excedido

---

### 400 Bad Request

**Causa:** Parâmetros obrigatórios faltando ou inválidos.

```json
{
  "error": true,
  "message": "Os campos \"origem\" e \"destino\" são obrigatórios"
}
```

**Solução:** Verifique se todos os parâmetros obrigatórios estão presentes e corretos.

---

### 404 Not Found

**Causa:** Rota não encontrada no banco de dados.

```json
{
  "error": true,
  "message": "Rota não encontrada no banco de dados: ORIGEM → DESTINO",
  "suggestion": "Verifique se os nomes de origem e destino estão corretos"
}
```

**Solução:**
- Verifique a grafia dos nomes das cidades
- Use MAIÚSCULAS sem acentos (ex: "SAO PAULO")
- Entre em contato para verificar rotas disponíveis

---

### 500 Internal Server Error

**Causa:** Erro interno ao processar a requisição.

```json
{
  "error": true,
  "message": "Erro interno ao processar requisição",
  "details": "Detalhes do erro"
}
```

**Solução:** Entre em contato com o suporte técnico.

---

## Limites e Quotas

### Limites por Token

| Recurso | Limite |
|---------|--------|
| Requisições por dia | Configurável (geralmente 100) |
| Meses à frente (máximo) | 24 meses |
| Previsões por mês | 4 (dias 1, 10, 15, 25) |
| Tempo de resposta típico | 1-5 segundos |

### Boas Práticas

- **Cache:** Armazene resultados localmente para evitar requisições duplicadas
- **Batch:** Quando possível, consulte múltiplos produtos/veículos em uma única requisição
- **Retry:** Implemente retry com backoff exponencial em caso de erros temporários
- **Timeout:** Configure timeouts de pelo menos 60 segundos para operações de previsão

---

## Perguntas Frequentes

### 1. Como sei quais cidades estão disponíveis?

Utilize as planilhas de apoio no repositorio.

### 2. Posso consultar previsões para mais de 24 meses?

Não. O limite máximo é de 24 meses para garantir a qualidade das previsões, mas recomendamos limitar em 12 meses.

### 3. Por que recebo 4 previsões por mês?

O modelo foi treinado para gerar previsões nos dias 1, 10, 15 e 25 de cada mês, garantindo uma boa distribuição temporal.

### 4. Posso consultar múltiplos produtos de uma vez?

Sim! Você pode passar arrays de produtos, veículos e carrocerias. A API gerará previsões para todas as combinações.

### 5. O que acontece se eu exceder meu limite diário?

Você receberá um erro 403 (Forbidden). O limite é resetado diariamente à meia-noite.

### 6. Como funciona o formato de nomes das cidades?

Use MAIÚSCULAS sem acentos:
- Correto: "SAO PAULO", "BRASILIA"
- Incorreto: "São Paulo", "Brasília"

### 7. GET ou POST?

Ambos funcionam! O POST é recomendado para requisições complexas com múltiplos parâmetros. O GET é útil para testes rápidos. O cliente Python fornecido (`exemplo_uso_api_forecast.py`) detecta automaticamente qual método usar.

---

## Suporte

Para dúvidas, problemas ou solicitação de novos recursos:

- Consulte o arquivo `exemplo_uso_api_forecast.py` para exemplos práticos
- Entre em contato com o administrador do sistema

---

## Notas de Versão

### v1.0.0 (2025-10-23)
- Lançamento inicial da API
- Suporte para métodos GET e POST
- Autenticação via token Bearer
- Previsões para até 24 meses
- Múltiplos produtos, veículos e carrocerias
- Sistema de limites diários
