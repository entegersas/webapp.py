import re
class IdentificaClassi:
    ritorno = indirizzo = binario  = ''
    ip = []
    esci = False
    future = 4

    def trova(self, indirizzo):
        self.ip = str(indirizzo).split('.')
        if len(self.ip) == 4:
            try:
                #converte in lista di interi da stringa, metodo migliore
                self.ip = list(map(int, self.ip))
                #la stringa viene salvata nell'oggetto
                self.indirizzo = str(indirizzo)
                #concatena lista self.ip in stringa usando la rappresentazione binaria
                self.binario = '.'.join(map(lambda x: str(bin(x))[2:], self.ip))
                #se tutti gli elementi della lista sono minori di 255 l'indirizzo è corretto
                if not all(i <= 255 for i in self.ip):
                    self.esci = True
            #se nel creare la lista self.ip sono contenuti caratteri alfabetici il flag ValueError scatta
            except ValueError:
                self.esci = True
            #gestire le eccezzioni per errori dati dalla concatenazione di stringe
            except IndexError:
                self.esci = True
            except TypeError:
                self.esci = True
        #se è stato inserito un indirizzo che non abbia 4 ottetti avviene un errore
        else:
            self.esci = True

    def __init__(self, indirizzo):
        #determina se l'ip inserito da utente è corretto
        self.trova(indirizzo)
        #se non avvengono errori in self.trova() si puo proseguire
        if not self.esci:
            #riempe con bit di padding gli ottetti in self.binario
            copia = self.binario+'.'
            uno = ''
            for j in range(4):
                self.binario = self.binario[:self.binario.find('.')]
                for i in range(8 - len(self.binario)):
                    self.binario = '0' + self.binario
                uno += '.' + self.binario
                self.binario = copia[copia.find('.')+1:]
                copia = copia[copia.find('.')+1:]
            self.binario = uno[1:]
            #determina la classe dell'indirizzo inserito
            self.classea()
            self.classeb()
            self.classec()
            self.classed()
            self.classee()
            # controlli per vedere se l indirizzo inserito è di default
            if self.ip == [0,0,0,0]:
                self.ritorno = 'Indirizzo IP 0.0.0.0 è l\' indirizzo di Rete di default'
            elif self.ip == [255, 255, 255, 255]:
                self.ritorno = 'Indirizzo IP 255.255.255.255 è l\' indirizzo di Broadcast di default'
            elif self.ip == [127, 0, 0, 1]:
                 self.ritorno = 'Indirizzo IP 127.0.0.1 è l\' indirizzo di Loopback di default'
        #se sono avvenuti errori in self.trova() esce e da come risultato ERRORE
        else:
            self.ritorno = 'ERRORE'
        #tupla finale che contiene (Frase di risposta, Ip base 10, Ip base 2)
        self.finale = (self.ritorno,self.indirizzo,self.binario)

    #Nelle prime tre classi di ip oltre ai controlli di appartenenza alla classe è necessario
    # controllare se l'indirizzo inserito sia privato.
    def classea(self):
        if 0 <= self.ip[0] <= 127:
            if self.ip[1] == 0 and self.ip[2] == 0 and self.ip[3] == 0:
                if self.ip[0] == 10:
                    self.ritorno = 'Indirizzo IP {0} è un indirizzo Privato di Rete della Classe A'.format(self.indirizzo)
                else:
                    self.ritorno = 'Indirizzo IP {0} è un indirizzo di Rete della Classe A'.format(self.indirizzo)
            elif self.ip[1] == 255 and self.ip[2] == 255 and self.ip[3] == 255:
                if self.ip[0] == 10:
                    self.ritorno = 'Indirizzo IP {0} è un indirizzo Privato di Broadcast della Classe A'.format(self.indirizzo)
                else:
                    self.ritorno = 'Indirizzo IP {0} è un indirizzo di Broadcast della Classe A'.format(self.indirizzo)
            elif self.ip[0] == 10:
                self.ritorno = 'Indirizzo IP {0} è un indirizzo Privato della Classe A'.format(self.indirizzo)
            else:
                self.ritorno = 'L\'Indirizzo IP {0} appartiene alla Classe A'.format(self.indirizzo)
        self.future = 1

    def classeb(self):
        if 128 <= self.ip[0] <= 191:
            if self.ip[2] == 0 and self.ip[3] == 0:
                if self.ip[0] == 172 and self.ip[1] == 16:
                    self.ritorno = 'Indirizzo IP {0} è un indirizzo Privato di Rete della Classe B'.format(self.indirizzo)
                else:
                    self.ritorno = 'Indirizzo IP {0} è un indirizzo di Rete della Classe B'.format(self.indirizzo)
            elif self.ip[2] == 255 and self.ip[3] == 255:
                if self.ip[0] == 172 and self.ip[1] == 31:
                    self.ritorno = 'Indirizzo IP {0} è un indirizzo Privato di Broadcast della Classe B'.format(self.indirizzo)
                else:
                    self.ritorno = 'Indirizzo IP {0} è un indirizzo di Broadcast della Classe B'.format(self.indirizzo)
            elif self.ip[0] == 172 and 16 <= self.ip[1] <= 31:
                self.ritorno = 'Indirizzo IP {0} è un indirizzo Privato della Classe B'.format(self.indirizzo)
            else:
                self.ritorno = 'L\'Indirizzo IP {0} appartiene alla Classe B'.format(self.indirizzo)
        self.future = 2

    def classec(self):
        if 192 <= self.ip[0] <= 223:
            if self.ip[3] == 0:
                if self.ip[0] == 192 and self.ip[1] == 168:
                    self.ritorno = 'Indirizzo IP {0} è un indirizzo Privato di Rete della Classe C'.format(self.indirizzo)
                else:
                    self.ritorno = 'Indirizzo IP {0} è un indirizzo di Rete della Classe C'.format(self.indirizzo)
            elif self.ip[3] == 255:
                if self.ip[0] == 192 and self.ip[1] == 168:
                    self.ritorno = 'Indirizzo IP {0} è un indirizzo Privato di Broadcast della Classe C'.format(self.indirizzo)
                else:
                    self.ritorno = 'Indirizzo IP {0} è un indirizzo di Broadcast della Classe C'.format(self.indirizzo)
            elif self.ip[0] == 192 and self.ip[1] == 168:
                self.ritorno = 'Indirizzo IP {0} è un indirizzo Privato della Classe C'.format(self.indirizzo)
            else:
                self.ritorno = 'L\'Indirizzo IP {0} appartiene alla Classe C'.format(self.indirizzo)
        self.future = 3

    def classed(self):
        if 224 <= self.ip[0] <= 239:
            self.ritorno = 'L\'Indirizzo IP {0} appartiene alla Classe D'.format(self.indirizzo)

    def classee(self):
        if 240 <= self.ip[0] <= 255 and 0 <= self.ip[3] <= 254:
            self.ritorno = 'L\'Indirizzo IP {0} appartiene alla Classe E'.format(self.indirizzo)

