import random

class Tipo:
    def __init__(self,nome,vantagens_defensivas,desvantagens_defensivas,imunidades):
        self.Nome = nome
        self.Vantagem_defensiva = vantagens_defensivas
        self.Desvantagem_defensiva = desvantagens_defensivas
        self.Imunidade = imunidades


class Curva_EXP:
    def __init__(self,Nome,Lvl,EXP):
        


class Especie:
    def __init__(self,Numero,Nome,HP_base,Atk_base,Def_base,Spc_base,Spd_base,Tipos,Taxa_captura,Exp_type,Base_exp_yield):
        self.Numero = int(Numero) #Numero da Pokedex, pode ser usado como chave
        self.Nome = Nome #Nome da espécie do Pokémon
        self.HP_base = int(HP_base) #Número inteiro, status base do Pokémon
        self.Atk_base = int(Atk_base) #Número inteiro, status base do Pokémon
        self.Def_base = int(Def_base) #Número inteiro, status base do Pokémon
        self.Spc_base = int(Spc_base) #Número inteiro, status base do Pokémon
        self.Spd_base = int(Spd_base) #Número inteiro, status base do Pokémon
        self.Tipos = Tipos #Recebe uma Tupla com dois tipos ou com o segundo tipo sendo None.
        self.Taxa_captura = int(Taxa_captura) #Número inteiro usado no cálculo da chance de captura
        self.Exp_type = Exp_type #Nome do tipo de curva de crescimento que a espécie tem
        self.Base_exp_yield = int(Base_exp_yield) #Número inteiro usado no cálculo da experiência passada pela espécie quando derrotada

    def dados(self,Pokedex):
        return (self.Numero,self.Nome,self.HP_base,self.Atk_base,self.Def_base,self.Spc_base,self.Spd_base,self.Tipos,self.Taxa_captura,self.Exp_type,self.Base_exp_yield)
        
        

def Pokemon_individuo (Especie):
    #Inicialização do objeto quando puxa de alguma base de dados salva
    def __init__(self,dados_pokedex,Max_HP,HP_IV,Atk_IV,Def_IV,Spc_IV,Spd_IV,HP_EV,Atk_EV,Def_EV,Spc_EV,Spd_EV,Golpes,HP_Atual,Status_condicao,Exp_atual):
        Especie.__init__(dados_pokedex) #Inicia uma nova instância do objeto Espécie para ter acesso às informações neste objeto indivíduo
        self.Max_HP = int(Max_HP) #HP máximo deste indivíduo
        self.HP_IV = int(HP_IV) #Individual Values deste indivíduo
        self.Atk_IV = int(Atk_IV) #Individual Values deste indivíduo
        self.Def_IV = int(Def_IV) #Individual Values deste indivíduo
        self.Spc_IV = int(Spc_IV) #Individual Values deste indivíduo
        self.Spd_IV = int(Spd_IV) #Individual Values deste indivíduo
        self.HP_EV = int(HP_EV) #Effort Values deste indivíduo
        self.Atk_EV = int(Atk_EV) #Effort Values deste indivíduo
        self.Def_EV = int(Def_EV) #Effort Values deste indivíduo
        self.Spc_EV = int(Spc_EV) #Effort Values deste indivíduo
        self.Spd_EV = int(Spd_EV) #Effort Values deste indivíduo
        self.Golpes = Golpes #Lista com até 4 ataques deste indivíduo
        self.HP_atual = int(HP_Atual) #HP que o Pokémon está
        self.Status_condicao = Status_condicao #Condição que o Pokémon está
        self.Exp_atual = int(Exp_atual) 

    #Inicialização para Pokémon selvagem ou de oponente
    def __init__(dados_pokedex,lvl):
        Especie.__init__(dados_pokedex)
        self.Atk_IV = random.randint(0,15) #Todo Individual Value é gerado automaticamente como um inteiro entre 0 e 15
        self.Def_IV = random.randint(0,15) #Todo Individual Value é gerado automaticamente como um inteiro entre 0 e 15
        self.Spc_IV = random.randint(0,15) #Todo Individual Value é gerado automaticamente como um inteiro entre 0 e 15
        self.Spd_IV = random.randint(0,15) #Todo Individual Value é gerado automaticamente como um inteiro entre 0 e 15
        self.HP_IV = 0
        if (self.Atk_IV % 2 == 1): self.HP_IV += 8
        if (self.Def_IV % 2 == 1): self.HP_IV += 4
        if (self.Spc_IV % 2 == 1): self.HP_IV += 2
        if (self.Spd_IV % 2 == 1): self.HP_IV += 1 #HP não tem IV próprio na primeira geração de Pokémon, usando o bit menos significativo de cada um dos outros IV's
        self.Max_HP = ((((self.BP_base+self.HP_IV)*2 + ( int((self.HP_EV)/4)^(1/2)))*lvl)/100)+lvl+10
        self.HP_EV = 0 #Todo Pokemon selvagem é inicializado com 0 de Effort Values
        self.Atk_EV = 0 #Todo Pokemon selvagem é inicializado com 0 de Effort Values
        self.Def_EV = 0 #Todo Pokemon selvagem é inicializado com 0 de Effort Values
        self.Spc_EV = 0 #Todo Pokemon selvagem é inicializado com 0 de Effort Values
        self.Spd_EV = 0 #Todo Pokemon selvagem é inicializado com 0 de Effort Values
        self.Golpes = 
        self.HP_atual = ((((self.BP_base+self.HP_IV)*2 + ( int((self.HP_EV)/4)^(1/2)))*lvl)/100)+lvl+10
        self.Status_condicao = None
        self.Exp_atual = 
