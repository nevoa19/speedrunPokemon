import pandas as pd
from grafo import GrafoPokemon
from genetic import AlgoritmoGenetico
from simulador import Jogador

pokedex_df = pd.read_excel("dados_pokemon_red.xlsx", sheet_name="Pokedex")
ataques_df = pd.read_excel("dados_pokemon_red.xlsx", sheet_name="Aprendizado de Ataques")

grafo = GrafoPokemon("dados_pokemon_red.xlsx")
ag = AlgoritmoGenetico(grafo, tamanho_populacao=30, geracoes=50, taxa_mutacao=0.1)
melhor_rota = ag.executar().caminho

jogador = Jogador("Ash", pokedex_df, ataques_df)
for local in melhor_rota:
    jogador.explorar(local)
    if local == "Indigo Plateau":
        break