class Bitwise:
    esci = False
    dizio   = {'ip1':[],'ip2':[],'subnetmask':[]}
    address = {'ip1':[],'ip2':[],'subnetmask':[]}
    binario = {'ip1':[],'ip2':[],'subnetmask':[]}
    ritorno = ''

    def trova(self, indirizzo,dove):
        self.dizio[dove] = str(indirizzo).split('.')
        if len(self.dizio[dove]) == 4:
            try:
                self.dizio[dove] = list(map(int, self.dizio[dove]))
                self.address[dove] = str(indirizzo)
                self.binario[dove] = '.'.join(map(lambda x: str(bin(x))[2:], self.dizio[dove]))
                if not all(i <= 255 for i in self.dizio[dove]):
                    self.esci = True
            except ValueError:
                self.esci = True
            except IndexError:
                self.esci = True
            except TypeError:
                self.esci = True
        else:
            self.esci = True

    def __init__(self,ip1,ip2,subnetmask):
        self.trova(ip1,'ip1')
        self.trova(ip2,'ip2')
        self.trova(subnetmask,'subnetmask')
        if not self.esci:
            for key,value in self.binario.items():
                # bit a 0 riempitivi
                copia = self.binario[key]+'.'
                uno = ''
                for j in range(4):
                    self.binario[key] = self.binario[key][:self.binario[key].find('.')]
                    for i in range(8 - len(self.binario[key])):
                        self.binario[key] = '0' + self.binario[key]
                    uno += '.' + self.binario[key]
                    self.binario[key] = copia[copia.find('.')+1:]
                    copia = copia[copia.find('.')+1:]
                self.binario[key] = uno[1:]
            for i in range(4):
                if (self.dizio['ip1'][i] & self.dizio['subnetmask'][i]) != (self.dizio['ip2'][i] & self.dizio['subnetmask'][i]):
                    self.ritorno = 'ERRORE'
                    self.esci = True
                    break
        if not self.esci:
            self.ritorno = 'Operazione di Messa in And Bitwise effettuata con successo, gli indirizzi IP inseriti appartengono alla stessa sottorete'
        self.finale = (self.ritorno,self.address,self.binario)

