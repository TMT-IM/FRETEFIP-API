"""
Cliente da API de Projeções que funciona COM OU SEM o problema de redirect
Tenta POST primeiro, se der 405 tenta GET
"""
import requests
import json
from urllib.parse import urlencode

class ForecastAPIClient:
    """Cliente inteligente que adapta ao método aceito"""

    def __init__(self, api_url, token):
        self.api_url = api_url
        self.token = token
        self.prefer_method = 'POST'  # Preferência inicial

    def consultar_projecoes(self, dados):
        """
        Consulta projeções adaptando ao método aceito pelo servidor

        Args:
            dados (dict): Dados da consulta (origem, destino, produtos, etc)

        Returns:
            dict: Dados ou None se erro
        """

        # Tentar com método preferido
        if self.prefer_method == 'POST':
            response = self._try_post(dados)

            # Se POST não funcionar (405), tentar GET
            if response is None:
                print("⚠️  POST falhou, tentando GET...")
                self.prefer_method = 'GET'  # Mudar preferência
                response = self._try_get(dados)
        else:
            response = self._try_get(dados)

        return response

    def _try_post(self, dados):
        """Tenta requisição POST"""
        try:
            print(f"📤 Tentando POST: {self.api_url}")

            response = requests.post(
                self.api_url,
                json=dados,
                headers={
                    'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json'
                },
                timeout=60  # Modelo pode demorar
            )

            if response.status_code == 405:
                print("❌ POST não aceito (405)")
                return None

            return self._handle_response(response, 'POST')

        except Exception as e:
            print(f"❌ Erro no POST: {str(e)}")
            return None

    def _try_get(self, dados):
        """Tenta requisição GET com query parameters"""
        try:
            print(f"📤 Tentando GET: {self.api_url}")

            # Converter dados para query params
            params = {}

            # Adicionar token aos query params
            params['token'] = self.token

            for key, value in dados.items():
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
                    'Authorization': f'Bearer {self.token}'
                },
                timeout=60
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
            print("⚠️  Rota não encontrada (404)")
            try:
                error = response.json()
                print(f"   {error.get('message', '')}")
                if 'suggestion' in error:
                    print(f"   💡 {error['suggestion']}")
            except:
                pass
            return None

        elif response.status_code == 401:
            print("❌ Token não fornecido (401)")
            return None

        elif response.status_code == 403:
            print("❌ Token inválido ou limite excedido (403)")
            return None

        elif response.status_code == 400:
            print("⚠️  Requisição inválida (400)")
            try:
                error = response.json()
                print(f"   {error.get('message', '')}")
            except:
                pass
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
    print("🚀 CLIENTE API DE PROJEÇÕES - Funciona com GET ou POST")
    print("="*70)

    # CONFIGURAÇÃO
    API_URL = "https://fretefip.up.railway.app/api/forecast/predict"
    TOKEN = "SEU_TOKEN_AQUI"

    client = ForecastAPIClient(API_URL, TOKEN)

    # Projeção de 12 meses
    print("\n" + "="*70)
    print("EXEMPLO: Projeção SINOP → ITAITUBA (12 meses)")
    print("="*70)

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

        print("\n📊 RESULTADO:")
        print(f"   Total de previsões: {len(previsoes)}")
        print(f"   Previsões por mês: 4 (dias 1, 10, 15, 25)")

        # Estatísticas
        stats = resultado['statistics']
        print(f"\n💰 Preços:")
        print(f"   Médio:  R$ {stats['avg_price']:.2f}")
        print(f"   Mínimo: R$ {stats['min_price']:.2f}")
        print(f"   Máximo: R$ {stats['max_price']:.2f}")

        # Rota
        route = resultado['route_info']
        print(f"\n🗺️  Rota:")
        print(f"   {route['origem']}/{route['uf_origem']} → {route['destino']}/{route['uf_destino']}")
        print(f"   Distância: {route['km']:.2f} km")

        # Todas as previsões
        print(f"\n📅 Previsões (48 totais):")
        for i, forecast in enumerate(previsoes, 1):
            data = forecast['date'].split('T')[0]
            print(f"   {i:2d}. {data}: R$ {forecast['preco_previsto']:>10,.2f}")

        print(f"\n💡 Método usado: {client.prefer_method}")
    else:
        print("\n❌ Consulta falhou")

    print("\n" + "="*70)
    print("✅ Teste concluído!")
    print(f"💡 API está aceitando: {client.prefer_method}")
    print("="*70)

if __name__ == "__main__":
    main()
