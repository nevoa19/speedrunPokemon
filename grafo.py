import pandas as pd
from collections import defaultdict

class GrafoPokemon:
    def __init__(self, path_excel):
        self.vertices = {}        # nome: { 'matos': int }
        self.adjacencias = defaultdict(list)  # nome: lista de conexões
        self.obstaculos = {}      # (origem, destino): obstáculo
        self.custos = {}          # (origem, destino): custo
        self._carregar_dados(path_excel)

    def _carregar_dados(self, path_excel):
        xls = pd.ExcelFile(path_excel)
        vertices_df = pd.read_excel(xls, sheet_name="Vértices - Mapa")
        arestas_df = pd.read_excel(xls, sheet_name="Arestas - Mapa")

        for _, row in vertices_df.iterrows():
            nome = row["Localidade"]
            matos = row["Matos obrigatórios"]
            self.vertices[nome] = {"matos": int(matos)}

        for _, row in arestas_df.iterrows():
            origem = row["Local saída"]
            destino = row["Local destino"]
            obstaculo = str(row["Obstáculo no trajeto"]) if not pd.isna(row["Obstáculo no trajeto"]) else ""
            custo = int(row["Custo"])

            self.adjacencias[origem].append(destino)
            self.adjacencias[destino].append(origem)
            self.custos[(origem, destino)] = custo
            self.custos[(destino, origem)] = custo
            self.obstaculos[(origem, destino)] = obstaculo
            self.obstaculos[(destino, origem)] = obstaculo

    def vizinhos(self, local):
        return self.adjacencias.get(local, [])

    def custo_entre(self, origem, destino):
        return self.custos.get((origem, destino), float('inf'))

    def obstaculo_entre(self, origem, destino):
        return self.obstaculos.get((origem, destino), None)

    def matos_obrigatorios(self, local):
        return self.vertices.get(local, {}).get("matos", 0)
