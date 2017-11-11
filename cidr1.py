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
    def pulisci(self):
        self.esci = False
        self.dizio   = {'ip1':[],'ip2':[],'subnetmask':[]}
        self.address = {'ip1':[],'ip2':[],'subnetmask':[]}
        self.binario = {'ip1':[],'ip2':[],'subnetmask':[]}
        self.ritorno = ''
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
        self.pulisci()
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
                    self.ritorno = 'NO'
                    self.esci = True
                    break
        if not self.esci:
            self.ritorno = 'SI'
        else:
            self.ritorno = 'ERRORE'

class Subnetting:
    esci = False
    dizio   = {'ip' : [], 'subnetmask' : []}
    address = {'ip' : '', 'subnetmask' : ''}
    binario = {'ip' : '', 'subnetmask' : ''}
    ritorno = ''
    n_host_max = 0
    n_sub_max  = 0
    def pulisci(self):
        self.esci = False
        self.dizio   = {'ip' : [], 'subnetmask' : []}
        self.address = {'ip' : '', 'subnetmask' : ''}
        self.binario = {'ip' : '', 'subnetmask' : ''}
        self.ritorno = ''
        self.n_host_max = 0
        self.n_sub_max  = 0
    def trova(self, indirizzo,dove):
        self.dizio[dove] = str(indirizzo).split('.')
        if len(self.dizio[dove]) == 4:
            try:
                self.dizio[dove] = list(map(int, self.dizio[dove]))
                self.address[dove] = str(indirizzo)
                self.binario[dove] = '.'.join(map(lambda x: str(bin(x))[2:].rjust(8,'0'), self.dizio[dove]))
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
        self.pulisci()
        self.trova(indirizzo,'ip')
        self.trova(subnetmask,'subnetmask')
        if not self.esci:
            #whichclass identifica la classe di appartenenza dell'indirizzo ip
            whichclass = IdentificaClassi(indirizzo).future
            copia = self.binario['subnetmask']
            #se si tratta di un indirizzo di classe A/B/C allora non da errore
            if whichclass < 4:
                #controlla se ci sono uno SOLO nei MSB(sx) e NON negli ottetti dedicati alla parte host
                for i in range(self.binario['subnetmask'].count('.')):
                    self.binario['subnetmask'] = self.binario['subnetmask'][:self.binario['subnetmask'].find('.')]+self.binario['subnetmask'][self.binario['subnetmask'].find('.')+1:]
                for j in range(whichclass):
                        #prende solamente l ottetto/gli ottetti dedicati alla parte host
                        self.binario['subnetmask'] = self.binario['subnetmask'][8:]
                if '1' in self.binario['subnetmask'][self.binario['subnetmask'].find('0'):]:
                    self.esci = True
                if not self.esci:
                    meno = {1:24,2:16,3:8}
                    n_bit_1 = len(self.binario['subnetmask'][:self.binario['subnetmask'].find('0')])
                    self.n_sub_max = 2**n_bit_1
                    self.n_host_max = 2**meno[whichclass]-n_bit_1
                    self.finale = (self.n_host_max, self.n_sub_max)
            else:
                self.esci = True
        if self.esci:
            self.finale = 'ERRORE'

