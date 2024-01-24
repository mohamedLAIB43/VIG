import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import pandas as pd
from functions import Vchiffrer, Vdechiffrer, Compteur

def sup_espace(m):
    d = ''
    CH = ',;:!?/.+-*)]\\_`)([}{#~\'<>/’,»1234567890|@=¨' + '"' + '╔' + "^"

    for i in m:
        if i not in CH and i != ' ' and i != '\n':
            d = d + i

    return d

def ic(texte):
    chaine = sup_espace(texte)
    frequences = [0] * 26
    n = len(chaine)
    for c in chaine:
        frequences[ord(c) - 65] += 1
    indice = 0.0
    for ni in frequences:
        indice += ni * (ni - 1)
    return indice / (n * (n - 1)) if n > 1 else 0

def ic_par_intervalle(texte, intervalle):
    chaine = sup_espace(texte)
    total_ic = 0.0
    for start in range(intervalle):
        sous_chaine = chaine[start::intervalle]
        total_ic += ic(sous_chaine)
    return total_ic / intervalle if intervalle > 0 else 0

def trouver_intervalle_anormal_ic(texte, seuil_ic=0.074, max_intervalle=100):
    result = ''
    for intervalle in range(1, max_intervalle + 1):
        ic_actuel = ic_par_intervalle(texte, intervalle)
        result += f"Intervalle: {intervalle}, IC: {ic_actuel:.5f} \n "  
        if ic_actuel > seuil_ic:
            return intervalle, result
    return None, result

def cle_repetition(c, dic, v):
    T = []
    d = ''
    s, compt = Compteur(c)
    for i in c:
        if i != ' ':
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

def trouver_intervalle_anormal_babbage(c, dic, v):
    result = ''
    T, s = cle_repetition(c, dic, v)
    d = {}
    k = 0
    for i in T:
        d[i] = s[k]
        k = k + 1

    for key in d:
        result += f"Clé: {key}, Taille: {d[key]} \n "  
    return result

v = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
     'X', 'Y', 'Z']

dic = {'a': 0, 'â': 0, 'à': 0, 'Ä': 0, 'A': 0, 'b': 1, 'B': 1, 'c': 2, 'C': 2, 'ç': 2, 'd': 3, 'D': 3, 'e': 4, 'E': 4,
       'é': 4, 'è': 4, 'ê': 4, 'Ë': 4, 'f': 5, 'F': 5, 'g': 6, 'G': 6, 'h': 7, 'H': 7, 'i': 8, 'I': 8, 'î': 8, 'ï': 8,
       'j': 9, 'J': 9, 'k': 10, 'K': 10, 'l': 11, 'L': 11, 'm': 12, 'M': 12, 'n': 13, 'N': 13, 'o': 14, 'O': 14, 'ô': 14,
       'Ö': 14, 'p': 15, 'P': 15, 'q': 16, 'Q': 16, 'r': 17, 'R': 17, 's': 18, 'S': 18, 't': 19, 'T': 19, 'u': 20, 'û': 20,
       'Ü': 20, 'ù': 20, 'U': 20, 'v': 21, 'V': 21, 'w': 22, 'W': 22, 'x': 23, 'X': 23, 'y': 24, 'Y': 24, 'z': 25, 'Z': 25,
       ' ': 26}

