from flask import Flask, render_template
import random
app = Flask(__name__)

class Bossbattle():
    max_player_hp = 100
    max_boss_hp = 150

    def __init__(self):
        self.boss_hp = self.max_boss_hp
        self.player_hp = self.max_player_hp
        self.battle_state = 'Battling'

    def player_attack(self):
        if self.battle_state != 'Battling':
            return

        if self.boss_hp < 20:
            self.boss_hp = 0
            self.battle_state = 'Victory'
        else:
            self.boss_hp -= 20
            self.boss_attack()
        


    def player_heal(self):
        if self.battle_state != 'Battling':
                return

        if self.player_hp < self.max_player_hp - 25:
            self.player_hp = self.max_player_hp
        else:
            self.player_hp += 25
            
        self.boss_attack()

    def boss_attack(self):
        attack_dmg = random.randint(0,30)
        if self.player_hp > attack_dmg:
            self.player_hp -= attack_dmg
        else:
            self.player_hp = 0
            self.battle_state = 'Defeat'

    def reset_boss(self):
        self.boss_hp = self.max_boss_hp
        self.player_hp = self.max_player_hp
        self.battle_state = 'Battling'


boss_battle = Bossbattle()

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', person=name)

@app.get('/boss/')
def start_boss():
    boss_battle.reset_boss()
    return render_template('boss.html',boss_hp=boss_battle.boss_hp, max_boss_hp=boss_battle.max_boss_hp, player_hp=boss_battle.player_hp, max_player_hp=boss_battle.max_player_hp, battle_state=boss_battle.battle_state)

@app.post("/boss/attack")
def attack():
    boss_battle.player_attack()
    return render_template('boss.html',boss_hp=boss_battle.boss_hp, max_boss_hp=boss_battle.max_boss_hp, player_hp=boss_battle.player_hp, max_player_hp=boss_battle.max_player_hp, battle_state=boss_battle.battle_state)

@app.post("/boss/heal")
def heal():
    boss_battle.player_heal()
    return render_template('boss.html',boss_hp=boss_battle.boss_hp, max_boss_hp=boss_battle.max_boss_hp, player_hp=boss_battle.player_hp, max_player_hp=boss_battle.max_player_hp, battle_state=boss_battle.battle_state)