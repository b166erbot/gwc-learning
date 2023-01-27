import re
from json import load
from pathlib import Path
from random import choice
import sys

import gi

gi.require_version("Pango", "1.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa
from gi.repository import Pango  # noqa


def retornar_local():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    else:
        return Path('.')

local_da_execucao = retornar_local()

with open(local_da_execucao / "config/teclas.json") as arquivo:
    dicionário = load(arquivo)

# refatorar. mover para outro escopo?
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


def colorir(texto, posicao, cor="green1"):
    """
    Função que colore um texto em uma determinada posição.
    """
    texto = list(map("".join, re.findall(r"(\s*)(\S*)(\s*)", texto)))
    # texto = texto.split(' ')  # não remova o espaço
    texto[posicao] = f'<span color="{cor}">{texto[posicao]}</span>'
    return "".join(texto)


class Janela:
    def __init__(self):
        # criando objetos.
        pango = Pango.FontDescription("ubuntu 17")
        self._apagar = False
        self.cache = ""
        self.red_cache = ""
        self.prof_cache = ""
        self.builder = Gtk.Builder()
        self.texto_do_arquivo = []
        self.n_word_cache = -1
        self.jogo_escolhido = "0"
        self.n_jogos = {"1": self._jogo1, "2": self._jogo2, "3": self._jogo3}

        # obtendo a interface glade.
        self.builder.add_from_file(str(local_da_execucao / "gwc.glade"))

        # obtendo objetos.
        self._janela = self.builder.get_object("janela")
        self._mostrar_maos = self.builder.get_object("mostrar_maos")
        self._maos = self.builder.get_object("maos")
        self._auto_apagar = self.builder.get_object("auto_apagar")
        self._professor = self.builder.get_object("professor")
        self._aluno = self.builder.get_object("aluno")
        self._aluno_texto = self.builder.get_object("texto_aluno")
        self._professor_texto = self.builder.get_object("texto_professor")
        self._arquivo = self.builder.get_object("arquivo")
        self._limpar_arquivo = self.builder.get_object("limpar_arquivo")
        self._popover = self.builder.get_object("popover")
        self._poplabel = self.builder.get_object("poplabel")
        self._jogos = self.builder.get_object("jogos")
        self._niveis = self.builder.get_object("niveis")
        self._area_arquivo = self.builder.get_object("area_arquivo")
        self._area_opcoes = self.builder.get_object("area_opcoes")
        self._niveis_botao = self.builder.get_object("níveis")
        self._remover_palavra = self.builder.get_object("remover_palavra")

        with open(local_da_execucao / "config/imagens.json") as arquivo:
            imagens = load(arquivo)
            self.imagens = {
                chave: self.builder.get_object(valor)
                for chave, valor in imagens.items()
            }

        # conectando objetos.
        self._janela.connect("destroy", Gtk.main_quit)
        self._mostrar_maos.connect("toggled", self.mostrar_imagem)
        self._aluno_texto.connect("end-user-action", self.aluno_digitando)
        self._professor_texto.connect("end-user-action", self.professor_digitando)
        self._auto_apagar.connect("toggled", self.auto_apagar_clicado)
        self._arquivo.connect("file-set", self.arquivo_escolhido)
        self._limpar_arquivo.connect("clicked", self.remover_arquivo)
        self._jogos.connect("changed", self.jogo_alterado)
        self._niveis_botao.connect("changed", self._nivel_alterado)
        self._remover_palavra.connect("clicked", self._remover_palavra_funcao)

        # configurando.
        self._janela.set_title("programa para aprender a digitar")
        self._professor.modify_font(pango)
        self._aluno.modify_font(pango)

    def mostrar_imagem(self, widget):
        """Método que mostra a imagem dos dedos."""
        self._maos.set_visible(not self._maos.is_visible())

    def aluno_digitando(self, widget):
        """
        Método que verifica qual caracter foi pressionado e define a próxima imagem.
        """
        prof = self._professor_texto
        aluno = widget
        texto = self._obter_texto('aluno')
        texto_professor = self._obter_texto('professor')
        self._normalizar_imagem()
        self._textos_iguais(texto, texto_professor, prof, aluno)
        self._imagens(prof, aluno)

    def _textos_iguais(self, texto, texto_professor, prof, aluno):
        """Método que verifica se o texto é igual."""
        if texto_professor == texto:
            if self.texto_do_arquivo:
                prof.set_text(self.texto_do_arquivo[0])
                self.professor_digitando(self._professor_texto)
                texto_professor = self.texto_do_arquivo.pop(0)
                self.n_word_cache = -1
            else:
                self.remover_arquivo(None)
                prof.set_text("")
            aluno.set_text("")

    def _textos_iguais_jogo_2(self, texto, texto_professor, prof, aluno):
        """Método que verifica se o texto é igual."""
        if texto_professor == texto:
            if self.texto_do_arquivo:
                prof.set_text(self.texto_do_arquivo[0])
                self.professor_digitando(self._professor_texto)
                texto_professor = self.texto_do_arquivo.pop(0)
                self.n_word_cache = -1
            else:
                prof.set_text("")
            aluno.set_text("")

    def _imagens(self, prof, aluno):
        """Método que define a imagem como vermelha ou branca."""
        texto = self._obter_texto('aluno')
        texto_professor = self._obter_texto('professor')
        if texto_professor.startswith(texto) and texto_professor != texto:
            # define a imagem como branca
            self.cache = texto_professor[len(texto) :][0]
            self._definir_imagem(self.cache, "brancas")
        elif not texto_professor.startswith(texto):
            # define a imagem como vermelha
            if all([texto, self._apagar]):
                self._aluno.do_backspace(self._aluno)
            elif texto:
                self._definir_imagem("backspace", "brancas")
            self.red_cache = texto[-1]
            self._definir_imagem(self.red_cache, "vermelhas")
        self._colorir_texto(texto_professor, texto)

    def _imagens_jogo_2(self, prof, aluno):
        """Método que define a imagem como vermelha ou branca."""
        texto = self._obter_texto('aluno')
        texto_professor = self._obter_texto('professor')
        if texto_professor.startswith(texto) and texto_professor != texto:
            # define a imagem como branca
            self.cache = texto_professor[len(texto) :][0]
            botao_ativo = int(self._niveis_botao.get_active_id())
            if botao_ativo > 0:
                self._definir_imagem(self.cache, "interrogacao", "pequenas")
            else:
                self._definir_imagem(self.cache, "brancas")
        elif not texto_professor.startswith(texto):
            # define a imagem como vermelha
            # fazer o do_backspace ou definir backspace como brancas
            if all([texto, self._apagar]):
                self._aluno.do_backspace(self._aluno)
            elif texto:
                self._definir_imagem("backspace", "brancas")
            self.red_cache = texto[-1]
            self._definir_imagem(self.red_cache, "interrogacao", 'pequenas_red')
        self._colorir_texto(texto_professor, texto)

    def professor_digitando(self, widget):
        """Método que gerencia a popup e define a próxima imagem como branca."""
        texto_professor = self._obter_texto('professor')
        if len(texto_professor) == 1 or self.texto_do_arquivo:
            self._normalizar_imagem()
            self.cache = self.prof_cache = texto_professor[0]
            self._definir_imagem(self.prof_cache, "brancas")
        elif not texto_professor:
            self._normalizar_imagem()
            self._popover.hide()
            self._poplabel.set_text("")

    def auto_apagar_clicado(self, widget):
        """Método que seta a variável _apagar para verdadeiro ou falso e apaga o texto do aluno."""
        self._apagar = not self._apagar
        self._aluno_texto.set_text("")
        self.aluno_digitando(self._aluno_texto)

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
                quadro.set_from_file(str(local_da_execucao / local_imagem))
        if pasta == "brancas":
            self._dedos(letra, imagem, quadro)
        if all([letra.isupper(), letra.lower() in lr]):
            if imagem.lower() in right_shift:
                shift = "direito"
            elif imagem.lower() in left_shift:
                shift = "esquerdo"
            quadro = self.imagens.get(f"shift_{shift}")
            imagem = f"imagens/{pasta}/shift_{shift}.png"
            quadro.set_from_file(str(local_da_execucao / imagem))

    def _limpar_texto(self, usuario="aluno"):
        """Método que limpa o texto do aluno, professor ou ambos."""
        # 'aluno', 'professor', 'ambos'
        prof, aluno = self._professor_texto, self._aluno_texto
        if usuario == "aluno":
            aluno.delete(aluno.get_start_iter(), aluno.get_end_iter())
        elif usuario == "professor":
            prof.delete(prof.get_start_iter(), prof.get_end_iter())
        elif usuario == "ambos":
            prof.delete(prof.get_start_iter(), prof.get_end_iter())
            aluno.delete(aluno.get_start_iter(), aluno.get_end_iter())

    def _obter_texto(self, usuario):
        """Método que obtem o texto do aluno ou o do professor."""
        if usuario == 'aluno':
            user = self._aluno_texto
        elif usuario == 'professor':
            user = self._professor_texto
        texto = user.get_text(user.get_start_iter(), user.get_end_iter(), False)
        return texto

    def _dedos(self, letra, imagem, quadro):
        """
        Método que mostra a popup na imagem correta com o número do dedo correto.
        """
        for conjunto in dedos:
            if imagem.lower() in conjunto or letra.lower() in conjunto:
                texto = str(dedos.index(conjunto) % 4 + 1)
                self._mostrar_popup(quadro, texto)
        if letra == " ":
            self._mostrar_popup(quadro, "5")

    def arquivo_escolhido(self, widget):
        """Método que abre o arquivo e exibe a primeira palavra."""
        self._limpar_texto("ambos")
        with open(widget.get_filename(), "r") as f:
            self.texto_do_arquivo = f.readlines()
        self.aluno_digitando(self._aluno_texto)

    def remover_arquivo(self, widget):
        """Método que remove o arquivo."""
        if self._arquivo.get_filename():
            self._arquivo.unselect_file(self._arquivo.get_file())
        # limpar o self.texto_do_arquivo, aluno, professor e normalizar as imagens
        self._normalizar_imagem()
        self.texto_do_arquivo = []
        self._limpar_texto("ambos")
        self._popover.hide()

    def _mostrar_popup(self, tecla, texto):
        """Método que mostra a popup."""
        self._popover.hide()
        self._poplabel.set_text(f"dedo: {texto}")
        self._popover.set_relative_to(tecla)
        self._popover.show()

    def jogo_alterado(self, widget):
        """Método que altera o tipo de jogo."""
        self.remover_arquivo(None)
        cache = self.jogo_escolhido
        self.jogo_escolhido = widget.get_active_id()
        self._niveis_botao.set_active_id("0")
        for a in jogo1:
            self._definir_imagem(a, "normais")
        if self.jogo_escolhido == "0":
            self._aluno_texto.connect("end-user-action", self.aluno_digitando)
            if cache != "0":
                self._aluno_texto.disconnect_by_func(self._jogo)
            self._normalizar_imagem()
            self._niveis.set_visible(False)
            self._professor.set_sensitive(True)
            self._area_arquivo.set_sensitive(True)
            self._area_opcoes.set_sensitive(True)
            self._remover_palavra.set_visible(False)
        else:
            self._aluno_texto.connect("end-user-action", self._jogo)
            if cache == "0":
                self._aluno_texto.disconnect_by_func(self.aluno_digitando)
            self._niveis.set_visible(True)
            self._professor.set_sensitive(False)
            self._area_arquivo.set_sensitive(False)
            self._auto_apagar.set_active(False)
            self._mostrar_maos.set_active(False)
            if self.jogo_escolhido == "2":
                self._area_opcoes.set_sensitive(True)
            else:
                self._area_opcoes.set_sensitive(False)
            if self.jogo_escolhido == "2":
                self._remover_palavra.set_visible(True)
            else:
                self._remover_palavra.set_visible(False)
            self._jogo(None)  # é preciso chamar a primeira vez

    def _colorir_texto(self, texto_p, texto):
        """Método que colore um texto em um text_view."""
        prof = self._professor_texto
        condicoes = [
            bool(texto_p),
            texto.count(" ") <= texto_p.count(" "),
            texto_p.count(" ") > 0,
            texto.count(" ") != self.n_word_cache,
        ]
        if all(condicoes):
            prof.set_text("")
            generator = map("".join, re.findall(r"(\s*)(\S*)(\s*)", texto))
            numero = len(list(generator))
            prof.insert_markup(prof.get_end_iter(), colorir(texto_p, numero - 2), -1)
            self.n_word_cache = numero
            # numero <- texto.count(' ')

    def _jogo(self, widget):
        """
        Método que roda os jogos escolhidos quando algum jogo é escolhido.
        """
        self.n_jogos[self.jogo_escolhido]()

    def _jogo1(self):
        """Método que joga o jogo 1."""
        letra = self._obter_texto('aluno')[-1:]  # não remova os pontos pois gera um bug
        self._aluno_texto.set_text(letra)
        if letra == self.cache:
            if self._niveis_botao.get_active_id() != "0":
                self._definir_imagem(self.cache, "interrogacao", "pequenas_red")
            else:
                self._normalizar_imagem()
            self.cache = choice(jogo1)
            self._definir_imagem(self.cache, "interrogacao", "pequenas")

    def _jogo2(self):
        """Método que roda o jogo 2."""
        # é obrigatório chamar o _textos_iguais antes do if senão gera um bug
        self._definir_imagem("backspace", "normais")
        botao_ativo = int(self._niveis_botao.get_active_id())
        if botao_ativo == 0:
            self._normalizar_imagem()
        elif botao_ativo > 0:
            self._definir_imagem(self.cache, "interrogacao", "pequenas_red")
        prof = self._professor_texto
        texto = self._obter_texto('aluno')
        texto_professor = self._obter_texto('professor')
        self._textos_iguais_jogo_2(texto, texto_professor, prof, self._aluno_texto)
        if not self._obter_texto('professor'):
            self._professor_texto.set_text(choice(palavras))
        self._imagens_jogo_2(prof, self._aluno_texto)

    def _jogo3(self):
        """Método que roda o jogo 3."""
        letra = self._obter_texto('aluno')[-1:]  # não remova os pontos
        self._aluno_texto.set_text(letra)
        if letra == self.cache:
            self._normalizar_imagem()
            self.cache = choice(jogo4)
            botao_ativo = int(self._niveis_botao.get_active_id())
            if botao_ativo == 0:
                self._definir_imagem(self.cache, "brancas")
            if botao_ativo in [1, 2]:
                self._definir_imagem(self.cache, 'interrogacao', 'pequenas')
            self._professor_texto.set_text(self.cache)

    def _nivel_alterado(self, widget):
        """Método que altera o nível dos jogos de palavras."""
        jogo_id = self.jogo_escolhido + widget.get_active_id()
        if jogo_id in ("12", "22"):
            for letra in jogo1:
                self._definir_imagem(letra, "interrogacao", "pequenas_red")
            self._definir_imagem(self.cache, "interrogacao", "pequenas")
        else:
            for letra in jogo1:
                self._definir_imagem(letra, "normais")
            self._definir_imagem(self.cache, "interrogacao", "pequenas")

    def _remover_palavra_funcao(self, widget):
        """Método que adiciona a palavra na lista negativa do arquivo palavras_erradas.txt."""
        palavra = self._obter_texto('professor')
        if palavra not in palavras_erradas:
            palavras_erradas.append(palavra)
            with open("palavras_erradas.txt", "a") as file:
                file.write(palavra + "\n")
        # é obrigatório chamar o self.aluno_digitando antes do professor_texto
        # senão gera um bug
        self.aluno_digitando(self._aluno_texto)
        self._professor_texto.set_text(choice(palavras))
        self.aluno_digitando(self._aluno_texto)


def main():
    app = Janela()  # noqa
    Gtk.main()
