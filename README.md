# 🚚 API de Métricas de Frete - Início Rápido

> **URL Base:** `https://fretefip.up.railway.app/api/external`

---

## 🎯 O que esta API faz?

Retorna **estatísticas** sobre fretes no Brasil:
- 💰 Preço médio, mínimo e máximo
- 📏 Distância média
- 📊 Quantidade de registros
- 📈 Desvio padrão

---

## 🚀 Início Rápido (3 passos)

### 1️⃣ Obtenha seu Token
Entre em contato para receber seu token de acesso.

### 2️⃣ Teste a API
```bash
curl "https://fretefip.up.railway.app/api/external/metrics?tipo_frete=R$/VIAGEM" \
  -H "Authorization: Bearer SEU_TOKEN"
```

### 3️⃣ Use em Python
```python
import requests

API_URL = "https://fretefip.up.railway.app/api/external/metrics"
TOKEN = "seu_token_aqui"

filtros = {
    "tipo_frete": "R$/VIAGEM",
    "origem": "CAMPINAS",
    "destino": "SÃO PAULO"
}

response = requests.post(
    API_URL,
    json=filtros,
    headers={"Authorization": f"Bearer {TOKEN}"}
)

if response.status_code == 200:
    data = response.json()
    print(f"Preço médio: R$ {data['data']['avg_price']:.2f}")
```

---

## 📋 Campos Obrigatórios

**APENAS 1 campo é obrigatório:**

| Campo | Valores Aceitos | Exemplo |
|-------|----------------|---------|
| `tipo_frete` | `"R$/VIAGEM"` ou `"R$/UND"` | `"R$/VIAGEM"` |

⚠️ **IMPORTANTE:** Use exatamente `"R$/VIAGEM"` ou `"R$/UND"` (com barras e $)

---

## 🎛️ Filtros Opcionais

| Campo | Tipo | Exemplo |
|-------|------|---------|
| `origem` | texto | `"CAMPINAS"` |
| `destino` | texto | `"SÃO PAULO"` |
| `cod_ibge_origem` | texto | `"3509502"` |
| `cod_ibge_destino` | texto | `"3550308"` |
| `uf_origem` | sigla UF | `"SP"` |
| `uf_destino` | sigla UF | `"RJ"` |
| `meso_origem` | texto | `"CAMPINAS"` |
| `meso_destino` | texto | `"METROPOLITANA DE SÃO PAULO"` |
| `produtos` | lista | `["SOJA", "MILHO"]` |
| `veiculos` | lista | `["CARRETA", "TRUCK"]` |
| `carrocerias` | lista | `["SIDER", "GRANELEIRO"]` |
| `periodo_dias` | número | `90` (padrão: 120) |

### 🆕 Busca por Código IBGE

Você pode usar o **código IBGE** da cidade ao invés do nome:

```python
filtros = {
    "tipo_frete": "R$/UND",
    "cod_ibge_origem": "5107909",   # SINOP - MT
    "cod_ibge_destino": "1503606",  # ITAITUBA - PA
    "produtos": ["SOJA"]
}
```

> 💡 **Dica:** O código IBGE é útil quando você já tem os códigos no seu sistema e quer evitar erros de digitação nos nomes das cidades.

---

## 💡 Exemplos Práticos

### Exemplo 1: Consulta Mais Simples
```python
filtros = {
    "tipo_frete": "R$/VIAGEM"
}
```

### Exemplo 2: Rota Específica
```python
filtros = {
    "tipo_frete": "R$/VIAGEM",
    "origem": "CAMPINAS",
    "destino": "SÃO PAULO",
    "periodo_dias": 60
}
```

### Exemplo 3: Filtrar por Estado e Produto
```python
filtros = {
    "tipo_frete": "R$/UND",
    "uf_origem": "MT",
    "uf_destino": "SP",
    "produtos": ["SOJA", "MILHO"],
    "periodo_dias": 90
}
```

### Exemplo 4: Usando Código IBGE
```python
filtros = {
    "tipo_frete": "R$/UND",
    "cod_ibge_origem": "5107909",   # SINOP - MT
    "cod_ibge_destino": "1503606",  # ITAITUBA - PA
    "produtos": ["SOJA"],
    "periodo_dias": 60
}
```

### Exemplo 5: Usando GET (alternativa)
```bash
curl "https://fretefip.up.railway.app/api/external/metrics?tipo_frete=R$/VIAGEM&origem=CAMPINAS&destino=SÃO%20PAULO" \
  -H "Authorization: Bearer SEU_TOKEN"
```

---

## 📊 Resposta da API

