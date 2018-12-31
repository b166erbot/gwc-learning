#!/usr/bin/python3.6
from os import getcwd
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


# 'sh': 'shift_esquerdo',
d = {' ': 'espaço', '/': 'barra_direita', '\\': 'barra_esquerda',
     '|': ['\\'], '?': ['/'],
     '[': 'colchete_esquerdo', ']': 'colchete_direito', '\n': 'enter',
     '{': ['['], '}': [']'],
     '.': 'ponto', ';': 'ponto_virgula', ',': 'virgula', "'": 'aspas',
     '>': ['.'], ':': [';'], '<': [','], '"': ["'"],
     'ã': ['til', 'a'], 'õ': ['til', 'o'], 'â': ['til', 'a'],
     'ê': ['til', 'e'], 'ô': ['til', 'o'], '=': 'igual',
     'á': ['agudo', 'a'], 'é': ['agudo', 'e'], 'í': ['agudo', 'i'],
     'ó': ['agudo', 'o'], 'ú': ['agudo', 'u'], '+': ['='],
     'à': ['agudo', 'a'], '_': ['-'], '-': 'menos',
     '!': ['1'], '@': ['2'], '#': ['3'], '$': ['4'],
     '%': ['5'], '¨': ['6'], '&': ['7'], '*': ['8'],
     '(': ['9'], ')': ['0']
     }

right_shift = '\'12345qwertasdfg\\zxcvb'
left_shift = '67890-=yuiophjklçnm,.;/~]´['
dedos = ['\'1qaz\\', '2wsx', '3edc', '45rtfgvb', '0pç;/~^´`-_=+[]{}\n', '9ol.',
         '8ik,', '67yuhjnm']


def RD(item):
    """
    Função de recursividade que retorna um gerador do dicionário d.
    """
    if isinstance(item, str) and item.lower() in d:
        if item.isupper():
            return (*RD(d.get(item.lower(), item.lower())), 'shift_esquerdo')
        return RD(d.get(item.lower(), item.lower()))
    elif isinstance(item, str):
        return item
    return (RD(a.lower()) for a in item)


def colorir(texto, posicao, cor='green1'):
    """
    Função que colore um texto em uma determinada posição.
    """
    texto = texto.split()
    texto[posicao] = f'<span color="{cor}">{texto[posicao]}</span>'
    return ' '.join(texto)


