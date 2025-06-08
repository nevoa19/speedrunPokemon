import random
from simulador import EVENTOS_ESPECIAIS, REQUISITOS_LOCAL

class Individuo:
    def __init__(self, caminho, grafo):
        self.caminho = caminho
        self.grafo = grafo
        self.fitness = None
        self.avaliar()

    def avaliar(self):
        custo_total = 0
        insignias = set()
        for origem, destino in zip(self.caminho, self.caminho[1:]):
            requisitos = REQUISITOS_LOCAL.get(destino, [])
            if not all(ins in insignias for ins in requisitos):
                custo_total += 99999
                continue

            custo = self.grafo.get_custo(origem, destino, incluir_mato=True)
            custo_total += 9999 if custo == float('inf') else custo

            if destino in EVENTOS_ESPECIAIS:
                insignias.add(EVENTOS_ESPECIAIS[destino])

        self.fitness = -custo_total


class AlgoritmoGenetico:
    def __init__(self, grafo, tamanho_populacao=50, geracoes=100, taxa_mutacao=0.1):
        self.grafo = grafo
        self.tamanho_populacao = tamanho_populacao
        self.geracoes = geracoes
        self.taxa_mutacao = taxa_mutacao
        self.populacao = []

    def gerar_populacao_inicial(self):
        locais = list(self.grafo.vertices)
        for _ in range(self.tamanho_populacao):
            caminho = random.sample(locais, k=len(locais))
            self.populacao.append(Individuo(caminho, self.grafo))

    def selecao(self):
        return sorted(self.populacao, key=lambda x: x.fitness, reverse=True)[:2]

    def crossover(self, pai1, pai2):
        meio = len(pai1.caminho) // 2
        inicio = pai1.caminho[:meio]
        resto = [x for x in pai2.caminho if x not in inicio]
        filho_caminho = inicio + resto
        return Individuo(filho_caminho, self.grafo)

    def mutacao(self, individuo):
        caminho = individuo.caminho[:]
        if random.random() < self.taxa_mutacao:
            i, j = random.sample(range(len(caminho)), 2)
            caminho[i], caminho[j] = caminho[j], caminho[i]
        return Individuo(caminho, self.grafo)

    def executar(self):
        self.gerar_populacao_inicial()
        for gen in range(self.geracoes):
            nova_populacao = []
            for _ in range(self.tamanho_populacao):
                pais = self.selecao()
                filho = self.crossover(pais[0], pais[1])
                filho_mutado = self.mutacao(filho)
                nova_populacao.append(filho_mutado)

            self.populacao = nova_populacao
            melhor = max(self.populacao, key=lambda x: x.fitness)
            print(f"Geração {gen+1}: Melhor Fitness = {melhor.fitness}")

        return max(self.populacao, key=lambda x: x.fitness)
