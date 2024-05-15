
# 
# classe responsável por encapsular os atributos e métodos comum a todos os herois
# 
class BaseHero():
    def __init__(self, name, max_health, base_damage, move_speed, jump_heigth):
        self.name = name
        self.max_health = max_health
        self.current_health = self.max_health
        self.base_damage = base_damage
        self.move_speed = move_speed
        self.jump_heigth = jump_heigth
    
    # retorna o hitbox do personagem
    def get_rect():
        pass
    
    # engatilha o ataque básico do personagem
    def attack():
        pass

    # movimentação do personagem
    def move():
        pass
    
    # animação quando o personagem está parado
    def idle():
        pass
    
    # engatilha o salto do personagem
    def jump():
        pass

    # animação de receber dano
    def hurt():
        pass
    
    # morte do personagem
    def die():
        pass

    # atualiza os atributos do personagem a cada frame
    def update():
        pass

    # desenha o heroi na tela com base nos seus atributos atuais
    def draw():
        pass
    
    # desenha a barra de vida por personagem
    def draw_health_bar():
        pass
    
    # ação quando o personagem toma dano
    def take_damage():
        pass


# 
# classe herda de BaseHero e encapsula atributos e métodos apenas de herois corpo-à-corpo
# 
class BaseHeroMelee(BaseHero):
    def __init__(self):
        super().__init__(self)
    
    # adiciona um inimigo que estiver dentro do seu alcance de ataque melee
    def add_enemy():
        pass
    
    # remove um inimigo que sai do seu range de ataque melee
    def remove_enemy():
        pass
    
    # obtem a hitbox de ataque do heroi
    def get_attack_hitbox():
        pass
    
    # causa dano aos inimigos
    def do_damage():
        pass

    
# 
# classe herda de BaseHero e encapsula atributos e métodos apenas de herois à distancia
# 
class BaseHeroRanged(BaseHero):
    def __init__(self):
        super().__init__(self)
    
    