"""
Cliente da API que funciona COM OU SEM o problema de redirect
Tenta POST primeiro, se der 405 tenta GET
"""
import requests
import json
from urllib.parse import urlencode

class FreteAPIClient:
    """Cliente inteligente que adapta ao método aceito"""
    
    def __init__(self, api_url, token):
        self.api_url = api_url
        self.token = token
        self.prefer_method = 'POST'  # Preferência inicial
        
    def consultar_metricas(self, filtros):
        """
        Consulta métricas adaptando ao método aceito pelo servidor
        
        Args:
            filtros (dict): Filtros da consulta
            
        Returns:
            dict: Dados ou None se erro
        """
        
        # Tentar com método preferido
        if self.prefer_method == 'POST':
            response = self._try_post(filtros)
            
            # Se POST não funcionar (405), tentar GET
            if response is None:
                print("⚠️  POST falhou, tentando GET...")
                self.prefer_method = 'GET'  # Mudar preferência
                response = self._try_get(filtros)
        else:
            response = self._try_get(filtros)
        
        return response
    
    def _try_post(self, filtros):
        """Tenta requisição POST"""
        try:
            print(f"📤 Tentando POST: {self.api_url}")
            
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
                print("❌ POST não aceito (405)")
                return None
            
            return self._handle_response(response, 'POST')
            
        except Exception as e:
            print(f"❌ Erro no POST: {str(e)}")
            return None
    
    def _try_get(self, filtros):
        """Tenta requisição GET com query parameters"""
        try:
            print(f"📤 Tentando GET: {self.api_url}")
            
            # Converter filtros para query params
            params = {}
            
            # 🔧 ADICIONAR TOKEN aos query params (GET precisa dele na URL!)
            params['token'] = self.token
            
            for key, value in filtros.items():
                if isinstance(value, list):
                    # Arrays viram JSON string
                    params[key] = json.dumps(value)
                else:
                    params[key] = value
            
            # Construir URL com query params
            url_with_params = f"{self.api_url}?{urlencode(params)}"
            
            response = requests.get(
                url_with_params,
                headers={
                    'Authorization': f'Bearer {self.token}'  # Enviar também no header
                },
                timeout=30
            )
            
            return self._handle_response(response, 'GET')
            
        except Exception as e:
            print(f"❌ Erro no GET: {str(e)}")
            return None
    
    def _handle_response(self, response, method):
        """Processa resposta HTTP"""
        print(f"📥 {method} retornou: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ Sucesso com {method}!")
            return response.json()
        
        elif response.status_code == 404:
            print("⚠️  Nenhum dado encontrado (404)")
            try:
                error = response.json()
                print(f"   {error.get('message', '')}")
            except:
                pass
            return None
        
        elif response.status_code == 401:
            print("❌ Token não fornecido (401)")
            return None
        
        elif response.status_code == 403:
            print("❌ Token inválido ou limite excedido (403)")
            return None
        
        else:
            print(f"❌ Erro {response.status_code}")
            try:
                error = response.json()
                print(f"   {error.get('message', '')}")
            except:
                print(f"   {response.text[:200]}")
            return None

# ========== EXEMPLO DE USO ==========

def main():
    print("="*70)
    print("🚀 CLIENTE INTELIGENTE - Funciona com GET ou POST")
    print("="*70)
    
    API_URL = "https://fretefip.up.railway.app/api/external/metrics"
    TOKEN = "035a907146952334e67d3414ae11bce69cb29132cbdce59102bdea63f14f4fcb"  # Substitua pelo seu token válido
    
    client = FreteAPIClient(API_URL, TOKEN)
    
    # Teste 1: Consulta básica
    print("\n" + "="*70)
    print("TESTE 1: Consulta Básica")
    print("="*70)
    
    filtros = {
        "tipo_frete": "R$/UND",
        "origem": "RONDONÓPOLIS",
        "periodo_dias": 30
    }
    
    resultado = client.consultar_metricas(filtros)
    
    if resultado and resultado.get('success'):
        print("\n📊 RESULTADO:")
        print(f"   Registros: {resultado['data']['count']}")
        print(f"   Preço médio: R$ {resultado['data']['avg_price']:.2f}")
        print(f"   Distância média: {resultado['data']['avg_distance']:.2f} km")
        print(f"   Método usado: {client.prefer_method}")
    else:
        print("\n❌ Consulta falhou")
    
    # Teste 2: Consulta com múltiplos filtros
    print("\n" + "="*70)
    print("TESTE 2: Múltiplos Filtros")
    print("="*70)
    
    filtros = {
        "tipo_frete": "R$/UND",
        "origem": "SINOP",
        "destino": "ITAITUBA",
        "produtos": ["SOJA"],
        "periodo_dias": 30
    }
    
    resultado = client.consultar_metricas(filtros)
    
    if resultado and resultado.get('success'):
        print("\n📊 RESULTADO:")
        print(f"   Registros: {resultado['data']['count']}")
        print(f"   Preço médio: R$ {resultado['data']['avg_price']:.2f}")
        print(f"   Produtos: {', '.join(resultado['filters_applied']['produtos'])}")
        print(f"   Método usado: {client.prefer_method}")
    else:
        print("\n❌ Consulta falhou")
    
    print("\n" + "="*70)
    print("✅ Testes concluídos!")
    print(f"💡 API está aceitando: {client.prefer_method}")
    print("="*70)

if __name__ == "__main__":
    main()