class VigenereApp:
    def __init__(self, root):
        self.root = root
        self.root.title('CryptoApp')

        self.m_label = ttk.Label(root, text='Entrez le texte:')
        self.m_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=5)
        self.k_label = ttk.Label(root, text='Entrez la clé')
        self.k_entry = ttk.Entry(root)
        self.output_label = ttk.Label(root, text='Sortie:')
        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=5)

        self.method_label = ttk.Label(root, text='Sélectionnez la méthode:')
        self.method_var = tk.StringVar()
        self.method_combobox = ttk.Combobox(root, textvariable=self.method_var,
                                            values=('Indice de Coïncidence', 'Babbage'))

        self.encode_button = ttk.Button(root, text='chiffrer', command=self.encode)
        self.decode_button = ttk.Button(root, text='déchiffrer', command=self.decode)
        self.cryptanalyze_button = ttk.Button(root, text='Cryptanalyse', command=self.cryptanalyze)
        self.clear_button = ttk.Button(root, text='supprimer', command=self.clear)
        self.load_file_button = ttk.Button(root, text='importer un txt', command=self.load_file)

        self.setup_ui()

    def setup_ui(self):
        self.m_label.grid(row=0, column=0, pady=(10, 0), sticky='w')
        self.m_entry.grid(row=1, column=0, padx=10, pady=(0, 10), columnspan=2)

        self.k_label.grid(row=2, column=0, pady=(10, 0), sticky='w')
        self.k_entry.grid(row=3, column=0, padx=10, pady=(0, 10), columnspan=2)

        self.method_label.grid(row=4, column=0, pady=(10, 0), sticky='w')
        self.method_combobox.grid(row=5, column=0, padx=10, pady=(0, 10), columnspan=2)

        self.encode_button.grid(row=6, column=0, pady=(10, 0), padx=10, sticky='w')
        self.decode_button.grid(row=6, column=1, pady=(10, 0), padx=10, sticky='w')
        self.cryptanalyze_button.grid(row=6, column=2, pady=(10, 0), padx=10, sticky='w')
        self.clear_button.grid(row=6, column=3, pady=(10, 0), padx=10, sticky='w')
        self.load_file_button.grid(row=6, column=4, pady=(10, 0), padx=10, sticky='w')

        self.output_label.grid(row=7, column=0, pady=(10, 0), sticky='w')
        self.output_text.grid(row=8, column=0, padx=10, pady=(0, 10), columnspan=2)

    def encode(self):
        m = self.m_entry.get("1.0", tk.END).strip()
        k = self.k_entry.get().upper()

        if len(k) > 0:
            c = Vchiffrer(m, k, dic, v)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, str(c))
        else:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, 'La clé de chiffrement est vide.')

    def decode(self):
        m = self.m_entry.get("1.0", tk.END).strip()
        k = self.k_entry.get().upper()

        if len(k) > 0:
            c = Vdechiffrer(m, k, dic, v)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, str(c))
        else:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, 'La clé de déchiffrement est vide.')

    def extraire_messages(self, texte, intervalle):
        messages_extraits = []
        for i in range(intervalle):
            sous_chaine = texte[i::intervalle]
            messages_extraits.append(sous_chaine)
        return messages_extraits

    def calculer_cle_indice_coincidence(self, messages_extraits):
        if not messages_extraits:
            return ""

        longueur_cle = len(messages_extraits[0])
        cle = ""

        for i in range(longueur_cle):
            sous_chaine = [message[i] for message in messages_extraits if len(message) > i]

            if sous_chaine:
                frequences = {lettre: sous_chaine.count(lettre) for lettre in set(sous_chaine)}
                lettre_cle = max(frequences, key=frequences.get)
                cle += lettre_cle

        return cle

    def show_cryptanalysis_results(self, cle_calcul, result_text):
        popup = tk.Toplevel(self.root)
        popup.title('Résultats de la cryptanalyse')

        scroll_view = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=80, height=20)
        scroll_view.pack(padx=10, pady=10)

        scroll_view.insert(tk.END, result_text)

    def cryptanalyze(self):
        m = self.m_entry.get("1.0", tk.END).strip()
        method = self.method_var.get()

        if len(m) > 0 and method:
            if method == 'Indice de Coïncidence':
                abnormal_interval, result = trouver_intervalle_anormal_ic(m)
                if abnormal_interval:
                    messages_extraits = self.extraire_messages(m, abnormal_interval)
                    cle_calcul = self.calculer_cle_indice_coincidence(messages_extraits)

                    result += f"Longueur de la clé : {abnormal_interval}\n"
                    self.show_cryptanalysis_results(cle_calcul, result)
                else:
                    self.output_text.delete("1.0", tk.END)
                    self.output_text.insert(tk.END, 'Pas d''intervalle anormal trouvé.')
            elif method == 'Babbage':
                result = trouver_intervalle_anormal_babbage(m, dic, v)
                self.show_cryptanalysis_results('', result)
        else:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, 'Vous n''avez pas entré de texte ou vous n''avez pas choisi de méthode.')



    def clear(self):
        self.m_entry.delete("1.0", tk.END)
        self.k_entry.delete(0, tk.END)
        self.output_text.delete("1.0", tk.END)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.m_entry.delete("1.0", tk.END)
                self.m_entry.insert(tk.END, content)


if __name__ == '__main__':
    root = tk.Tk()
    app = VigenereApp(root)
    root.mainloop()