class Cidr:
    esci = False
    dizio   = {'ip' : [], 'subnetmask' : []}
    address = {'ip' : '', 'subnetmask' : ''}
    binario = {'ip' : '', 'subnetmask' : ''}
    range_dec = []
    range_bin = []
    range_dec_fin = []
    range_bin_fin = []
    ritorno = ''
    fratto = {2:65534, 3:254}
    n_bit_1 = 0
    finale = ()

    def pulisci(self):
        self.esci = False
        self.dizio   = {'ip' : [], 'subnetmask' : []}
        self.address = {'ip' : '', 'subnetmask' : ''}
        self.binario = {'ip' : '', 'subnetmask' : ''}
        self.range_dec = []
        self.range_bin = []
        self.range_dec_fin = []
        self.range_bin_fin = []
        self.ritorno = ''
        self.fratto = {2:65534, 3:254}
        self.n_bit_1 = 0
        self.finale = ()
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

    def __init__(self,indirizzo,n_host):
        self.pulisci()
        self.trova(indirizzo,'ip')
        whichclass = IdentificaClassi(indirizzo).future
        #non serve supernet
        if n_host <= 254:
            whichclass = 6#valore impossibile
            self.range_dec_fin.append(indirizzo)
            self.range_bin_fin.append('.'.join(map(lambda x: str(bin(x))[2:], self.dizio['ip'])))
            self.finale = (self.range_dec_fin,self.range_bin_fin)
        #situazione di errore classe c
        elif whichclass==3 & n_host >= 65535:
            whichclass = 7
            self.finale = ('ERRORE')
            self.esci = True
        #situazione di errore classe b
        elif whichclass==2 & n_host <65535:
            whichclass = 7
            self.finale = ('ERRORE')
            self.esci = True
        #se si tratta di un indirizzo di classe b o c
        elif (not self.esci) & (2<=whichclass<=3):
            for i in range(round(n_host/self.fratto[whichclass])):
                self.range_dec.append(self.dizio['ip'][whichclass-1]+i)
                self.range_bin.append(bin(self.dizio['ip'][whichclass-1]+i))
                #aggiunge bit a 0 di padding
                self.range_bin[i] = self.range_bin[i][2:].rjust(8,'0')
            #trova le parti invariate in range
            mask_result = ''
            #itera primo-ultimo elemento di self.range_bin e fa un and bitwise
            for i in range(8):
                if self.range_bin[0][i] == self.range_bin[len(self.range_bin)-1][i]:
                    mask_result += '1'
                else:
                    mask_result += '0'
            n_bit_1 = len(mask_result[:mask_result.find('0')])
            #crea la subnetmask
            for i in range(whichclass-1):
                self.binario['subnetmask'] += '11111111.'
            self.binario['subnetmask'] += '1'*n_bit_1+'0'*(8-n_bit_1)+'.'
            for i in range(whichclass,4):
                self.binario['subnetmask'] += '00000000.'
            copia = ''
            copia = self.binario['subnetmask'] = self.binario['subnetmask'][:35]
            #inserisce la subnetmask appena creata nella lista dizio, convertendola in intero
            for i in range(4):
                self.dizio['subnetmask'].append(int(self.binario['subnetmask'][:self.binario['subnetmask'].find('.')],2))
                self.binario['subnetmask'] = self.binario['subnetmask'][self.binario['subnetmask'].find('.')+1:]
            self.binario['subnetmask'] = copia
            #crea il range di ip
            for i in range(len(self.range_dec)):
                if whichclass == 3:
                    if self.range_dec[i] <= 255:
                        self.range_dec_fin.append(str(self.dizio['ip'][0])+'.'+str(self.dizio['ip'][1])+'.'+str(self.range_dec[i])+'.'+str(self.dizio['ip'][3]))
                        self.range_bin_fin.append(str(bin(self.dizio['ip'][0])[2:].rjust(8,'0'))+'.'+str(bin(self.dizio['ip'][1])[2:].rjust(8,'0'))+'.'+str(bin(self.range_dec[i])[2:].rjust(8,'0'))+'.'+str(bin(self.dizio['ip'][3])[2:].rjust(8,'0')))
                    else:
                        self.range_dec_fin.append('Puoi avere al massimo {0} indirizzi'.format(i))
                        self.range_bin_fin.append('Puoi avere al massimo {0} indirizzi'.format(i))
                        break
                if whichclass == 2:
                    if self.range_dec[i] <= 255:
                        self.range_dec_fin.append(str(self.dizio['ip'][0])+'.'+str(self.range_dec[i])+'.'+str(self.dizio['ip'][2])+'.'+str(self.dizio['ip'][3]))
                        self.range_bin_fin.append(str(bin(self.dizio['ip'][0])[2:].rjust(8,'0'))+'.'+str(bin(self.range_dec[i])[2:].rjust(8,'0'))+'.'+str(bin(self.dizio['ip'][2])[2:].rjust(8,'0'))+'.'+str(bin(self.dizio['ip'][3])[2:].rjust(8,'0')))
                    else:
                        self.range_dec_fin.append('Puoi avere al massimo {0} indirizzi'.format(i))
                        self.range_bin_fin.append('Puoi avere al massimo {0} indirizzi'.format(i))
                        break
        if (not self.esci) & (whichclass != (6,7)):
                #restituisce ip, subnetmask, iprange, binari
                self.finale = (self.range_dec_fin,self.dizio['subnetmask'])

#--------------------------------MAIN PROGRAM--------------------------------
#IdentificaClassi(ip)------>classe a/b/c/d/e
#print(IdentificaClassi('192.168.10.8').future)
#print('\n')
#Subnetting(ip, subnetmask)---->Controlla se la subnetmask è corretta e da max_host e n_subnet
#print(Subnetting('120.168.10.8','255.255.255.0').finale)
#print('\n')
#Bitwise(ip1,ip2,subnetmask)------>Messa in And Bitwise ip1&subnetmask ip2&subnetmask
    #print(Bitwise('192.168.10.8','192.168.10.2','255.255.255.128').finale)
    #print('\n')
#CIDR(ip/n bit a 1)
#print(Cidr('192.168.1.1',500).finale)
uscita = uno = due = tre = quattro = False
while not uscita:
    while not uno:
        ip = input('Inserisci indirizzo ip(192.168.1.1): ')
        if IdentificaClassi(ip).finale[0] != 'ERRORE':
            print(IdentificaClassi(ip).finale[0],'\n')
            uno=True
    domanda = input('Vuoi fare subnetting o messa in and o supernetting?(1 o 2 o 3): ')
    try:
        if domanda[0] == '1':
            while not due:
                subnetmask = input('Inserisci Subnet mask(255.255.255.0): ')
                if Subnetting(ip,subnetmask).finale != 'ERRORE':
                    print('n host massimi, n subnet massime')
                    print(Subnetting(ip,subnetmask).finale,'\n')
                    due = True
        elif domanda[0] == '2':
            while not tre:
                ip1= input('Inserisci un secondo indirizzo Ip(192.168.1.2): ')
                subnetmask = input('Inserisci Subnet mask(255.255.255.0): ')
                if Bitwise(ip,ip1,subnetmask).ritorno != 'ERRORE':
                       print('La Messa in And è andata a buon fine? ',Bitwise(ip,ip1,subnetmask).ritorno,'\n')
                       if Bitwise(ip,ip1,subnetmask).ritorno == 'NO':
                           if  input('Vuoi rifare(S/N)') == 'N':
                               tre = True
                       else:
                           tre = True
        elif domanda[0] == '3':
            while not quattro:
                try:
                    n_host = int(input('inserisci numero host: (500): '))
                except ValueError:
                    print('inserisci un intero')
                if Cidr(ip,n_host).finale != 'ERRORE':
                    print('(range_ip , subnetmask)')
                    print(Cidr(ip,n_host).finale,'\n')
                    quattro = True
        domanda = input('Vuoi uscire? (S/N): ')
        if domanda[0] == 'S':
                uscita = True
        elif domanda[0] == 'N':
            uno = due = tre = quattro = False
        else:
            print('Rispondi in modo corretto')
    except:
            print('Rispondi in modo corretto')
