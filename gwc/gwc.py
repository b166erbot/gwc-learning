from random import choice
import re
from json import load
import gi
gi.require_version('Pango', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa
from gi.repository import Pango  # noqa


with open('gwc/teclas.json') as arquivo:
    dicionário = load(arquivo)

# refatorar. mover para outro escopo?
right_shift = 'qwertasdfgzxcvbãáâàêé'
left_shift = 'yuiophjklçnmíõôóú'
lr = right_shift + left_shift
dedos = [
    '\'"1qaz\\|', '2wsx', '3edc', '45rtfgvb', '0pç;:/?~^´`-_=+[]{}\n',
    '9ol>.', '8ik<,', '67yuhjnm'
]
jogo1 = 'abcdefghijklmnopqrstuvxwyzç,.;/~]´[\\'
jogo4 = 'ãêáõôéâíóúà`´~^' + 'ãêáõôéâíóúà'.upper()

with open('palavras.txt', 'r') as f:
    palavras = [a.split() for a in f.readlines()][0]


def colorir(texto, posicao, cor='green1'):
    """
    Função que colore um texto em uma determinada posição.
    """
    texto = list(map(''.join, re.findall(r'(\s*)(\S*)(\s*)', texto)))
    # texto = texto.split(' ')  # não remova o espaço
    texto[posicao] = f'<span color="{cor}">{texto[posicao]}</span>'
    return ''.join(texto)


class Janela:
    def __init__(self):
        # criando objetos.
        pango = Pango.FontDescription('ubuntu 17')
        self._apagar = False
        self.cache = ''
        self.red_cache = ''
        self.prof_cache = ''
        self.builder = Gtk.Builder()
        self.texto = []
        self.n_word_cache = -1
        self.jogo_escolhido = '0'
        self.n_jogos = {'1': self._jogo1, '2': self._jogo2, '3': self._jogo3}

        # obtendo a interface glade.
        self.builder.add_from_file('gwc.glade')

        # obtendo objetos.
        self._janela = self.builder.get_object('janela')
        self._mostrar_maos = self.builder.get_object('mostrar_maos')
        self._maos = self.builder.get_object('maos')
        self._auto_apagar = self.builder.get_object('auto_apagar')
        self._professor = self.builder.get_object('professor')
        self._aluno = self.builder.get_object('aluno')
        self._aluno_texto = self.builder.get_object('texto_aluno')
        self._professor_texto = self.builder.get_object('texto_professor')
        self._arquivo = self.builder.get_object('arquivo')
        self._limpar_arquivo = self.builder.get_object('limpar_arquivo')
        self._popover = self.builder.get_object('popover')
        self._poplabel = self.builder.get_object('poplabel')
        self._jogos = self.builder.get_object('jogos')
        self._niveis = self.builder.get_object('niveis')
        self._area_arquivo = self.builder.get_object('area_arquivo')
        self._area_opcoes = self.builder.get_object('area_opcoes')
        self._niveis_botao = self.builder.get_object('níveis')
        self._printar_palavra = self.builder.get_object('printar_palavra')

        with open('gwc/imagens.json') as arquivo:
            imagens = load(arquivo)
            self.imagens = {
                chave: self.builder.get_object(valor)
                for chave, valor in imagens.items()
            }

        # conectando objetos.
        self._janela.connect('destroy', Gtk.main_quit)
        self._mostrar_maos.connect('toggled', self.mostrar_imagem)
        self._aluno_texto.connect('end-user-action', self.aluno_digitando)
        self._professor_texto.connect(
            'end-user-action', self.professor_digitando
        )
        self._auto_apagar.connect('toggled', self.auto_apagar_clicado)
        self._arquivo.connect('file-set', self.arquivo_escolhido)
        self._limpar_arquivo.connect('clicked', self.remover_arquivo)
        self._jogos.connect('changed', self.jogo_alterado)
        self._niveis_botao.connect('changed', self._nivel_alterado)
        self._printar_palavra.connect(
            'clicked', lambda *x: print(self._obter_texto(True))
        )

        # configurando.
        self._janela.set_title('programa para aprender a digitar')
        self._professor.modify_font(pango)
        self._aluno.modify_font(pango)

    def mostrar_imagem(self, widget):
        self._maos.set_visible(not self._maos.is_visible())

    def aluno_digitando(self, widget):
        prof = self._professor_texto
        texto = self._obter_texto()
        texto_professor = self._obter_texto(True)
        self._normalizar_imagem()
        self._textos_iguais(texto, texto_professor, prof, widget)
        self._imagens(prof, widget)

    def _textos_iguais(self, texto, texto_professor, prof, aluno):
        if texto_professor == texto:
            if self.texto:
                prof.set_text(self.texto[0])
                self.professor_digitando(self._professor_texto)
                texto_professor = self.texto.pop(0)
                self.n_word_cache = -1
            else:
                self.remover_arquivo(None)
                prof.set_text('')
            aluno.set_text('')

    def _imagens(self, prof, aluno):
        texto, texto_professor = self._obter_texto(), self._obter_texto(True)
        if texto_professor.startswith(texto) and texto_professor != texto:
            # imagem branca
            self.cache = texto_professor[len(texto):][0]
            self._definir_imagem(self.cache, 'brancas')
        elif not texto_professor.startswith(texto):
            # imagem vermelha
            if all([texto, self._apagar]):
                self._aluno.do_backspace(self._aluno)
            if texto:
                self._definir_imagem('backspace', 'brancas')
            self.red_cache = texto[-1]
            self._definir_imagem(self.red_cache, 'vermelhas')
        self._colorir_texto(texto_professor, texto)

    def professor_digitando(self, widget):
        texto_professor = self._obter_texto(True)
        if len(texto_professor) == 1 or self.texto:
            self._normalizar_imagem()
            self.cache = self.prof_cache = texto_professor[0]
            self._definir_imagem(self.prof_cache, 'brancas')
        elif not texto_professor:
            self._normalizar_imagem()
            self._popover.hide()
            self._poplabel.set_text('')

    def auto_apagar_clicado(self, widget):
        self._apagar = not self._apagar

    def _normalizar_imagem(self):
        if self.cache:
            self._definir_imagem(self.cache, 'normais')
            self.cache = ''
        if self.red_cache:
            self._definir_imagem(self.red_cache, 'normais')
            self._definir_imagem('backspace', 'normais')
            self.red_cache = ''
        if self.prof_cache:
            self._definir_imagem(self.prof_cache, 'normais')
            self.prof_cache = ''

    # a = letra, c = segundo nome da imagem, caso eu queira outra.
    def _definir_imagem(self, letra, pasta, nomeNaoDicionario=''):
        for imagem in dicionário.get(letra.lower(), letra.lower()):
            quadro = self.imagens.get(imagem)
            if bool(quadro):
                local_imagem = (
                    f'imagens/{pasta}/{nomeNaoDicionario or imagem}.png'
                )
                quadro.set_from_file(local_imagem)
        if pasta == 'brancas':
            self._dedos(letra, imagem, quadro)
        if all([letra.isupper(), letra.lower() in lr]):
            if imagem.lower() in right_shift:
                shift = 'direito'
            elif imagem.lower() in left_shift:
                shift = 'esquerdo'
            quadro = self.imagens.get(f'shift_{shift}')
            imagem = f'imagens/{pasta}/shift_{shift}.png'
            quadro.set_from_file(imagem)

    def _limpar_texto(self, usuario='aluno'):
        # 'aluno', 'professor', 'ambos'
        prof, aluno = self._professor_texto, self._aluno_texto
        if usuario == 'aluno':
            aluno.delete(aluno.get_start_iter(), aluno.get_end_iter())
        elif usuario == 'professor':
            prof.delete(prof.get_start_iter(), prof.get_end_iter())
        elif usuario == 'ambos':
            prof.delete(prof.get_start_iter(), prof.get_end_iter())
            aluno.delete(aluno.get_start_iter(), aluno.get_end_iter())

    def _obter_texto(self, professor=False):
        user = self._professor_texto if professor else self._aluno_texto
        texto = user.get_text(
            user.get_start_iter(), user.get_end_iter(), False
        )
        return texto

    def _dedos(self, letra, imagem, quadro):
        for conjunto in dedos:
            if imagem.lower() in conjunto or letra.lower() in conjunto:
                texto = str(dedos.index(conjunto) % 4 + 1)
                self._mostrar_popup(quadro, texto)
        if letra == ' ':
            self._mostrar_popup(quadro, '5')

    def arquivo_escolhido(self, widget):
        self._limpar_texto('ambos')
        with open(widget.get_filename(), 'r') as f:
            self.texto = f.readlines()
        self.aluno_digitando(self._aluno_texto)

    def remover_arquivo(self, widget):
        if self._arquivo.get_filename():
            self._arquivo.unselect_file(self._arquivo.get_file())
        # limpar o self.texto, aluno, professor e normalizar as imagens
        self._normalizar_imagem()
        self.texto = ''
        self._limpar_texto('ambos')
        self._popover.hide()

    def _mostrar_popup(self, tecla, texto):
        self._popover.hide()
        self._poplabel.set_text(f'dedo: {texto}')
        self._popover.set_relative_to(tecla)
        self._popover.show()

    def jogo_alterado(self, widget):
        self.remover_arquivo(None)
        cache = self.jogo_escolhido
        self.jogo_escolhido = widget.get_active_id()
        self._niveis_botao.set_active_id('0')
        for a in jogo1:
            self._definir_imagem(a, 'normais')
        if self.jogo_escolhido == '0':
            self._aluno_texto.connect('end-user-action', self.aluno_digitando)
            if cache != '0':
                self._aluno_texto.disconnect_by_func(self._jogo)
            self._normalizar_imagem()
            self._niveis.set_visible(False)
            self._professor.set_sensitive(True)
            self._area_arquivo.set_sensitive(True)
            self._area_opcoes.set_sensitive(True)
            self._printar_palavra.set_visible(False)
        else:
            self._aluno_texto.connect('end-user-action', self._jogo)
            if cache == '0':
                self._aluno_texto.disconnect_by_func(self.aluno_digitando)
            self._niveis.set_visible(True)
            self._professor.set_sensitive(False)
            self._area_arquivo.set_sensitive(False)
            self._area_opcoes.set_sensitive(False)
            self._auto_apagar.set_active(False)
            self._mostrar_maos.set_active(False)
            self._printar_palavra.set_visible(True)
            self._jogo(None)  # é preciso chamar a primeira vez

    def _colorir_texto(self, texto_p, texto):
        """ Método que colore um texto em um text_view """
        prof = self._professor_texto
        condicoes = [
            bool(texto_p), texto.count(' ') <= texto_p.count(' '),
            texto_p.count(' ') > 0,
            texto.count(' ') != self.n_word_cache
        ]
        if all(condicoes):
            prof.set_text('')
            generator = map(''.join, re.findall(r'(\s*)(\S*)(\s*)', texto))
            numero = len(list(generator))
            prof.insert_markup(
                prof.get_end_iter(),
                colorir(texto_p, numero - 2), -1
            )
            self.n_word_cache = numero
            # numero <- texto.count(' ')

    def _jogo(self, widget):
        """
        Método que roda os games escolhidos quando algum game é escolhido.
        """
        self.n_jogos[self.jogo_escolhido]()

    def _jogo1(self):
        letra = self._obter_texto()[-1:]  # não remova os pontos
        self._aluno_texto.set_text(letra)
        if letra == self.cache:
            if self._niveis_botao.get_active_id() != '0':
                self._definir_imagem(self.cache, '?', 'pequenas_red')
            else:
                self._normalizar_imagem()
            self.cache = choice(jogo1)
            self._definir_imagem(self.cache, '?', 'pequenas')

    def _jogo2(self):
        self.aluno_digitando(self._aluno_texto)
        if not self._obter_texto(True):
            self._professor_texto.set_text(choice(palavras))
        self.aluno_digitando(self._aluno_texto)

    def _jogo3(self):
        letra = self._obter_texto()[-1:]  # não remova os pontos
        self._aluno_texto.set_text(letra)
        if letra == self.cache:
            self._normalizar_imagem()
            self.cache = choice(jogo4)
            self._definir_imagem(self.cache, 'brancas')
            self._professor_texto.set_text(self.cache)

    def _nivel_alterado(self, widget):
        jogo_id = self.jogo_escolhido + widget.get_active_id()
        if jogo_id == '12':
            for a in jogo1:
                self._definir_imagem(a, '?', 'pequenas_red')
            self._definir_imagem(self.cache, '?', 'pequenas')
        else:
            if self.jogo_escolhido == '1':
                temp = self.cache
                for a in jogo1:
                    self._definir_imagem(a, 'normais')
                self._definir_imagem(temp, '?', 'pequenas')


def main():
    app = Janela()  # noqa
    Gtk.main()