class Janela:
    def __init__(self):
        # criando objetos.
        self._apagar = False
        self.cache = ''
        self.red_cache = ''
        self.prof_cache = ''
        self.builder = Gtk.Builder()
        self.local = getcwd()
        self.texto = ''
        self.n_word_cache = -1

        # obtendo a interface glade
        self.builder.add_from_file('datilografia.glade')

        # obtendo objetos.
        self._janela = self.builder.get_object('janela')
        self._0 = self.builder.get_object('zero')
        self._1 = self.builder.get_object('um')
        self._2 = self.builder.get_object('dois')
        self._3 = self.builder.get_object('tres')
        self._4 = self.builder.get_object('quatro')
        self._5 = self.builder.get_object('cinco')
        self._6 = self.builder.get_object('seis')
        self._7 = self.builder.get_object('sete')
        self._8 = self.builder.get_object('oito')
        self._9 = self.builder.get_object('nove')
        self._agudo = self.builder.get_object('agudo')
        self._alt_direito = self.builder.get_object('alt-direito')
        self._alt_esquerdo = self.builder.get_object('alt-esquerdo')
        self._a = self.builder.get_object('a')
        self._aspas = self.builder.get_object('aspas')
        self._backspace = self.builder.get_object('backspace')
        self._barra_direita = self.builder.get_object('barra-direita')
        self._barra_esquerda = self.builder.get_object('barra-esquerda')
        self._b = self.builder.get_object('b')
        self._capslock = self.builder.get_object('capslock')
        self._colchete_direito = self.builder.get_object('colchete-direito')
        self._colchete_esquerdo = self.builder.get_object('colchete-esquerdo')
        self._control_direito = self.builder.get_object('control-direito')
        self._control_esquerdo = self.builder.get_object('control-esquerdo')
        self._c = self.builder.get_object('c')
        self._ç = self.builder.get_object('ç')
        self._d = self.builder.get_object('d')
        self._enter = self.builder.get_object('enter')
        self._e = self.builder.get_object('e')
        self._esc = self.builder.get_object('esc')
        self._espaço = self.builder.get_object('espaço')
        self._f10 = self.builder.get_object('f10')
        self._f11 = self.builder.get_object('f11')
        self._f12 = self.builder.get_object('f12')
        self._f1 = self.builder.get_object('f1')
        self._f2 = self.builder.get_object('f2')
        self._f3 = self.builder.get_object('f3')
        self._f4 = self.builder.get_object('f4')
        self._f5 = self.builder.get_object('f5')
        self._f6 = self.builder.get_object('f6')
        self._f7 = self.builder.get_object('f7')
        self._f8 = self.builder.get_object('f8')
        self._f9 = self.builder.get_object('f9')
        self._f = self.builder.get_object('f')
        self._g = self.builder.get_object('g')
        self._h = self.builder.get_object('h')
        self._igual = self.builder.get_object('igual')
        self._i = self.builder.get_object('i')
        self._j = self.builder.get_object('j')
        self._k = self.builder.get_object('k')
        self._l = self.builder.get_object('l')
        self._menos = self.builder.get_object('menos')
        self._menu = self.builder.get_object('menu')
        self._m = self.builder.get_object('m')
        self._n = self.builder.get_object('n')
        self._o = self.builder.get_object('o')
        self._ponto = self.builder.get_object('ponto')
        self._ponto_virgula = self.builder.get_object('ponto-virgula')
        self._p = self.builder.get_object('p')
        self._q = self.builder.get_object('q')
        self._r = self.builder.get_object('r')
        self._shift_direito = self.builder.get_object('shift-direito')
        self._shift_esquerdo = self.builder.get_object('shift-esquerdo')
        self._s = self.builder.get_object('s')
        self._tab = self.builder.get_object('tab')
        self._til = self.builder.get_object('til')
        self._t = self.builder.get_object('t')
        self._u = self.builder.get_object('u')
        self._virgula = self.builder.get_object('virgula')
        self._v = self.builder.get_object('v')
        self._windows_direito = self.builder.get_object('windows-direito')
        self._windows_esquerdo = self.builder.get_object('windows-esquerdo')
        self._w = self.builder.get_object('w')
        self._x = self.builder.get_object('x')
        self._y = self.builder.get_object('y')
        self._z = self.builder.get_object('z')
        self._mostrar_maos = self.builder.get_object('mostrar_maos')
        self._maos = self.builder.get_object('maos')
        self._auto_apagar = self.builder.get_object('auto_apagar')
        self._professor = self.builder.get_object('professor')
        self._aluno_texto = self.builder.get_object('texto_aluno')
        self._professor_texto = self.builder.get_object('texto_professor')
        self._aluno = self.builder.get_object('aluno')
        self._professor = self.builder.get_object('professor')
        self._arquivo = self.builder.get_object('arquivo')
        self._limpar_arquivo = self.builder.get_object('limpar_arquivo')
        self._popover = self.builder.get_object('popover')
        self._poplabel = self.builder.get_object('poplabel')

        # conectando objetos.
        self._janela.connect('destroy', Gtk.main_quit)
        self._mostrar_maos.connect('toggled', self.mostrar_imagem)
        self._aluno_texto.connect('changed', self.aluno_digitando)
        self._professor_texto.connect('changed', self.professor_digitando)
        self._auto_apagar.connect('toggled', self.auto_apagar_clicado)
        self._arquivo.connect('file-set', self.arquivo_escolhido)
        self._limpar_arquivo.connect('clicked', self.remover_arquivo)

        # configurando.
        self._janela.set_title('programa para aprender a digitar')

    def mostrar_imagem(self, widget):
        var = not self._maos.is_visible()
        self._maos.set_visible(var)

    def aluno_digitando(self, widget):
        self._normalizar_imagem()
        prof = self._professor_texto
        texto = widget.get_text(widget.get_start_iter(), widget.get_end_iter(),
                                False)
        texto_professor = prof.get_text(prof.get_start_iter(),
                                        prof.get_end_iter(),
                                        False)
        if texto_professor == texto:
            # apagar e talvez inserir texto do arquivo
            if self.texto:
                prof.set_text(self.texto[0])
                texto_professor = self.texto[0]
                texto = ''
                self.texto.pop(0)
                self.n_word_cache = -1
            else:
                prof.delete(prof.get_start_iter(), prof.get_end_iter())
                if self._arquivo.get_filename():
                    self._arquivo.unselect_file(self._arquivo.get_file())
            widget.set_text('')
        condicoes = [bool(texto_professor),
                     texto.count(' ') <= texto_professor.count(' '),
                     texto_professor.count(' ') > 0,
                     texto.count(' ') != self.n_word_cache]
        if all(condicoes):
            # colorir texto professor
            prof.set_text('')
            prof.insert_markup(prof.get_end_iter(),
                               colorir(texto_professor, texto.count(' ')), -1)
            self.n_word_cache = texto.count(' ')
        if texto_professor.startswith(texto) and texto_professor != texto:
            # imagem branca
            self.cache = texto_professor[len(texto):][0]
            rd = RD(self.cache)
            if isinstance(rd, str):
                self._definir_imagem(rd, 'brancas')
            else:
                for a in rd:
                    self._definir_imagem(a, 'brancas')
        elif not texto_professor.startswith(texto):
            # imagem vermelha
            if texto and self._apagar:
                self._aluno.do_backspace(self._aluno)
            self.red_cache = texto[-1]
            rd = RD(self.red_cache)
            if isinstance(rd, str):
                self._definir_imagem(rd, 'vermelhas')
            else:
                for a in rd:
                    self._definir_imagem(a, 'vermelhas')
            if not self._apagar:
                imagem = f'{self.local}/imagens/brancas/backspace.png'
                self.__dict__['_backspace'].set_from_file(imagem)

    def professor_digitando(self, widget):
        prof = self._professor_texto
        texto_professor = prof.get_text(prof.get_start_iter(),
                                        prof.get_end_iter(),
                                        False)
        if len(texto_professor) == 1:
            self._normalizar_imagem()
            self.cache = self.prof_cache = texto_professor[0]
            rd = RD(self.prof_cache)
            if isinstance(rd, str):
                self._definir_imagem(rd, 'brancas')
            else:
                for a in rd:
                    self._definir_imagem(a, 'brancas')
        elif not texto_professor:
            self._normalizar_imagem()

    def auto_apagar_clicado(self, widget):
        self._apagar = not self._apagar

    def _normalizar_imagem(self):
        if self.cache:
            rd = RD(self.cache)
            if isinstance(rd, str):
                self._definir_imagem(rd, 'normais')
            else:
                for a in rd:
                    self._definir_imagem(a, 'normais')
        if self.red_cache:
            rd = RD(self.red_cache)
            if isinstance(rd, str):
                self._definir_imagem(rd, 'normais')
            else:
                for a in rd:
                    self._definir_imagem(a, 'normais')
            self._definir_imagem('backspace', 'normais')
        if self.prof_cache:
            rd = RD(self.prof_cache)
            if isinstance(rd, str):
                self._definir_imagem(rd, 'normais')
            else:
                for a in rd:
                    self._definir_imagem(a, 'normais')

    def _definir_imagem(self, a, pasta):
        quadro = self.__dict__.get('_' + a.lower(), '')
        if quadro:
            imagem = f'{self.local}/imagens/{pasta}/{a.lower()}.png'
            quadro.set_from_file(imagem)
            if pasta != 'normais':
                texto = ''
                for b in dedos:
                    if a.lower() in b:
                        texto = str(dedos.index(b)%4+1)
                if texto:
                    self._mostrar_popup(quadro, texto)
            else:
                self._popover.hide()
        if a.isupper():
            if a.lower() in right_shift:
                shift = 'direito'
            elif a.lower() in left_shift:
                shift = 'esquerdo'
            quadro = self.__dict__[f'_shift_{shift}']
            imagem = f'{self.local}/imagens/{pasta}/shift_{shift}.png'
            quadro.set_from_file(imagem)

    def arquivo_escolhido(self, widget):
        with open(widget.get_filename(), 'r') as f:
            self.texto = f.readlines()
        self.aluno_digitando(self._aluno_texto)

    def remover_arquivo(self, widget):
        self._arquivo.unselect_file(self._arquivo.get_file())
        # limpar o self.texto, aluno e professor
        self.texto = ''
        prof, aluno = self._professor_texto, self._aluno_texto
        prof.delete(prof.get_start_iter(), prof.get_end_iter())
        aluno.delete(aluno.get_start_iter(), aluno.get_end_iter())
        self._popover.hide()

    def _mostrar_popup(self, tecla, texto):
        self._popover.hide()
        self._poplabel.set_text('dedo: ' + texto)
        self._popover.set_relative_to(tecla)
        self._popover.show()


if __name__ == '__main__':
    app = Janela()
    Gtk.main()


# colorir as mãos quando deve se digitar uma tecla
