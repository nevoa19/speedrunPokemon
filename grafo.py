import pandas as pd

class GrafoPokemon:
    def __init__(self, caminho_arquivo):
        self.vertices = set()
        self.arestas = {}  # { origem: { destino: custo } }
        self.matos = {}    # { localidade: quantidade de mato obrigatório }
        self.carregar_grafo(caminho_arquivo)

    def carregar_grafo(self, caminho_arquivo):
        df_arestas = pd.read_excel(caminho_arquivo, sheet_name="Arestas - Mapa")
        for _, row in df_arestas.iterrows():
            origem = row["Local saída"]
            destino = row["Local destino"]
            custo = row["Custo"]

            self.vertices.update([origem, destino])
            self.arestas.setdefault(origem, {})[destino] = custo
            self.arestas.setdefault(destino, {})[origem] = custo

        df_matos = pd.read_excel(caminho_arquivo, sheet_name="Vértices - Mapa")
        for _, row in df_matos.iterrows():
            local = row["Localidade"]
            mato = row["Matos obrigatórios"]
            self.matos[local] = mato if not pd.isna(mato) else 0

    def get_custo(self, origem, destino, incluir_mato=True):
        """
        Retorna o custo de viajar de origem para destino.
        Se incluir_mato=True, soma o número de matos obrigatórios da origem + destino como penalidade.
        """
        try:
            custo_base = self.arestas[origem][destino]
        except KeyError:
            return float('inf')

        if incluir_mato:
            mato_origem = self.matos.get(origem, 0)
            mato_destino = self.matos.get(destino, 0)
            penalidade = mato_origem + mato_destino
            return custo_base + penalidade

        return custo_base

    def vizinhos(self, local):
        """Retorna os vizinhos conectados a uma localidade."""
        return self.arestas.get(local, {})
