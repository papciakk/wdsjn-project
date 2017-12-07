# -*- coding: utf-8 -*-

# Python CLP Wrapper
# (c) Krzysztof Dorosz
# 2008-2013 AGH, dorosz@agh.edu.pl

from ctypes import c_int, CDLL, c_char_p, create_string_buffer, byref

__VERSION__ = 'PLP 3.5'

Array50 = c_int * 50 # Typ pomocniczy dla buforow (tablic) int

class PLP(object):
    class CZESCI_MOWY:
        RZECZOWNIK =    'A'
        CZASOWNIK =     'B'
        PRZYMIOTNIK =   'C'
        LICZEBNIK =     'D'
        ZAIMEK =        'E'
        PRZYSLOWEK =    'F'
        NIEODMIENNY =   'G'
        SEGMENTOWY =    'H'
        SKROT =         'I'

    OGONKOWE = {
        'a':  ['ą'],
        'c':  ['ć'],
        'e' : ['ę'],
        'l' : ['ł'],
        'n' : ['ń'],
        'o' : ['ó'],
        's' : ['ś'],
        'z' : ['ż', 'ź'],
    }

    def __init__(self, clp_lib_path='/usr/local/clp/lib/libclp_2.6.so'):
        self.clp_lib_path = clp_lib_path
        self.CLPLIB = CDLL(self.clp_lib_path)
        self.CLPLIB.clp_ver.restype = c_char_p
        self._init()

    def _init(self):
        """Inicjalizuje bibiloteke CLP"""
        self.CLPLIB.clp_init(1)

    def ver(self):
        """Zwraca napis z numerem wersji CLP"""
        ver = create_string_buffer(80)
        self.CLPLIB.clp_ver(ver)
        return ver.value.decode('utf-8')

    def stat(self, pos):
        """Zwraca statystyke czesci mowy w bibliotece CLP"""
        return self.CLPLIB.clp_stat(c_int(pos))

    def ogonkify(self, word, pos=0):
        """Zwraca liste ogonkowych mozliwosci danego slowa. Slowo musi byc zapisane malymi literami"""
        lista = []
        if len(word) > 20:
            return []
        for i in range(pos, len(word)):
            if word[i] in self.OGONKOWE:
                for ogonek in self.OGONKOWE[word[i]]:
                    next_word = word[0:i] + ogonek + word[i+1:]
                    lista += [next_word] + self.ogonkify(next_word, i)
        return lista

    def orec(self, word):
        """Ogonkowy rec()"""
        if len(word) > 80:
            return []
        ids = self.rec(word)
        for word in self.ogonkify(word.lower()):
            ids += self.rec(word)
        return list(set(ids))


    def rec(self, word):
        """Zwraca liste numerow ID dla danego slowa"""
        if len(word) > 80:
            return []
        ids = Array50()
        num = c_int(0)
        self.CLPLIB.clp_rec(word.encode('utf-8'), ids, byref(num))
        return ids[0:num.value]

    def label(self, id):
        """Zwraca etykiete dla danego ID"""
        label = create_string_buffer(10)
        self.CLPLIB.clp_label(c_int(id), label)
        return label.value.decode('utf-8')

    def bform(self, id):
        """Zwraca forme bazowa dla danego ID"""
        bform = create_string_buffer(80)
        self.CLPLIB.clp_bform(c_int(id), bform)
        return bform.value.decode('utf-8')

    def forms(self, id):
        """Zwraca liste form dla danego wyrazu"""
        formy = create_string_buffer(2048)
        self.CLPLIB.clp_forms(c_int(id), formy)
        return [x.decode('utf-8') for x in formy.value.split(':')[0:-1]]

    def formv(self, id):
        """Zwraca liste form dla danego wyrazu"""
        formy = create_string_buffer(2048)
        self.CLPLIB.clp_formv(c_int(id), formy)
        return [x.decode('utf-8') for x in formy.value.split(':')[0:-1]]

    def vec(self, id, word):
        """Zwraca wector odmiany"""
        out = Array50()
        num = c_int(0)
        self.CLPLIB.clp_vec(c_int(id), word.encode('utf-8'), out, byref(num))
        return out[0:num.value]

    def ldec(self, etykieta):
        opis = create_string_buffer(2048)
        self.CLPLIB.clp_ldec(str(etykieta), opis)
        return [x.decode('utf-8') for x in opis.value.split(':')[0:-1]]

    def lrec(self, word, label):
        id = self.rec(word)
        id = [(x, self.label(x)) for x in id]
        id = [i_l for i_l in id if i_l[1] == label]
        try:
            return id[0][0]
        except IndexError:
            return None

    def fvec(self, id):
        vec = {}
        formy = self.forms(id)
        for f in formy:
            for n in self.vec(id, f):
                vec[n] = f
        return vec
