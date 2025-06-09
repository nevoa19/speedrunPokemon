import random
import pandas as pd
import math
from utils import POKEMONS_INICIAIS, POKEMONS_POR_ROTA, EFICACIA_TIPOS, EVENTOS_ESPECIAIS, REQUISITOS_LOCAL

class Jogador:
    def __init__(self, nome, pokedex_df, ataques_df):
        self.nome = nome
        self.pokedex_df = pokedex_df
        self.ataques_df = ataques_df
        inicial = random.choice(POKEMONS_INICIAIS)
        print(f"{nome} escolheu o Pokémon inicial: {inicial}!")
        self.time = [Pokemon(self.pokedex_df[self.pokedex_df["Pokémon"] == inicial].iloc[0], self.ataques_df)]
        self.pokebolas = 5
        self.rota_percorrida = []
        self.vitorias = 0
        self.total_batalhas = 0
        self.insignias = set()

    def explorar(self, local):
        if not self._pode_visitar(local):
            print(f"{self.nome} não pode acessar {local} ainda.")
            return

        print(f"{self.nome} chegou em {local}")
        self.rota_percorrida.append(local)

        if local in EVENTOS_ESPECIAIS:
            lider = EVENTOS_ESPECIAIS[local]
            if lider not in self.insignias:
                print(f"{self.nome} enfrentou o líder {lider}!")
                venceu = self._batalha_ginasio(lider)
                if venceu:
                    print(f"{self.nome} venceu {lider} e ganhou a insígnia!")
                    self.insignias.add(lider)
                else:
                    print(f"{self.nome} perdeu para {lider}. Volta ao Centro Pokémon.")
                    return
            if lider == "Elite Four" and venceu:
                print(f"{self.nome} venceu a Elite Four e finalizou a jornada!")
                self.insignias.add("Elite Four")

        if self._chance_encontro():
            inimigo = self._gerar_inimigo(local)
            print(f"Encontrou um {inimigo.nome} selvagem!")
            self._batalhar(inimigo)

    def _pode_visitar(self, local):
        requisitos = REQUISITOS_LOCAL.get(local, [])
        return all(ins in self.insignias for ins in requisitos)

    def _batalha_ginasio(self, lider):
        meu = self.time[0]
        chance = 0.7 if meu.nivel >= 10 else 0.3
        return random.random() < chance

    def _chance_encontro(self):
        return random.random() < 0.4

    def _gerar_inimigo(self, local):
        pool = POKEMONS_POR_ROTA.get(local, ["Pidgey", "Rattata"])
        especie = random.choice(pool)
        nivel = random.randint(2, 5)
        return Pokemon(self.pokedex_df[self.pokedex_df["Pokémon"] == especie].iloc[0], self.ataques_df, nivel)

    def _batalhar(self, inimigo):
        meu = self.time[0]
        print(f"Batalha: {meu.nome} (Nv {meu.nivel}) vs {inimigo.nome} (Nv {inimigo.nivel})")
        self.total_batalhas += 1
        chance = 0.7 if meu.nivel >= inimigo.nivel else 0.3
        if random.random() < chance:
            print(f"Vitória! Ganhou {inimigo.base_exp_yield} XP")
            self.vitorias += 1
            meu.ganhar_xp(inimigo.base_exp_yield)
            if self._pode_capturar():
                self._tentar_captura(inimigo)
        else:
            print("Derrota! Volta ao Centro Pokémon")

    def _pode_capturar(self):
        return self.pokebolas > 0 and len(self.time) < 6

    def _tentar_captura(self, inimigo):
        print(f"Tentando capturar {inimigo.nome}...")
        taxa = inimigo.taxa_captura / 255
        sucesso = random.random() < taxa
        self.pokebolas -= 1
        if sucesso:
            print(f"Capturou {inimigo.nome}!")
            self.time.append(inimigo)
        else:
            print(f"{inimigo.nome} escapou...")

    def resumo(self):
        print("\nRESUMO DA AVENTURA:")
        print(f"- Locais visitados: {len(self.rota_percorrida)}")
        print(f"- Batalhas realizadas: {self.total_batalhas}")
        print(f"- Vitórias: {self.vitorias}")
        print(f"- Pokémon capturados: {len(self.time)}")
        print(f"- Pokébolas restantes: {self.pokebolas}")
        if self.total_batalhas > 0:
            taxa = (self.vitorias / self.total_batalhas) * 100
            print(f"- Taxa de sucesso nas batalhas: {taxa:.2f}%")
        else:
            print("- Nenhuma batalha aconteceu.")

class Especie:
    def __init__(self, dados):
        self.numero = int(dados["Número"])
        self.nome = dados["Pokémon"]
        self.hp_base = int(dados["HP"])
        self.atk_base = int(dados["Ataque"])
        self.def_base = int(dados["Defesa"])
        self.spd_base = int(dados["Velocidade"])
        self.spc_base = int(dados["Especial"])
        self.tipo1 = dados["Tipo 1"]
        self.tipo2 = dados["Tipo 2"] if not pd.isna(dados["Tipo 2"]) else None
        self.curva_exp = dados["Crescimento em exp"]
        self.base_exp_yield = int(dados["Experiência que distribui"])
        self.taxa_captura = int(dados["Taxa de captura"])

class Pokemon(Especie):
    def __init__(self, dados_pokedex, ataques_df, nivel=5):
        super().__init__(dados_pokedex)
        self.nivel = nivel
        self.xp = self.get_xp_por_nivel(nivel)
        self.hp_iv = self.gerar_iv()
        self.atk_iv = self.gerar_iv()
        self.def_iv = self.gerar_iv()
        self.spc_iv = self.gerar_iv()
        self.spd_iv = self.gerar_iv()
        self.hp_atual = self.calcular_hp()
        self.golpes = self.get_golpes(ataques_df)

    def gerar_iv(self):
        return random.randint(0, 15)

    def calcular_hp(self):
        return math.floor((((self.hp_base + self.hp_iv) * 2 * self.nivel) / 100) + self.nivel + 10)

    def get_xp_por_nivel(self, nivel):
        if self.curva_exp == "Fast":
            return int(4 * (nivel ** 3) / 5)
        elif self.curva_exp == "Medium Fast":
            return int(nivel ** 3)
        elif self.curva_exp == "Medium Slow":
            return int((6/5) * (nivel ** 3) - 15 * (nivel ** 2) + 100 * nivel - 140)
        elif self.curva_exp == "Slow":
            return int(5 * (nivel ** 3) / 4)
        else:
            return 0

    def get_golpes(self, ataques_df):
        ataques_df = ataques_df.copy()
        ataques_df["Nível"] = pd.to_numeric(ataques_df["Nível"], errors='coerce')
        ataques_df = ataques_df.dropna(subset=["Nível"])
        ataques_df["Nível"] = ataques_df["Nível"].astype(int)
        golpes = ataques_df[
            (ataques_df["Pokémon"] == self.nome) &
            (ataques_df["Nível"] <= self.nivel)
        ]
        return golpes

    def ganhar_xp(self, xp_ganho):
        self.xp += xp_ganho
        novo_nivel = 1
        while self.get_xp_por_nivel(novo_nivel + 1) <= self.xp:
            novo_nivel += 1
        if novo_nivel > self.nivel:
            print(f"{self.nome} subiu para o nível {novo_nivel}!")
            self.nivel = novo_nivel
            self.hp_atual = self.calcular_hp()