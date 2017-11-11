from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import *
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
                    self.ritorno = 'NO'
                    self.esci = True
                    break
        if not self.esci:
            self.ritorno = 'SI'

class Subnetting:
    esci = False
    dizio   = {'ip' : [], 'subnetmask' : []}
    address = {'ip' : '', 'subnetmask' : ''}
    binario = {'ip' : '', 'subnetmask' : ''}
    ritorno = ''
    n_host_max = 0
    n_sub_max  = 0

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
        self.trova(indirizzo,'ip')
        self.trova(subnetmask,'subnetmask')
        if not self.esci:
            #whichclass identifica la classe di appartenenza dell'indirizzo ip
            whichclass = IdentificaClassi(indirizzo).future
            copia = self.binario['subnetmask']
            #se si tratta di un indirizzo di classe A/B/C allora non da errore
            if whichclass < 4:
                for j in range(whichclass-1):
                    #prende solamente l ottetto/gli ottetti dedicati alla parte host
                    self.binario['subnetmask'] = self.binario['subnetmask'][self.binario['subnetmask'].find('.')+1:]
                #controlla se ci sono uno SOLO nei MSB(sx) e NON negli ottetti dedicati alla parte host
                if '1' in self.binario['subnetmask'][self.binario['subnetmask'].find('0'):]:
                    self.esci = True
            if not self.esci:
                self.binario['subnetmask'] = copia
                self.finale = (self.n_host_max, self.n_sub_max, self.address, self.binario)
            else:
                self.finale = 'ERRORE'
        else:
            self.finale = 'ERRORE'
        if not self.esci:
            print(self.binario['subnetmask'])

class Cidr:
    esci = False
    dizio   = {'ip' : [], 'subnetmask' : []}
    binario = {'ip' : '', 'subnetmask' : ''}
    range_dec = []
    range_bin = []
    range_dec_fin = []
    fratto = 254
    n_bit_1 = 0
    finale = ()

    def trova(self, indirizzo,dove):
        self.dizio[dove] = str(indirizzo).split('.')
        if len(self.dizio[dove]) == 4:
            try:
                self.dizio[dove] = list(map(int, self.dizio[dove]))
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
        self.trova(indirizzo,'ip')
        whichclass = IdentificaClassi(indirizzo).future
        n_indirizzi = round(n_host/self.fratto)
        #non serve supernet

        if not self.esci:
            if n_host <= 254:
                whichclass = 6#valore impossibile
                self.finale = indirizzo
            #situazione di errore classe c
            elif whichclass==3 & n_host >= 65535:
                whichclass = 7
                self.finale = ('ERRORE')
                self.esci = True
            #se si tratta di un indirizzo di classe c
            elif (not self.esci) & (whichclass==3):
                #crea range ip
                strano = False
                insert = False
                cont1 = 0
                dove = 2
                listacopia = self.dizio['ip'][2]
                for i in range(n_indirizzi):
                    if (self.dizio['ip'][2] == 255) & (self.dizio['ip'][1] < 255):
                        if (not insert):
                            self.range_dec.append(str(self.dizio['ip'][0])+'.'+str(self.dizio['ip'][1])+'.'+str(self.dizio['ip'][2])+'.'+str(self.dizio['ip'][3]))
                            insert = True
                        self.range_dec.append(str(self.dizio['ip'][0])+'.'+str(self.dizio['ip'][1]+1)+'.'+str(cont1)+'.'+str(self.dizio['ip'][3]))
                        cont1 += 1
                        dove = 1
                        self.dizio['ip'][2] = 0
                        self.dizio['ip'][1] += 1

                        self.range_dec.append(str(self.dizio['ip'][0]+1)+'.'+'0'+'.'+str(cont1)+'.'+str(self.dizio['ip'][3]))
                        cont1 += 1
                        dove = 0
                    elif (self.dizio['ip'][2] == 255) & (self.dizio['ip'][1] == 255) & (self.dizio['ip'][0] == 255):
                        self.range_dec.append('è stato possibile creare solo {0} indirizzi'.format(i+1))
                        strano = True
                        break
                    else:
                        self.range_dec.append(str(self.dizio['ip'][0])+'.'+str(self.dizio['ip'][1])+'.'+str(self.dizio['ip'][2]+i)+'.'+str(self.dizio['ip'][3]))
                        self.dizio['ip'][2] += 1
                self.dizio['ip'][2] = listacopia
                print(self.range_dec)
                if not strano:
                    for i in range(len(self.range_dec)):
                        lista = []
                        stringa = ''
                        lista = str(self.range_dec[i]).split('.')
                        for j in range(dove,3):
                            stringa += str(bin(int(lista[j]))[2:].rjust(8,'0'))
                        self.range_bin.append(stringa)
                print(self.range_bin)
                #trova le parti invariate in range
                mask_result = ''
                #itera primo-ultimo elemento di self.range_bin e fa un and bitwise
                for i in range(8):
                    pass
                    #if self.range_bin[0] == self.range_bin[len(self.range_bin)-1] & cont1 == 0:
                    #    mask_result += '1'
                    #else:
                    #    mask_result += '0'
                n_bit_1 = len(mask_result[:mask_result.find('0')])
                #crea la subnetmask
                for i in range(whichclass-1):
                    self.binario['subnetmask'] += '11111111.'
                self.binario['subnetmask'] += '1'*n_bit_1+'0'*(8-n_bit_1)+'.'
                for i in range(whichclass,4):
                    self.binario['subnetmask'] += '00000000.'
                copia = ''
                copia = self.binario['subnetmask'] = self.binario['subnetmask'][:35]
            if (not self.esci) & (whichclass != (6,7)):
                    #restituisce ip, subnetmask, iprange, binari
                    self.finale = (self.range_dec_fin,self.dizio['subnetmask'])



class Home(TemplateView):
    template_name = "homepage/home.html"
    def get(self,request):
        classi = ClassiForm()
        subnet = SubnetForm()
        bitwise = MessaInAnd()
        cidr = CidrForm()
        return render(request, self.template_name, { 'classi' : classi, 'subnet':subnet, 'bitwise':bitwise, 'cidr': cidr })
    def post(self, request):
        classi = ClassiForm(request.POST)
        subnet = SubnetForm(request.POST)
        bitwise = MessaInAnd(request.POST)
        cidr = CidrForm(request.POST)
        primo = secondo = terzo = quarto = ''
        if classi.is_valid() & ('classe-btn' in request.POST):
            primo = IdentificaClassi(classi.cleaned_data['ip']).finale[0]
        elif subnet.is_valid() & ('subn-btn' in request.POST):
            secondo = Subnetting(subnet.cleaned_data['ip'],subnet.cleaned_data['subnetmask']).finale
        elif bitwise.is_valid() & ('bitwise-btn' in request.POST):
            terzo = Bitwise(subnet.cleaned_data['ip1'],subnet.cleaned_data['ip2'],subnet.cleaned_data['subnetmask']).ritorno
        elif cidr.is_valid() & ('cidr-btn' in request.POST):
            quarto = Cidr(cidr.cleaned_data['ip'],cidr.cleaned_data['n_host']).finale

        classi = ClassiForm()
        subnet = SubnetForm()
        bitwise = MessaInAnd()
        cidr = CidrForm()
        args= {'classi' : classi, 'subnet':subnet, 'bitwise':bitwise, 'cidr': cidr, 'primo':primo,'secondo':secondo,'terzo':terzo,'quarto':quarto}
        return render(request, self.template_name, args)
