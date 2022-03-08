from hashlib import sha256
from datetime import datetime


# BLOCK LÉTREHOZÁSA
class Block:


    # KONSTRUKTOR FÜGGVÉNY
    def __init__(self, data, time=datetime.today(), pre_hash='0'*64):
        self.data = data
        self.time = time
        self.pre_hash = pre_hash
        self.nonce = 0
        self.hash = self.make_hash()
    

    # SAJÁT OBJEKTUM ADATTAGJAIN VALÓ VÉGIG LÉPKEDÉS, MAJD
    # ITEMS SEGÍTSÉGÉVEL TUPLE-É VALÓ ÁTALAKÍTÁS
    # str(row[0]) -> SELF.DATA   str(row[1]) -> DATA
    def __str__(self):
        text = ''
        for row in self.__dict__.items():
            text += str(row[0]) + ' : ' + str(row[1]) + '\n'
        return text


    # 64 HOSSZÚSÁGÚ STRING ELŐÁLLÍTÁSA
    def make_hash(self):
        return sha256( (str(self.data) + str(self.time) + str(self.pre_hash) + str(self.nonce)).encode() ).hexdigest()


    # MEGFELELŐ HASH ELŐÁLLÍTÁSA
    def mine(self, difficulty):
        print('Start mining:', self.data)
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1    # AZÉRT, HOGY ÚJ HASH-T TUDJUNK GENERÁLNI
            self.hash = self.make_hash()
        print('Experiment:', self.nonce)
        print('Mined:', self.hash, '\n')


# BLOCKCHAIN OSZTÁLY AMI BLOKKOKAT TARTALMAZ
class Blockchain:


    def __init__(self):
        self.chain = [self.genesis_block()]
        self.difficulty = 4


    def __str__(self):
        text = ''
        for block in self.chain:
            text += '\n' + str(block)
        return text
    

    def genesis_block(self):
        return Block('Genesis block')


    # LÉTREHOZ EGY ÚJ BLOKKOT ÉS BEILLESZTI A SORBA
    def new_block(self, block):
        block.pre_hash = self.chain[-1].hash    # AZ ELŐZŐ BLOKK HASH-ÉT BELEÍRJA A JELENLEGI BLOKK PRE-HASH-ÉBE
        block.mine(self.difficulty)    # MILYEN NEHÉZSÉGGEL BÁNYÁSSZON
        self.chain.append(block)


    # A JELENLEGI HASHÜNK MEGEGYEZIK E A KÖVETKEZŐ BLOKK PRE-HASH-ÉVEL
    def is_valid(self):
        for i in range(len(self.chain)-1):
            if self.chain[i].hash != self.chain[i+1].pre_hash:
                return 'Previous hash conflict detected in ' + str(i+1) + '. block!'
            if self.chain[i].hash != self.chain[i].make_hash():
                return 'Own has conflict detected in ' + str(i+1) + '. block!'
        return 'OK'


# OGJEKTUM PÉLDÁNY ÉS BLOCKCHAIN NEVŰ OSZTÁLYA
coin = Blockchain()


# BLOKKOK, TRANZAKCIÓK
coin.new_block(Block({'from' : 'Luke', 'to' : 'Han', 'coin' : 50}))
coin.new_block(Block({'from' : 'Obi-Wan', 'to' : 'Han', 'coin' : 150}))
coin.new_block(Block({'from' : 'Han', 'to' : 'Yoda', 'coin' : 200}))


print(coin)
print('Is valid?', coin.is_valid())


# EGY ÉRTÉK MEGVÁLTOZTATÁSA 150->350
coin.chain[2].data['coin'] = 350
print('Is valid?', coin.is_valid())


# SAJÁT HASH KISZÁMÍTÁSA
coin.chain[2].hash = coin.chain[2].make_hash()
print('Is valid?', coin.is_valid())