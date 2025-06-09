import pandas as pd
import random
from grafo import GrafoPokemon
from genetic import AlgoritmoGenetico
from simulador import Jogador, EVENTOS_ESPECIAIS

pokedex_df = pd.read_excel("dados_pokemon_red.xlsx", sheet_name="Pokedex")
ataques_df = pd.read_excel("dados_pokemon_red.xlsx", sheet_name="Aprendizado de Ataques")

grafo = GrafoPokemon("dados_pokemon_red.xlsx")
ag = AlgoritmoGenetico(grafo, tamanho_populacao=30, geracoes=50, taxa_mutacao=0.1)
melhor_rota = ag.executar().caminho

jogador = Jogador("Ash", pokedex_df, ataques_df)

for local in melhor_rota:
    tentativas = 0
    sucesso = False

    while tentativas < 3 and not sucesso:
        pode_ir = jogador._pode_visitar(local)

        if not pode_ir:
            print(f"{jogador.nome} não pode acessar {local} ainda.")
            break

        pre_insignias = set(jogador.insignias)
        pre_batalhas = jogador.total_batalhas

        jogador.explorar(local)

        ganhou_insignia = jogador.insignias != pre_insignias
        fez_batalha = jogador.total_batalhas > pre_batalhas

        if ganhou_insignia or local not in EVENTOS_ESPECIAIS:
            sucesso = True
        else:
            treino_rotas = ["Route 1", "Route 2", "Route 3", "Route 6", "Route 22", "Route 24"]
            for treino in treino_rotas:
                jogador.explorar(treino)

        tentativas += 1

while "Elite Four" not in jogador.insignias:
    print("\nAinda não venceu a Elite Four. Explorando novamente...")
    nova_rota = random.sample(list(grafo.vertices), k=len(grafo.vertices))
    for local in nova_rota:
        jogador.explorar(local)
        if "Elite Four" in jogador.insignias:
            break

print("\nAsh venceu a Elite Four! Parabéns, campeão da Liga Pokémon!")
jogador.resumo()