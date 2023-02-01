# observações:
# não é possível inserir texto por código no tkinter.Text caso
# ele esteja desativado. isso é uma limitação se comparado ao 
# gtk.

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import re
from json import load
from pathlib import Path
from random import choice
import sys
from string import printable
from unittest.mock import Mock


def retornar_local():
    """Retorna o local onde o programa está rodando."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)  # noqa
    else:
        return Path('.')

local_da_execucao = retornar_local()

with open(local_da_execucao / "config/teclas.json") as arquivo:
    dicionário = load(arquivo)

# refatorar. mover para outro escopo?
printable = printable[:-2]
right_shift = "qwertasdfgzxcvbãáâàêé"
left_shift = "yuiophjklçnmíõôóú"
lr = right_shift + left_shift
dedos = [
    "'\"1qaz\\|",
    "2wsx",
    "3edc",
    "45rtfgvb",
    "0pç;:/?~^´`-_=+[]{}\n",
    "9ol>.",
    "8ik<,",
    "67yuhjnm",
]
jogo1 = "abcdefghijklmnopqrstuvxwyzç,.;/~]´[\\"
jogo4 = "ãêáõôéâíóúà`´~^" + "ãêáõôéâíóúà".upper()

with open(local_da_execucao / "palavras.txt", "r") as file:
    palavras = set([palavra.strip() for palavra in file.readlines()])

if Path("palavras_erradas.txt").exists():
    with open("palavras_erradas.txt") as file:
        palavras_erradas = set([palavra.strip() for palavra in file.readlines()])
    palavras -= palavras_erradas
else:
    palavras_erradas = set()
palavras = list(palavras)
palavras_erradas = list(palavras_erradas)


# def colorir(texto, posicao, cor="green1"):
#     """
#     Função que colore um texto em uma determinada posição.
#     """
#     texto = list(map("".join, re.findall(r"(\s*)(\S*)(\s*)", texto)))
#     # texto = texto.split(' ')  # não remova o espaço
#     texto[posicao] = f'<span color="{cor}">{texto[posicao]}</span>'
#     return "".join(texto)