```json
{
  "success": true,
  "data": {
    "count": 1500,
    "avg_price": 5000.00,
    "avg_distance": 850.50,
    "min_price": 2000.00,
    "max_price": 12000.00,
    "std_dev": 1500.00
  },
  "filters_applied": {
    "tipo_frete": "R$/VIAGEM",
    "origem": "CAMPINAS",
    "destino": "SÃO PAULO"
  },
  "period": {
    "start_date": "2024-06-01",
    "end_date": "2024-09-30",
    "days": 90
  }
}
```

---

## ❌ Erros Comuns

### 404 - Nenhum dado encontrado
```json
{
  "error": true,
  "message": "Nenhum dado encontrado para os filtros aplicados"
}
```

**Soluções:**
- ✅ Verifique se `tipo_frete` está correto (`R$/VIAGEM` ou `R$/UND`)
- ✅ Remova alguns filtros para ampliar a busca
- ✅ Aumente o `periodo_dias`

### 401 - Token não fornecido
```json
{
  "error": true,
  "message": "Token de API não fornecido"
}
```

**Solução:** Adicione o header `Authorization: Bearer SEU_TOKEN`

### 403 - Token inválido
```json
{
  "error": true,
  "message": "Token inválido, expirado ou limite excedido"
}
```

**Soluções:**
- ✅ Verifique se o token está correto
- ✅ Verifique se não excedeu o limite diário

---

## 📦 Arquivos Disponíveis

1. **📚 `API_DOCUMENTACAO_COMPLETA.md`** - Documentação detalhada
2. **💻 `exemplo.py`** - Exemplos práticos em Python
3. **📄 `README.md`** - Este arquivo (início rápido)

---

## 🔧 Métodos Aceitos

A API aceita **POST** (recomendado) e **GET**:

### POST (Recomendado)
```python
response = requests.post(
    API_URL,
    json=filtros,
    headers={"Authorization": f"Bearer {TOKEN}"}
)
```

**Vantagens:**
- ✅ Mais seguro (dados no body)
- ✅ Sem limite de tamanho
- ✅ Filtros complexos

### GET (Alternativa)
```python
response = requests.get(
    f"{API_URL}?tipo_frete=R$/VIAGEM&origem=CAMPINAS",
    headers={"Authorization": f"Bearer {TOKEN}"}
)
```

**Vantagens:**
- ✅ Mais simples para testes rápidos
- ✅ Funciona no navegador

---

## 📊 Limites

- **Requisições por dia:** 1000 (padrão)
- **Timeout:** 30 segundos
- **Registros processados:** até 10.000

---

## 📞 Suporte

**Problemas ou dúvidas?**

- 📧 Email: inteligencia@tmtlog.com
- 🌐 Site: https://fretefip.com.br

---

## ✅ Checklist Rápido

- [ ] Recebi meu token
- [ ] Testei com `curl`
- [ ] Usei `"R$/VIAGEM"` ou `"R$/UND"` em `tipo_frete`
- [ ] Adicionei header `Authorization: Bearer TOKEN`
- [ ] Li a documentação completa

---

## 🎬 Próximos Passos

1. ✅ Execute o arquivo `exemplo_api_completo.py`
2. ✅ Teste diferentes combinações de filtros
3. ✅ Integre na sua aplicação
4. ✅ Leia a documentação completa para detalhes

---

**Versão:** 1.1.0
**Última atualização:** 16/12/2025

---

## 📝 Exemplo Completo de Integração

```python
#!/usr/bin/env python3
"""
Script de exemplo - Consulta API de Fretes
"""
import requests

# Configuração
API_URL = "https://fretefip.up.railway.app/api/external/metrics"
TOKEN = "seu_token_aqui"  # Substitua aqui!

def consultar_frete(tipo_frete, origem=None, destino=None, periodo=90):
    """Consulta métricas de frete"""
    
    filtros = {"tipo_frete": tipo_frete, "periodo_dias": periodo}
    
    if origem:
        filtros["origem"] = origem
    if destino:
        filtros["destino"] = destino
    
    try:
        response = requests.post(
            API_URL,
            json=filtros,
            headers={"Authorization": f"Bearer {TOKEN}"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro {response.status_code}: {response.json()}")
            return None
            
    except Exception as e:
        print(f"Erro: {e}")
        return None

# Usar
resultado = consultar_frete(
    tipo_frete="R$/VIAGEM",
    origem="CAMPINAS",
    destino="SÃO PAULO",
    periodo=60
)

if resultado and resultado.get('success'):
    data = resultado['data']
    print(f"✅ Encontrados {data['count']} registros")
    print(f"💰 Preço médio: R$ {data['avg_price']:.2f}")
    print(f"📏 Distância média: {data['avg_distance']:.2f} km")
else:
    print("❌ Consulta sem resultados")
```


---

**🎉 Pronto para começar!**
