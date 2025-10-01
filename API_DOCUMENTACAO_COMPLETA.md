# 📚 API Externa de Métricas de Frete - Documentação Completa

> **Versão:** 1.0.0  
> **Base URL:** `https://fretefip.up.railway.app/api/external`  
> **Última atualização:** Setembro 2025

---

## 📋 Índice

1. [Introdução](#introdução)
2. [Autenticação](#autenticação)
3. [Endpoints Disponíveis](#endpoints-disponíveis)
4. [Filtros e Campos](#filtros-e-campos)
5. [Exemplos de Código](#exemplos-de-código)
6. [Limites e Quotas](#limites-e-quotas)
7. [Códigos de Erro](#códigos-de-erro)
8. [FAQ e Troubleshooting](#faq-e-troubleshooting)

---

## 🎯 Introdução

Esta API permite consultar **métricas estatísticas** sobre fretes no Brasil, incluindo:
- Preços médios, mínimos e máximos
- Distâncias médias
- Quantidade de registros
- Desvio padrão dos preços

A API aceita **filtros flexíveis** para refinar as consultas por origem, destino, produto, veículo e período.

---

## 🔒 Autenticação

Todas as requisições (exceto health check) requerem um **token de API**.

### Como usar o token:

**Opção 1: Header Authorization (Recomendado)**
```http
Authorization: Bearer SEU_TOKEN_AQUI
```

**Opção 2: Query Parameter**
```
?token=SEU_TOKEN_AQUI
```

### Obtendo seu token:
Entre em contato com o suporte para receber seu token de acesso.

---

## 📡 Endpoints Disponíveis

### 1. Health Check

Verifica se a API está online (não requer autenticação).

**Endpoint:** `GET /health`

**URL Completa:** `https://fretefip.up.railway.app/api/external/health`

**Resposta:**
```json
{
  "status": "online",
  "timestamp": "2025-09-30T19:51:47.685140",
  "version": "1.0.0"
}
```

---

### 2. Consultar Métricas

Retorna estatísticas de fretes baseado nos filtros fornecidos.

**Endpoint:** `POST /metrics` ou `GET /metrics`

**URL Completa:** `https://fretefip.up.railway.app/api/external/metrics`

#### **Métodos Aceitos:**

**POST (Recomendado):** Filtros no body JSON
```http
POST /api/external/metrics
Content-Type: application/json
Authorization: Bearer SEU_TOKEN

{
  "tipo_frete": "R$/VIAGEM",
  "origem": "CAMPINAS",
  "periodo_dias": 90
}
```

**GET (Alternativo):** Filtros em query parameters
```http
GET /api/external/metrics?tipo_frete=R$/VIAGEM&origem=CAMPINAS&periodo_dias=90
Authorization: Bearer SEU_TOKEN
```

> ⚠️ **Importante:** POST é preferido pois suporta filtros mais complexos e não expõe dados na URL.

---

## 🎛️ Filtros e Campos

### Filtros Disponíveis

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|-------|------|-------------|-----------|---------|
| `tipo_frete` | string | ✅ **SIM** | Tipo do frete | `"R$/VIAGEM"` ou `"R$/UND"` |
| `origem` | string | Não | Cidade de origem | `"CAMPINAS"` |
| `destino` | string | Não | Cidade de destino | `"SÃO PAULO"` |
| `uf_origem` | string | Não | Estado de origem (sigla) | `"SP"` |
| `uf_destino` | string | Não | Estado de destino (sigla) | `"RJ"` |
| `meso_origem` | string | Não | Mesorregião de origem | `"CAMPINAS"` |
| `meso_destino` | string | Não | Mesorregião de destino | `"METROPOLITANA DE SÃO PAULO"` |
| `produtos` | array | Não | Lista de produtos | `["SOJA", "MILHO"]` |
| `veiculos` | array | Não | Lista de veículos | `["CARRETA", "TRUCK"]` |
| `carrocerias` | array | Não | Lista de carrocerias | `["SIDER", "GRANELEIRO"]` |
| `periodo_dias` | integer | Não | Período em dias (padrão: 120) | `90` |

### ⚠️ Valores Válidos para `tipo_frete`

**APENAS estes valores são aceitos:**
- `"R$/VIAGEM"` - Preço por viagem completa
- `"R$/UND"` - Preço por unidade/tonelada

❌ **NÃO use:** "CIF", "FOB" ou outros valores

### 📊 Campos Retornados

A API retorna as seguintes estatísticas:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `count` | integer | Quantidade de registros encontrados |
| `avg_price` | float | Preço médio (R$) |
| `avg_distance` | float | Distância média (km) |
| `min_price` | float | Preço mínimo (R$) |
| `max_price` | float | Preço máximo (R$) |
| `std_dev` | float | Desvio padrão dos preços (R$) |

**Dados originais incluem (mas não são retornados individualmente):**
- `data_anuncio` - Data do anúncio
- `origem` - Cidade de origem
- `destino` - Cidade de destino
- `uf_origem` - UF de origem
- `uf_destino` - UF de destino
- `meso_origem` - Mesorregião de origem
- `meso_destino` - Mesorregião de destino
- `km` - Distância em quilômetros
- `preco` - Preço do frete
- `tipo_de_frete` - Tipo do frete

---

## 💻 Exemplos de Código

### Python - Exemplo Completo

```python
"""
Exemplo completo de uso da API de Métricas de Frete
Funciona com GET ou POST automaticamente
"""
import requests
import json

# ========== CONFIGURAÇÃO ==========
API_URL = "https://fretefip.up.railway.app/api/external/metrics"
TOKEN = "seu_token_aqui"  # Substitua pelo seu token

# ========== EXEMPLO 1: Consulta Básica (POST) ==========
print("=" * 70)
print("EXEMPLO 1: Consulta Básica")
print("=" * 70)

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

filtros = {
    "tipo_frete": "R$/VIAGEM",
    "periodo_dias": 90
}

response = requests.post(API_URL, json=filtros, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"\n✅ Sucesso!")
    print(f"📊 Registros encontrados: {data['data']['count']}")
    print(f"💰 Preço médio: R$ {data['data']['avg_price']:.2f}")
    print(f"📏 Distância média: {data['data']['avg_distance']:.2f} km")
    print(f"📉 Preço mínimo: R$ {data['data']['min_price']:.2f}")
    print(f"📈 Preço máximo: R$ {data['data']['max_price']:.2f}")
elif response.status_code == 404:
    print("\n⚠️  Nenhum dado encontrado para os filtros especificados")
else:
    print(f"\n❌ Erro {response.status_code}: {response.json()}")

# ========== EXEMPLO 2: Consulta com Filtros Específicos ==========
print("\n" + "=" * 70)
print("EXEMPLO 2: Rota Específica")
print("=" * 70)

filtros = {
    "tipo_frete": "R$/VIAGEM",
    "origem": "CAMPINAS",
    "destino": "SÃO PAULO",
    "uf_origem": "SP",
    "uf_destino": "SP",
    "periodo_dias": 60
}

response = requests.post(API_URL, json=filtros, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"\n✅ Rota: {data['filters_applied']['origem']} → {data['filters_applied']['destino']}")
    print(f"📊 Registros: {data['data']['count']}")
    print(f"💰 Preço médio: R$ {data['data']['avg_price']:.2f}")
    print(f"📏 Distância média: {data['data']['avg_distance']:.2f} km")

# ========== EXEMPLO 3: Filtrar por Produtos ==========
print("\n" + "=" * 70)
print("EXEMPLO 3: Filtro por Produtos")
print("=" * 70)

filtros = {
    "tipo_frete": "R$/UND",
    "produtos": ["SOJA", "MILHO"],
    "uf_origem": "MT",
    "periodo_dias": 120
}

response = requests.post(API_URL, json=filtros, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"\n✅ Produtos: {', '.join(data['filters_applied']['produtos'])}")
    print(f"📊 Registros: {data['data']['count']}")
    print(f"💰 Preço médio por unidade: R$ {data['data']['avg_price']:.2f}")

# ========== EXEMPLO 4: Usando GET (alternativo) ==========
print("\n" + "=" * 70)
print("EXEMPLO 4: Usando GET (Query Parameters)")
print("=" * 70)

# Construir URL com parâmetros
params = {
    "tipo_frete": "R$/VIAGEM",
    "origem": "CAMPINAS",
    "periodo_dias": 30
}

response = requests.get(
    API_URL,
    params=params,
    headers={"Authorization": f"Bearer {TOKEN}"}
)

if response.status_code == 200:
    data = response.json()
    print(f"\n✅ Consulta via GET funcionou!")
    print(f"📊 Registros: {data['data']['count']}")
    print(f"💰 Preço médio: R$ {data['data']['avg_price']:.2f}")
```

---

### Python - Cliente Inteligente (Recomendado)

```python
"""
Cliente inteligente que tenta POST primeiro, fallback para GET
"""
import requests
import json
from urllib.parse import urlencode

class FreteAPIClient:
    """Cliente da API de Fretes com fallback automático"""
    
    def __init__(self, token):
        self.api_url = "https://fretefip.up.railway.app/api/external/metrics"
        self.token = token
        self.prefer_method = 'POST'
        
    def consultar_metricas(self, filtros):
        """
        Consulta métricas com fallback automático GET/POST
        
        Args:
            filtros (dict): Dicionário com filtros
            
        Returns:
            dict: Dados da consulta ou None se erro
        """
        if self.prefer_method == 'POST':
            result = self._try_post(filtros)
            if result is None and self._last_error == 405:
                # POST não aceito, tentar GET
                self.prefer_method = 'GET'
                result = self._try_get(filtros)
            return result
        else:
            return self._try_get(filtros)
    
    def _try_post(self, filtros):
        """Tenta POST"""
        try:
            response = requests.post(
                self.api_url,
                json=filtros,
                headers={
                    'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json'
                },
                timeout=30
            )
            
            if response.status_code == 405:
                self._last_error = 405
                return None
            
            if response.status_code == 200:
                return response.json()
            
            self._last_error = response.status_code
            return None
            
        except Exception as e:
            print(f"Erro: {e}")
            return None
    
    def _try_get(self, filtros):
        """Tenta GET"""
        try:
            params = {}
            for key, value in filtros.items():
                if isinstance(value, list):
                    params[key] = json.dumps(value)
                else:
                    params[key] = value
            
            response = requests.get(
                f"{self.api_url}?{urlencode(params)}",
                headers={'Authorization': f'Bearer {self.token}'},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            
            return None
            
        except Exception as e:
            print(f"Erro: {e}")
            return None

# ========== USO ==========
client = FreteAPIClient(token="seu_token_aqui")

resultado = client.consultar_metricas({
    "tipo_frete": "R$/VIAGEM",
    "origem": "CAMPINAS",
    "destino": "SÃO PAULO"
})

if resultado and resultado.get('success'):
    print(f"Registros: {resultado['data']['count']}")
    print(f"Preço médio: R$ {resultado['data']['avg_price']:.2f}")
```

---

### JavaScript (Node.js)

```javascript
const axios = require('axios');

const API_URL = 'https://fretefip.up.railway.app/api/external/metrics';
const TOKEN = 'seu_token_aqui';

// ========== EXEMPLO 1: POST ==========
async function consultarMetricas() {
  try {
    const filtros = {
      tipo_frete: 'R$/VIAGEM',
      origem: 'CAMPINAS',
      destino: 'SÃO PAULO',
      periodo_dias: 90
    };
    
    const response = await axios.post(API_URL, filtros, {
      headers: {
        'Authorization': `Bearer ${TOKEN}`,
        'Content-Type': 'application/json'
      }
    });
    
    const data = response.data;
    
    console.log('✅ Sucesso!');
    console.log(`📊 Registros: ${data.data.count}`);
    console.log(`💰 Preço médio: R$ ${data.data.avg_price.toFixed(2)}`);
    console.log(`📏 Distância média: ${data.data.avg_distance.toFixed(2)} km`);
    
  } catch (error) {
    if (error.response) {
      console.error(`❌ Erro ${error.response.status}:`, error.response.data);
    } else {
      console.error('❌ Erro:', error.message);
    }
  }
}

consultarMetricas();
```

---

### cURL

```bash
# ========== POST (Recomendado) ==========
curl -X POST https://fretefip.up.railway.app/api/external/metrics \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_frete": "R$/VIAGEM",
    "origem": "CAMPINAS",
    "destino": "SÃO PAULO",
    "periodo_dias": 90
  }'

# ========== GET (Alternativo) ==========
curl "https://fretefip.up.railway.app/api/external/metrics?tipo_frete=R$/VIAGEM&origem=CAMPINAS&destino=SÃO%20PAULO&periodo_dias=90" \
  -H "Authorization: Bearer SEU_TOKEN"

# ========== Health Check ==========
curl https://fretefip.up.railway.app/api/external/health
```

---

## 📊 Limites e Quotas

| Recurso | Limite |
|---------|--------|
| **Requisições por dia** | Definido no seu token (padrão: 1000/dia) |
| **Timeout** | 30 segundos |
| **Máximo de registros retornados** | 50.000 registros processados |
| **Tamanho máximo do body (POST)** | 1 MB |
| **Tamanho máximo da URL (GET)** | ~2000 caracteres |

### Verificar uso:
O uso de requisições é rastreado automaticamente. Entre em contato com o suporte se precisar aumentar seu limite diário.

---

## 🚨 Códigos de Erro

| Código | Descrição | Solução |
|--------|-----------|---------|
| **200** | ✅ Sucesso | Dados retornados com sucesso |
| **400** | ❌ Bad Request | Verifique se `tipo_frete` foi informado e está correto |
| **401** | ❌ Unauthorized | Token não fornecido. Adicione o header `Authorization: Bearer TOKEN` |
| **403** | ❌ Forbidden | Token inválido, expirado ou limite diário excedido |
| **404** | ⚠️ Not Found | Nenhum dado encontrado para os filtros. Tente aumentar o período ou remover filtros |
| **405** | ❌ Method Not Allowed | Método HTTP não permitido (use POST ou GET) |
| **429** | ⚠️ Too Many Requests | Limite diário de requisições excedido. Aguarde até amanhã |
| **500** | ❌ Internal Server Error | Erro no servidor. Entre em contato com o suporte |

### Exemplos de Respostas de Erro

**400 - Tipo de frete inválido:**
```json
{
  "error": true,
  "message": "O campo 'tipo_frete' é obrigatório"
}
```

**404 - Nenhum dado encontrado:**
```json
{
  "error": true,
  "message": "Nenhum dado encontrado para os filtros aplicados"
}
```

**403 - Token inválido:**
```json
{
  "error": true,
  "message": "Token inválido, expirado ou limite excedido"
}
```

---

## ❓ FAQ e Troubleshooting

### 1. Qual método devo usar: GET ou POST?

**Recomendação:** Use **POST** sempre que possível.

- ✅ **POST:** Mais seguro, suporta filtros complexos, sem limite de tamanho
- ⚠️ **GET:** Alternativa para compatibilidade, limitado a ~2000 caracteres

### 2. Quais tipos de frete posso usar?

**APENAS:**
- `"R$/VIAGEM"` - Preço total da viagem
- `"R$/UND"` - Preço por unidade/tonelada

❌ Não use: "CIF", "FOB", "cif", "fob", etc.

### 3. Por que estou recebendo 404?

**Possíveis causas:**
1. ❌ `tipo_frete` incorreto (use `R$/VIAGEM` ou `R$/UND`)
2. ⚠️ Filtros muito específicos (ex: cidade + produto que não existem juntos)
3. ⚠️ Período muito curto

**Soluções:**
- Verifique se o `tipo_frete` está correto
- Remova alguns filtros para ampliar a busca
- Aumente o `periodo_dias` (ex: 120 ou 180 dias)

### 4. Como passar arrays no GET?

**Opção 1: JSON string**
```
?produtos=["SOJA","MILHO"]
```

**Opção 2: Múltiplos parâmetros**
```
?produtos=SOJA&produtos=MILHO
```

### 5. Meu token está funcionando?

**Teste rápido:**
```bash
curl https://fretefip.up.railway.app/api/external/metrics?tipo_frete=R$/VIAGEM \
  -H "Authorization: Bearer SEU_TOKEN"
```

- ✅ 200 ou 404: Token válido
- ❌ 401: Token não fornecido
- ❌ 403: Token inválido ou limite excedido

### 6. Como sei se atingi o limite diário?

Você receberá erro **403** com mensagem indicando limite excedido.

### 7. Posso filtrar por múltiplos produtos?

Sim! Use um array:
```json
{
  "tipo_frete": "R$/VIAGEM",
  "produtos": ["SOJA", "MILHO", "FERTILIZANTE"]
}
```

### 8. Como obter dados de um mês específico?

Use `periodo_dias` baseado na data atual:
```json
{
  "tipo_frete": "R$/VIAGEM",
  "periodo_dias": 30  // Últimos 30 dias
}
```

### 9. A API retorna dados em tempo real?

Não. A API retorna **estatísticas agregadas** baseadas em dados históricos. Não retorna registros individuais.

### 10. Posso salvar/exportar os dados?

Sim! Salve a resposta JSON:
```python
import json

response = requests.post(...)
with open('metricas.json', 'w') as f:
    json.dump(response.json(), f, indent=2)
```

---

## 📞 Suporte

**Para dúvidas, problemas ou solicitação de token:**

- 📧 Email: inteligencia@tmtlog.com
- 🌐 Site: https://fretefip.com.br


---

## 📝 Changelog

### v1.0.0 (Setembro 2025)
- ✅ Lançamento inicial da API
- ✅ Endpoints: `/health` e `/metrics`
- ✅ Suporte para GET e POST
- ✅ Autenticação via token
- ✅ Limite diário de requisições
- ✅ Tipos de frete: `R$/VIAGEM` e `R$/UND`

---

## 📄 Termos de Uso

1. Use seu token apenas para sua organização
2. Não compartilhe seu token publicamente
3. Respeite os limites de requisições
4. Os dados são fornecidos "como estão"
5. Entre em contato para uso comercial de alto volume

---

**Última atualização:** 30/09/2025  
**Versão da API:** 1.0.0