class Janela(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # criando objetos.
        # pango = Pango.FontDescription("ubuntu 17")
        
        self._apagar = False
        self.cache = ""
        self.red_cache = ""
        self.prof_cache = ""
        self.texto_do_arquivo = []
        self._arquivo_aberto = False
        self._texto_colado = False
        self.n_word_cache = -1
        self.jogo_escolhido = 'Nenhum'
        self._mostrar_maos_visivel = False
        self.n_jogos = {
            'Nenhum': lambda: 1,
            "Adivinhe a tecla": self._jogo1,
            "Digite a palavra": self._jogo2,
            "Treinar acentos": self._jogo3
        }
        
        # Carregando o nome das imagens.
        with open(local_da_execucao / "config/imagens.json") as arquivo:
            imagens = load(arquivo)
            self.imagens = dict()
            for dicio in imagens:
                self.imagens.update(dicio)
        
        # Barra Lateral:
        # Definindo os widgets da barra:
        self.label_adicionar_arquivo = tk.Label(self)
        
        # =========================== FRAME_CIMA ===========================
        
        # Criando o Frame:
        self.frame_cima = tk.Frame(self)
        
        # Posicionando o Frame:
        self.frame_cima.grid(
            column=0,
            row=0
        )
        
        # Criando os Frames das linhas:
        self.linhas = {
            'linha0': tk.Frame(self.frame_cima),
            'linhas2_3': tk.Frame(self.frame_cima)
        }

        self.linhas.update({
            'esc': tk.Frame(self.linhas['linha0']),
            'f1_f4': tk.Frame(self.linhas['linha0']),
            'f5_f8': tk.Frame(self.linhas['linha0']),
            'f9_f12': tk.Frame(self.linhas['linha0']),
            
            'linha1': tk.Frame(self.frame_cima),
            
            
            'enter': tk.Frame(self.linhas['linhas2_3']),
            'linha2': tk.Frame(self.linhas['linhas2_3']),
            'linha3': tk.Frame(self.linhas['linhas2_3']),
            
            'linha4': tk.Frame(self.frame_cima),
            'linha5': tk.Frame(self.frame_cima)
        })
        
        # Posicionando as linhas:
        self.linhas['linha0'].grid(row=0, column=0)
        self.linhas['linha1'].grid(row=1, column=0)
        self.linhas['linhas2_3'].grid(row=2, rowspan=2, column=0)
        self.linhas['linha4'].grid(row=4, column=0)
        self.linhas['linha5'].grid(row=5, column=0)
        
        # Posicionando as box dentro das linhas:
        # Linha 0:
        self.linhas['esc'].grid(row=0, column=0)
        self.linhas['f1_f4'].grid(row=0, column=1, padx=10)
        self.linhas['f5_f8'].grid(row=0, column=2, padx=10)
        self.linhas['f9_f12'].grid(row=0, column=3, padx=10)
        
        # Linhas 2 e 3:
        self.linhas['linha2'].grid(column=0, row=0)
        self.linhas['linha3'].grid(column=0, row=1)
        self.linhas['enter'].grid(column=1, row=0, rowspan=2)
        

        '''
        dentro de labels_com_imagens irá conter listas e cada lista
        irá conter uma fileira de imagens do programa.
        exemplo: imagem do exc, f1, f2, f3, f4 até f12, que será a primeira fileira.
        '''

        # Colocando as imagens nos Labels:
        labels_com_imagens = []  # Lista dos Labels;
        
        # laço For para percorrer o imagens.json
        for numero, dicio in enumerate(imagens):
            lista = []
            labels_com_imagens.append(lista)
            
            # Percorrendo dicionários internos nos índices de imagens.json
            for numero_do_label, nome in enumerate(dicio):
                linha_x = f'linha{numero}'
                
                # Abrindo a imagem a ser inserida no label:
                local_da_imagem = (
                    local_da_execucao / f"imagens/normais/{nome}.png"
                )
                with Image.open(local_da_imagem) as arquivo:
                    img_local = ImageTk.PhotoImage(arquivo)
                                                                               
                # Inserindo as imagens nos devidos lugares:
                if numero != 0:
                    if nome == 'enter':
                        label = tk.Label(self.linhas['enter'])
                        
                    else:
                        label = tk.Label(self.linhas[linha_x])
                    
                    label.pack(side='left')
                    
                else:
                    if numero_do_label == 0:
                        label = tk.Label(self.linhas['esc'])
                        
                    elif 1 <= numero_do_label <= 4:
                        label = tk.Label(self.linhas['f1_f4'])
                    
                    elif 5 <= numero_do_label <= 8:
                        label = tk.Label(self.linhas['f5_f8'])
                    
                    else:
                        label = tk.Label(self.linhas['f9_f12'])
                    
                    label.pack(side='left')
                    
                # Colocando a imagem no Label
                label.configure(image=img_local)
                label.image = img_local
                lista.append(label)

                # Colocando a imagem no dicionário de imagens
                self.imagens[nome] = label

        # ==================================================================
        # ========================== FRAME_DIREITA =========================
        '''
        Aqui vão algumas abas de configurações do programa
        e algumas opções, como abrir arquivos *.txt
        '''
        # Criando o Frame:
        self.frame_direita = tk.Frame(self)
        
        # Posicionando o Frame:
        self.frame_direita.grid(
            column=1,
            row=0,
            rowspan=2
        )
        
        # Criando os Labels:
        label_texto = tk.Label(
            self.frame_direita,
            text='Adicione um arquivo \ne comece a digitar \npor ele.'
        )
        label_jogos = tk.Label(
            self.frame_direita,
            text='Jogos:'
        )

        # Criando os botões de pegar e remover arquivo:
        self.botao_abrir_arquivo = tk.Button(
            self.frame_direita,
            text='Abrir arquivo',
            command=self.abrir_arquivo
        )
        self.botao_remover_arquivo = tk.Button(
            self.frame_direita,
            text='Remover arquivo',
            command=self.remover_arquivo
        )

        # Configurando os botões de pegar e remover arquvo:
        self.botao_remover_arquivo.config(state='disabled')
        
        # Criando o BooleanVar para o button_auto_apagar:
        self._status_auto_apagar = tk.BooleanVar()

        # Criando os RadioButtons:
        self.button_mostrar_maos = tk.Checkbutton(
            self.frame_direita,
            text = 'mostrar mãos',
            command = self.mostrar_imagem
        )
        self.button_auto_apagar = tk.Checkbutton(
            self.frame_direita,
            text = 'auto-apagar',
            command = self.auto_apagar_clicado,
            variable = self._status_auto_apagar
        )

        # Criando a ComboBox:
        self.combobox_jogos = ttk.Combobox(self.frame_direita, state="readonly")
        ttk.Style().configure('TCombobox', relief='flat')
        
        # Definindo os valores da Combobox:
        self.nomes_dos_jogos = (
            'Nenhum',
            'Adivinhe a tecla',
            'Digite a palavra',
            'Treinar acentos'
        )
        self.combobox_jogos['values'] = self.nomes_dos_jogos
        self.combobox_jogos.current(0)
        
        # Posicionando os Widgets:
        label_texto.grid()
        self.botao_abrir_arquivo.grid()
        self.botao_remover_arquivo.grid()
        self.button_mostrar_maos.grid()
        self.button_auto_apagar.grid()
        label_jogos.grid()
        self.combobox_jogos.grid()
        
        # ==================================================================
        # =========================== FRAME_BAIXO ==========================
        # Criando o Frame:
        self.frame_baixo = tk.Frame(self)
        
        # Posicionando os Frames:
        self.frame_baixo.grid(
            column=0,
            row=1
        )
        
        # Criando os Texts:
        self._text_professor = tk.Text(self.frame_baixo)
        self._text_aluno = tk.Text(self.frame_baixo)

        # Criando e configurando as scroolbar
        # ================== criar aqui

        # Criando as StringVar para armazenar o conteúdo digitado pelo usuário das Entries:
        # self._stringvar_texto = tk.StringVar()
        # self._stringvar_digitar = tk.StringVar()
        # self._entry_texto['textvariable'] = self._stringvar_texto
        # self._entry_digitar['textvariable'] = self._stringvar_digitar
        
        # Criando os Labels:
        label_texto1 = tk.Label(
            self.frame_baixo,
            text='Insira um texto abaixo (copiando e colando):'
        )
        
        label_texto2 = tk.Label(
            self.frame_baixo,
            text='Replique o texto abaixo:'
        )

        # Criando o frame, o label para a imagem:
        self.frame_imagem_maos = tk.Frame(self.frame_baixo)
        self._label_imagem_maos = tk.Label(self.frame_imagem_maos)
        local_da_imagem = (
            local_da_execucao / f"imagens/mãos.png"
        )
        with Image.open(local_da_imagem) as arquivo:
            img_local = ImageTk.PhotoImage(arquivo)
        self._label_imagem_maos.configure(image=img_local)
        self._label_imagem_maos.image = img_local
        
        # Posicionando os Widgets:
        label_texto1.pack()
        self._text_professor.config(width=65, height=6)
        self._text_professor.pack() #(ipadx=200, ipady=30)
        label_texto2.pack()
        self._text_aluno.config(width=65, height=6)
        self._text_aluno.pack() #(ipadx=200, ipady=30)
        self.frame_imagem_maos.pack_forget()
        self._label_imagem_maos.pack_forget()
        # ==================================================================

        # conectando objetos.
        # self._mostrar_maos.connect("toggled", self.mostrar_imagem)
        self._text_aluno.bind('<KeyRelease>', self.aluno_digitando)
        self._text_professor.bind('<KeyRelease>', self.professor_digitando)
        self._text_professor.bind('<Control-v><KeyRelease>', self.texto_colado)
        self.combobox_jogos.bind('<<ComboboxSelected>>', self.jogo_alterado)

        # configurando.
        self.title("programa para aprender a digitar")
    
    def mostrar_imagem(self):
        """Método que mostra a imagem dos dedos."""
        self._mostrar_maos_visivel = not self._mostrar_maos_visivel
        if self._mostrar_maos_visivel:
            self.frame_imagem_maos.pack()
            self._label_imagem_maos.pack()
        else:
            self.frame_imagem_maos.pack_forget()
            self._label_imagem_maos.pack_forget()

    def aluno_digitando(self, evento):
        """
        Método que verifica qual caracter foi pressionado e define a próxima imagem.
        """
        prof = self._text_professor
        aluno = self._text_aluno
        texto = self._obter_texto('aluno')
        texto_professor = self._obter_texto('professor')
        self._normalizar_imagem()
        self._textos_iguais(texto, texto_professor, prof, aluno)
        condicao = [
            all([texto, self._apagar]),
            not texto_professor.startswith(texto)
        ]
        if all(condicao):
            self._limpar_texto('aluno')
            self._text_aluno.insert(1.0, texto[:-1])
        self._imagens(prof, aluno)

    def _textos_iguais(self, texto, texto_professor, prof, aluno):
        """Método que verifica se o texto é igual."""
        if texto_professor == texto:
            if self.texto_do_arquivo:
                texto_professor_ = self.texto_do_arquivo.pop(0)
                self._limpar_texto('ambos')
                prof.insert(1.0, texto_professor_)
                evento_mock = Mock(char='a')
                self.professor_digitando(evento_mock)
                self.n_word_cache = -1
            else:
                self.remover_arquivo()
                self._limpar_texto('professor')
            self._limpar_texto('aluno')

    # a diferença entre o método _textos_iguais e esse é que esse não
    # tem self.remover_arquivo
    def _textos_iguais_jogo_2(self, texto, texto_professor, prof, aluno):
        """Método que verifica se o texto é igual."""
        if texto_professor == texto:
            if self.texto_do_arquivo:
                texto_professor_ = self.texto_do_arquivo.pop(0)
                self._limpar_texto('ambos')
                prof.insert(1.0, texto_professor_)
                evento_mock = Mock(char='a')
                self.professor_digitando(evento_mock)
                self.n_word_cache = -1
            else:
                self._limpar_texto('professor')
            self._limpar_texto('aluno')

    def _imagens(self, prof, aluno):
        """Método que define a imagem como vermelha ou branca."""
        texto = self._obter_texto('aluno')
        texto_professor = self._obter_texto('professor')
        if texto_professor.startswith(texto) and texto_professor != texto:
            # define a imagem como branca
            self.cache = texto_professor[len(texto):][0]
            self._definir_imagem(self.cache, "brancas")
        elif not texto_professor.startswith(texto):
            # define a imagem como vermelha
            if texto:
                self._definir_imagem("backspace", "brancas")
            self.red_cache = texto[-1]
            self._definir_imagem(self.red_cache, "vermelhas")
        # self._colorir_texto(texto_professor, texto)

    def professor_digitando(self, evento):
        """Método que gerencia a popup e define a próxima imagem como branca."""
        texto_professor = self._obter_texto('professor')
        if not bool(texto_professor):
            self._normalizar_imagem()
            # self._popover.hide()
            # self._poplabel.set_text("")
        if evento.char in printable and bool(texto_professor):
            opcoes = [
                len(texto_professor) == 1,
                self.texto_do_arquivo,
                self._texto_colado
            ]
            if any(opcoes):
                self._normalizar_imagem()
                self.cache = self.prof_cache = texto_professor[0]
                self._definir_imagem(self.prof_cache, "brancas")

    def texto_colado(self, evento):
        """Método que chama o professor_digitando caso o texto seja colado."""
        self._texto_colado = not self._texto_colado
        evento_mock = Mock()
        evento_mock.char = 'a'
        self.professor_digitando(evento_mock)
        self._texto_colado = not self._texto_colado

    def auto_apagar_clicado(self):
        """Método que seta a variável _apagar para verdadeiro ou falso e apaga o texto do aluno."""
        self._apagar = not self._apagar
        self._limpar_texto('aluno')
        self.aluno_digitando(None)

    def _normalizar_imagem(self):
        """Método que volta a imagem ao padrão."""
        if self.cache:
            self._definir_imagem(self.cache, "normais")
            self.cache = ""
        if self.red_cache:
            self._definir_imagem(self.red_cache, "normais")
            self._definir_imagem("backspace", "normais")
            self.red_cache = ""
        if self.prof_cache:
            self._definir_imagem(self.prof_cache, "normais")
            self.prof_cache = ""

    # argumentos:
    # letra -> qualquer letra do alfabeto português, com ou sem acento.
    # pasta -> nome da pasta onde contem a imagem.
    # o que pode ser passado para pasta: brancas, interrogacao, normais, vermelhas.
    # nomeNaoDicionario -> é um nome que não contem no dicionário.
    # o que pode ser passado para nomeNaoDicionario: pequenas, pequenas_red
    def _definir_imagem(self, letra, pasta, nomeNaoDicionario=""):
        """Método que define a imagem."""
        for imagem in dicionário.get(letra.lower(), letra.lower()):
            quadro = self.imagens.get(imagem)
            if bool(quadro):
                local_imagem = f"imagens/{pasta}/{nomeNaoDicionario or imagem}.png"
                with Image.open(str(local_da_execucao / local_imagem)) as arquivo:
                    img_local = ImageTk.PhotoImage(arquivo)
                quadro.configure(image=img_local)
                quadro.image = img_local
        if pasta == "brancas":
            # self._dedos(letra, imagem, quadro)
            pass
        if all([letra.isupper(), letra.lower() in lr]):
            if imagem.lower() in right_shift:
                shift = "direito"
            elif imagem.lower() in left_shift:
                shift = "esquerdo"
            quadro = self.imagens.get(f"shift_{shift}")
            imagem = f"imagens/{pasta}/shift_{shift}.png"
            with Image.open(str(local_da_execucao / imagem)) as arquivo:
                    img_local = ImageTk.PhotoImage(arquivo)
            quadro.configure(image=img_local)
            quadro.image = img_local

    # parâmetro usuario pode receber: 'aluno', 'professor', 'ambos'
    def _limpar_texto(self, usuario="aluno"):
        """Método que limpa o texto do aluno, professor ou ambos."""
        prof, aluno = self._text_professor, self._text_aluno
        if usuario == "aluno":
            aluno.delete(1.0, 'end')
        elif usuario == "professor":
            prof.delete(1.0, 'end')
        elif usuario == "ambos":
            prof.delete(1.0, 'end')
            aluno.delete(1.0, 'end')

    def _obter_texto(self, usuario):
        """Método que obtem o texto do aluno ou o do professor."""
        if usuario == 'aluno':
            user = self._text_aluno
        elif usuario == 'professor':
            user = self._text_professor
        texto = user.get(1.0, "end-1c")
        return texto

    # def _dedos(self, letra, imagem, quadro):
    #     """
    #     Método que mostra a popup na imagem correta com o número do dedo correto.
    #     """
    #     for conjunto in dedos:
    #         if imagem.lower() in conjunto or letra.lower() in conjunto:
    #             texto = str(dedos.index(conjunto) % 4 + 1)
    #             self._mostrar_popup(quadro, texto)
    #     if letra == " ":
    #         self._mostrar_popup(quadro, "5")

    def abrir_arquivo(self):
        """Método que abre o arquivo e exibe a primeira palavra."""
        self._limpar_texto('ambos')
        try:
            self.combobox_jogos.current(0)
            with filedialog.askopenfile() as arquivo:
                self.texto_do_arquivo = arquivo.readlines()
            # self._text_professor.config(state='disabled')
            # não pode desabilitar senão ele não insere texto
            self._arquivo_aberto = True
            self.aluno_digitando(None)
            self._arquivo_aberto = False
            self.botao_remover_arquivo.config(state='normal')
        except AttributeError:
            pass

    def remover_arquivo(self):
        """Método que remove o arquivo."""
        self._normalizar_imagem()
        self.texto_do_arquivo = []
        self._limpar_texto("ambos")
        self.botao_remover_arquivo.config(state='disabled')
        # self._popover.hide()

    # def _mostrar_popup(self, tecla, texto):
    #     """Método que mostra a popup."""
    #     self._popover.hide()
    #     self._poplabel.set_text(f"dedo: {texto}")
    #     self._popover.set_relative_to(tecla)
    #     self._popover.show()

    def jogo_alterado(self, evento):
        """Método que altera o tipo de jogo."""
        self.remover_arquivo()
        self.jogo_escolhido = self.combobox_jogos.get()
        self._normalizar_imagem()
        self.cache = ''
        self.button_auto_apagar['state'] = 'disabled'
        if self.jogo_escolhido == self.nomes_dos_jogos[0]:
            self._text_aluno.unbind('<KeyRelease>')
            self._text_aluno.bind('<KeyRelease>', self.aluno_digitando)
            self._normalizar_imagem()
            # gera um bug quando desabilita
            # self._text_professor.config(state='normal')
            self._limpar_texto('ambos')
            self.button_auto_apagar['state'] = 'normal'
        else:
            self._text_aluno.unbind('<KeyRelease>')
            self._text_aluno.bind('<KeyRelease>', self._jogo)
            # gera um bug quando desabilita
            # self._text_professor.config(state='disabled')
            self._limpar_texto('ambos')
            if self.jogo_escolhido == self.nomes_dos_jogos[2]:
                self.button_auto_apagar['state'] = 'normal'
            else:
                self.button_auto_apagar['state'] = 'disabled'
            self._jogo(None)  # é preciso chamar a primeira vez
        self._apagar = False
        self._status_auto_apagar.set(False)

    # def _colorir_texto(self, texto_p, texto):
    #     """Método que colore um texto em um text_view."""
    #     prof = self._professor_texto
    #     condicoes = [
    #         bool(texto_p),
    #         texto.count(" ") <= texto_p.count(" "),
    #         texto_p.count(" ") > 0,
    #         texto.count(" ") != self.n_word_cache,
    #     ]
    #     if all(condicoes):
    #         prof.set_text("")
    #         generator = map("".join, re.findall(r"(\s*)(\S*)(\s*)", texto))
    #         numero = len(list(generator))
    #         prof.insert_markup(prof.get_end_iter(), colorir(texto_p, numero - 2), -1)
    #         self.n_word_cache = numero
    #         # numero <- texto.count(' ')

    def _jogo(self, widget):
        """
        Método que roda os jogos escolhidos quando algum jogo é escolhido.
        """
        self.n_jogos[self.jogo_escolhido]()

    def _jogo1(self):
        """Método que joga o jogo 1."""
        letra = self._obter_texto('aluno')[-1:]  # não remova os pontos pois gera um bug
        self._limpar_texto('aluno')
        self._text_aluno.insert(1.0, letra)
        if letra == self.cache:
            self._normalizar_imagem()
            self.cache = choice(jogo1)
            self._definir_imagem(self.cache, "interrogacao", "pequenas")

    def _jogo2(self):
        """Método que roda o jogo 2."""
        self._definir_imagem("backspace", "normais")
        self._normalizar_imagem()
        prof = self._text_professor
        aluno = self._text_aluno
        texto = self._obter_texto('aluno')
        texto_professor = self._obter_texto('professor')
        # é obrigatório chamar o _textos_iguais antes do if senão gera um bug
        self._textos_iguais_jogo_2(texto, texto_professor, prof, aluno)
        if not texto_professor:
            prof.insert(1.0, choice(palavras))
        self._imagens(prof, aluno)

    def _jogo3(self):
        """Método que roda o jogo 3."""
        letra = self._obter_texto('aluno')[-1:]  # não remova os pontos
        self._limpar_texto('aluno')
        self._text_aluno.insert(1.0, letra)
        if letra == self.cache:
            self._normalizar_imagem()
            self.cache = choice(jogo4)
            self._definir_imagem(self.cache, "brancas")
            self._limpar_texto('professor')
            self._text_professor.insert(1.0, self.cache)

# Executando a janela:
def main():
    app = Janela()  # noqa
    tk.mainloop() 
