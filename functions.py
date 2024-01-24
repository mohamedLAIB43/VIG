import sys
import pandas as pd

def Vchiffrer(m, k, dic, v):
    k = sup_espace(k)
    d = sup_espace(m)
    c = ''
    s = len(k)
    try:
        for i in range(len(d)):
            a = (dic[d[i]] + dic[k[i % s]]) % 26
            c = c + v[a]
            if ((i + 1) % 5 == 0):
                c = c + ' '
        return c
    except Exception as e:
        return 'There is an error: ' + str(e)

def Vdechiffrer(c, k, dic, v):
    k = sup_espace(k)
    m = ''
    d = sup_espace(c)
    s = len(k)
    for i in range(len(d)):
        a = (dic[d[i]] - dic[k[i % s]])
        if (a < 0):
            a = a + 26
        m = m + v[a]
        if ((i + 1) % 4 == 0):
            m = m + ' '
    return m

def cle_coincidence(c, dic, v, lb, ub):
    T = []
    d = sup_espace(c)
    IC, tab = Cle_size(c, dic, lb, ub)

    for i in tab:
        key = ''
        for j in range(i):
            N = 26 * [0]
            for k in range(j, len(d), i):
                N[dic[d[k]]] += 1
            key = key + v[(N.index(max(N)) - 4) % 26]
        T.append(key)
    return T, tab, IC

def cle_repetition(c, dic, v):
    T = []
    d = ''
    s, compt = Compteur(c)
    for i in c:
        if (i != ' '):
            d = d + i
    for i in s:
        key = ''
        for j in range(i):
            N = 26 * [0]
            for k in range(j, len(d), i):
                N[dic[d[k]]] += 1
            key = key + v[(N.index(max(N)) - 4) % 26]
        T.append(key)
    return T, s

def sup_espace(m):
    d = ''
    CH = ',;:!?/.+-*)]\\_`)([}{#~\'<>/’,»1234567890|@=¨' + '"' + '╔' + "^"

    for i in m:
        if i not in CH and i != ' ' and i != '\n':
            d = d + i

    return d

def que_des_majuscules(m):
    """
    Fonction qui permet de supprimer tous les caractères inutiles d'une chaine.
    """
    CH = ',;:!?/.+-*)]\\_`)([}{#~\'<>/’,»1234567890|@=¨' + '"' + '╔' + "^"
    d = ''
    for i in m:
        if i not in CH and i != ' ' and i != '\n':
            d = d + i
    return d

def ic(texte):
    chaine = que_des_majuscules(texte)
    frequences = [0] * 26
    n = len(chaine)
    for c in chaine:
        frequences[ord(c) - 65] += 1
    indice = 0.0
    for ni in frequences:
        indice += ni * (ni - 1)
    return indice / (n * (n - 1)) if n > 1 else 0

def ic_par_intervalle(texte, intervalle):
    chaine = que_des_majuscules(texte)
    total_ic = 0.0
    for start in range(intervalle):
        sous_chaine = chaine[start::intervalle]
        total_ic += ic(sous_chaine)
    return total_ic / intervalle if intervalle > 0 else 0

def trouver_intervalle_anormal(texte, seuil_ic=0.074, max_intervalle=100):
    for intervalle in range(1, max_intervalle + 1):
        ic_actuel = ic_par_intervalle(texte, intervalle)
        if ic_actuel > seuil_ic:
            return intervalle
    return None

def trouver_cle_ic(texte, intervalle):
    chaine = sup_espace(texte)
    cle = ''
    for start in range(intervalle):
        sous_chaine = chaine[start::intervalle]
        cle += trouver_lettre_cle_ic(sous_chaine)
    return cle
def extraire_messages(self, texte, intervalle):
        messages_extraits = []
        for i in range(intervalle):
            sous_chaine = texte[i::intervalle]
            messages_extraits.append(sous_chaine)
        return messages_extraits

def calculer_cle_indice_coincidence(self, messages_extraits):
        longueur_cle = len(messages_extraits[0])
        cle = ""

        for i in range(longueur_cle):
            sous_chaine = [message[i] for message in messages_extraits]

            frequences = {lettre: sous_chaine.count(lettre) for lettre in set(sous_chaine)}

            lettre_cle = max(frequences, key=frequences.get)

            cle += lettre_cle

        return cle

