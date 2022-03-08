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
            if type(row[1]) == list:
                for transaction in row[1]:    # MIVEL A DATA LISTA, EZÉRT KELL FOR CIKLUSSAL VÉGIG MENNI RAJTA
                    text += transaction.sender + '-' + transaction.receiver + '-' + str(transaction.amount) + ' '
                    text += '\n'
            else:
                text += str(row[0]) + ' : ' + str(row[1]) + '\n'
        return text


    # 64 HOSSZÚSÁGÚ STRING ELŐÁLLÍTÁSA
    def make_hash(self):
        return sha256( (''.join(str(transaction) for transaction in self.data) + str(self.time) + str(self.pre_hash) + str(self.nonce)).encode() ).hexdigest()



    # MEGFELELŐ HASH ELŐÁLLÍTÁSA
    def mine(self, difficulty):
        print('Start mining:')
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
        self.reward = 25    # jutalom
        self.transaction_list = []    # ebben gyűjtöm a tranzakciókat, amíg nem kész a blokk


    def __str__(self):
        text = ''
        for block in self.chain:
            text += str(block) + '\n'
        return text
    

    def genesis_block(self):
        return Block([Transaction('GA', 'GA', 0)])


    # ÚJ TRANZAKCIÓK
    def new_transaction(self, transaction):
        self.transaction_list.append(transaction)


    # AKI ELŐSZÖR MEGTALÁLJA A MEGFELELŐ HASH-T, AZ KAPJA MEG A REWARD-OT ÉRTE
    # LÉTREJÖN A BLOKK
    # KIBÁNYÁSSZUK
    # HOZZÁADJUK A LÉTREHOZOTT BLOKKLÁNCHOZ
    # A TRANZAKCIÓ A TRANZAKCIÓS LISTA RÉSZE LETT
    def mine_transaction(self, miner):
        block = Block(self.transaction_list, pre_hash=self.chain[-1].hash)
        block.mine(self.difficulty)
        self.chain.append(block)
        self.transaction_list = [Transaction('Ga', miner, self.reward)]


    # A JELENLEGI HASHÜNK MEGEGYEZIK E A KÖVETKEZŐ BLOKK PRE-HASH-ÉVEL
    def is_valid(self):
        for i in range(len(self.chain)-1):
            if self.chain[i].hash != self.chain[i+1].pre_hash:
                return 'Previous hash conflict detected in ' + str(i+1) + '. block!'
            if self.chain[i].hash != self.chain[i].make_hash():
                return 'Own has conflict detected in ' + str(i+1) + '. block!'
        return 'OK'


    # KINEK MENNYI PÉNZE VAN
    def get_balance(self, person):
        balance = 0
        for block in self.chain:
            for transaction in block.data:
                if transaction.receiver == person:
                    balance += transaction.amount
                if transaction.sender == person:
                    balance -= transaction.amount
        return balance


# TRANZAKCIÓ, BENNE VAN A KÜLDŐ-FOGADÓ-EGYSÉG
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __str__(self):
        text = ''
        for row in self.__dict__.items():
            text += str(row[0]) + ': ' + str(row[1]) + '\n'
        return text


# OGJEKTUM PÉLDÁNY ÉS BLOCKCHAIN NEVŰ OSZTÁLYA
coin = Blockchain()


print('>>> GENESIS BLOCK >>>')
print(coin)

# BLOKKOK, TRANZAKCIÓK
coin.new_transaction(Transaction('Luke', 'Han', 50))
coin.new_transaction(Transaction('Obi-Wan', 'Han', 150))
coin.new_transaction(Transaction('Han', 'Yoda', 200))


print('>>> TRANSACTIONS >>>')
for item in coin.transaction_list:
    print(item)

print('>>> MINING >>>')
coin.mine_transaction('Yoda')

print('>>> BLOCKS >>>')
print(coin)

print('>>> TRANSACTIONS >>>')
for item in coin.transaction_list:
    print(item)

print('>>> BALANCE >>>')
print('Luke: ', coin.get_balance('Luke'))
print('Han: ', coin.get_balance('Han'))
print('Obi-Wan: ', coin.get_balance('Obi-Wan'))
print('Yoda: ', coin.get_balance('Yoda'))

print('>>> MINING >>>')
coin.mine_transaction('Yoda')

print('>>> BLOCKS >>>')
print(coin)
print('Yoda: ', coin.get_balance('Yoda'))


print('Is valid?', coin.is_valid())

coin.chain[1].data[0].amount = 100
print('Is valid?', coin.is_valid())

coin.chain[1].hash = coin.chain[1].make_hash()
print('Is valid?', coin.is_valid())