class Subnetting:
    esci = False
    dizio   = {'ip' : [], 'subnetmask' : []}
    address = {'ip' : '', 'subnetmask' : ''}
    binario = {'ip' : '', 'subnetmask' : ''}
    ritorno = ''

    def trova(self, indirizzo,dove):
        self.dizio[dove] = str(indirizzo).split('.')
        if len(self.dizio[dove]) == 4:
            try:
                self.dizio[dove] = list(map(int, self.dizio[dove]))
                self.address[dove] = str(indirizzo)
                self.binario[dove] = '.'.join(map(lambda x: str(bin(x))[2:], self.dizio[dove]))
                if not all(i <= 255 for i in self.dizio[dove]):
                    self.esci = True
            except ValueError:
                self.esci = True
            except IndexError:
                self.esci = True
            except TypeError:
                self.esci = True
        else:
            self.esci = True

    def __init__(self,indirizzo, subnetmask):
        self.trova(indirizzo,'ip')
        self.trova(subnetmask,'subnetmask')
        if not self.esci:
            whichclass = IdentificaClassi(indirizzo[:indirizzo.find('/')]).future
            copia = self.binario['subnetmask']
            if whichclass < 4:
                for j in range(whichclass):
                    #prende solamente l ottetto/gli ottetti dedicati alla parte host
                    self.binario['subnetmask'] = self.binario['subnetmask'][self.binario['subnetmask'].find('.')+1:]
                #controlla se ci sono uno solo nei MSB e non negli ottetti dedicati alla parte host
                if '1' in self.binario['subnetmask'][self.binario['subnetmask'].find('0'):]:
                    self.ritorno = 'ERRORE'
                else:
                    self.ritorno = 'Corretto'
            self.binario['subnetmask'] = copia
            self.finale = (self.ritorno, self.address, self.binario)
        else:
            self.finale = 'ERRORE'
class Cidr:
    esci = False
    dizio   = {'ip' : [], 'subnetmask' : []}
    address = {'ip' : '', 'subnetmask' : ''}
    binario = {'ip' : '', 'subnetmask' : ''}
    range_dec = []
    range_bin = []
    range_bin_fin = []
    ritorno = ''
    fratto = {2:65534, 3:254}
    n_bit_1 = 0
    finale = ()

    def trova(self, indirizzo,dove):
        self.dizio[dove] = str(indirizzo).split('.')
        if len(self.dizio[dove]) == 4:
            try:
                self.dizio[dove] = list(map(int, self.dizio[dove]))
                self.address[dove] = str(indirizzo)
                self.binario[dove] = '.'.join(map(lambda x: str(bin(x))[2:], self.dizio[dove]))
                if not all(i <= 255 for i in self.dizio[dove]):
                    self.esci = True
            except ValueError:
                self.esci = True
            except IndexError:
                self.esci = True
            except TypeError:
                self.esci = True
        else:
            self.esci = True

    def __init__(self,indirizzo):
        self.trova(indirizzo[:indirizzo.find('/')],'ip')
        y=int(indirizzo[indirizzo.find('/')+1:])
        whichclass = IdentificaClassi(indirizzo[:indirizzo.find('/')]).future
        if (not self.esci) & (2<=whichclass<=3):
            for i in range(round(int(indirizzo[indirizzo.find('/')+1:])/self.fratto[whichclass])+1):
                self.range_dec.append(self.dizio['ip'][2]+i)
                self.range_bin.append(bin(self.dizio['ip'][2]+i))
                #aggiunge bit a 0 di padding
                self.range_bin[i] = self.range_bin[i][2:].rjust(8,'0')
            for i in range(len(self.range_bin)):
                self.range_bin_fin.append(str(bin(self.dizio['ip'][0])[2:])+'.'+str(bin(self.dizio['ip'][1])[2:])+'.'+str(self.range_bin[i])+'.'+str(bin(self.dizio['ip'][3])[2:]))
            #creare ip range
            print(bin(self.range_bin[0]))
            print(bin(self.range_bin[len(self.range_bin)-1]))
            string = str(bin(self.range_bin[0]) & bin(self.range_bin[len(self.range_bin)-1]))
            #trova le parti invariate in range
            n_bit_1 = len(string[:string.find('0')])
            print(string)
            print(n_bit_1)
            #crea la subnet
            for i in range(whichclass-1):
                self.binario['subnetmask'] += '11111111.'
            self.binario['subnetmask'] += '1'*n_bit_1+'0'*(8-n_bit_1)+'.'
            for i in range(whichclass,4):
                self.binario['subnetmask'] += '11111111.'
            print(self.binario['subnetmask'])
            #self.trova(subnetmask,'subnetmask')
            #restituisce ip, subnetmask, iprange, binari
            self.finale = self.dizio#(self.dizio,self.binario)
#--------------------------------MAIN PROGRAM--------------------------------
#IdentificaClassi(ip)------>classe a/b/c/d/e
print(IdentificaClassi('192.168.10.8').finale)
print('\n')
#Subnetting(ip/n__bit_a_1_subnetmask)---->Controlla se la subnetmask è corretta
print(Subnetting('192.168.10.8','255.255.255.0').finale)
#Bitwise(ip1,ip2,subnetmask)------>Messa in And Bitwise ip1&subnetmask ip2&subnetmask
print(Bitwise('192.168.10.8','192.168.10.2','255.255.255.128').finale)
print('\n')
#CIDR(ip/n bit a 1)
print(Cidr('192.168.1.0/1500').finale)