def trouver_lettre_cle_ic(chaine):
    frequences = [0] * 26
    n = len(chaine)
    for c in chaine:
        frequences[ord(c) - 65] += 1
    lettre_cle = chr((frequences.index(max(frequences)) + 4) % 26 + 65)
    return lettre_cle

def Indice_Coincidance(c, dic):
    d = sup_espace(c)
    N = 26 * [0]
    for i in d:
        N[dic[i]] += 1
    ic = 0
    for i in N:
        ic = ic + i * (i - 1)
    ic = ic / (len(d) * (len(d) - 1))

    return ic

def permutation(a, b):
    c = a
    a = b
    b = c
    return a, b

def tri(IC, tab):
    icf = 0.074
    for i in range(len(IC) - 1):
        for j in range(i + 1, len(IC)):
            if (abs(IC[i] - icf) > abs(IC[j] - icf)):
                IC[i], IC[j] = permutation(IC[i], IC[j])
                tab[i], tab[j] = permutation(tab[i], tab[j])
    return IC, tab

def Cle_size(c, dic, lb, ub):
    tab = []
    IC = []
    d = ''
    for i in c:
        if (i != ' '):
            d = d + i
    for j in range(len(d) - 1):
        c_dec = ''
        for i in range(0, len(d), j + 1):
            c_dec = c_dec + d[i]
        ic = Indice_Coincidance(c_dec, dic)

        if (ic >= lb and ic <= ub):
            IC.append(round(ic, 4))
            tab.append(j + 1)
    IC, tab = tri(IC, tab)
    return IC, tab

def MinMax(facteur):
    a = 1000
    b = 0
    for i in range(len(facteur)):
        if (a > min(facteur[i])):
            a = min(facteur[i])

        if (b < max(facteur[i])):
            b = max(facteur[i])
    return a, b

def repetition(c):
    c = sup_espace(c)
    chaine = []
    rep = []
    pos = []
    for i in range(3, 10):
        for j in range(len(c) - i):
            r = c[j:i + j]
            for k in range(j + i, len(c) - i):
                if (r == c[k:k + i]):
                    chaine.append(r)
                    rep.append(k - j)
                    pos.append(k)
    return chaine, rep, pos

def decomposition(c):
    chaine, rep, pos = repetition(c)
    facteur = []
    for n in (rep):
        fact = []
        d = 2
        while n > 1:
            while n % d == 0:
                if (d not in fact):
                    fact.append(d)
                n = n // d
            d = d + 1
        facteur.append(fact)
    return facteur

def FactCom(c):
    facteur = decomposition(c)
    a, b = MinMax(facteur)
    v = []
    for i in range(a, b):
        for j in range(len(facteur)):
            if (i in facteur[j]):
                if (i not in v):
                    v.append(i)
    return v

def Tri(IC, tab):
    icf = 0.074
    for i in range(len(IC) - 1):
        for j in range(i + 1, len(IC)):
            if (abs(IC[i] - icf) > abs(IC[j] - icf)):
                IC[i], IC[j] = permutation(IC[i], IC[j])
                tab[i], tab[j] = permutation(tab[i], tab[j])
    return IC, tab

def permutation(a, b):
    c = a
    a = b
    b = c
    return a, b

def Tri(s, compt):
    for i in range(len(s) - 1):
        for j in range(i + 1, len(s)):
            if (compt[i] < compt[j]):
                compt[i], compt[j] = permutation(compt[i], compt[j])
                s[i], s[j] = permutation(s[i], s[j])
    return s, compt

def Compteur(c):
    facteur = decomposition(c)
    s = FactCom(c)
    compt = []
    for i in s:
        cpt = 0
        for j in range(len(facteur)):
            if (i in facteur[j]):
                cpt = cpt + 1
        compt.append(cpt)
    Tri(s, compt)
    try:
        a = [s[0], 2 * s[0], 3 * s[0], 4 * s[0], 5 * s[0], 6 * s[0], 7 * s[0], 8 * s[0], 9 * s[0], 10 * s[0], 11 * s[0],
             12 * s[0]]
        b = compt[0]
    except:
        a = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
        b = 39
    return a, b
