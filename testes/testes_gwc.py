"""gnome write correctly testes."""


from unittest import main, TestCase
from gwc import *


class Testes(TestCase):
    app = Janela()
    prof = app._professor_texto
    aluno = app._aluno_texto

    def teste_texto_aluno_replicado(self):
        self.prof.set_text('ola')
        self.aluno.set_text('ola')
        self.assertEqual(self.prof.get_text(self.prof.get_start_iter(),
                                       self.prof.get_end_iter(), False), '')

    def teste_auto_apagar(self):
        self.app._auto_apagar.set_active(True)
        self.prof.set_text('oi')
        self.aluno.set_text('ola')
        self.assertEqual(self.aluno.get_text(self.aluno.get_start_iter(),
                                             self.aluno.get_end_iter(),
                                             False), 'o')
        self.app._auto_apagar.set_active(False)
        self.prof.set_text('')
        self.aluno.set_text('')

    def teste_mostar_imagem(self):
        self.app.mostrar_imagem(0)
        self.assertEqual(self.app._maos.is_visible(), True)
        self.app.mostrar_imagem(0)
        self.assertEqual(self.app._maos.is_visible(), False)

    def teste_funcao_colorir(self):
        self.assertEqual(colorir('olá meu amigo', 1),
                         'olá <span color="green1">meu</span> amigo')
        self.assertEqual(colorir('olá meu amigo', 2, 'yellow2'),
                         'olá meu <span color="yellow2">amigo</span>')
        self.assertEqual(colorir('olá meu amigo', 0, 'orange'),
                         '<span color="orange">olá</span> meu amigo')

    def teste_funcao_dr(self):
        self.assertEqual(list(dr('á')), ['agudo', 'a'])
        self.assertEqual(dr('['), 'colchete_esquerdo')
        self.assertEqual(list(dr('à')), ['agudo', 'a'])
        self.assertEqual(list(dr('{')), ['colchete_esquerdo'])

    def teste_popup_dedos_corretos(self):
        self.prof.set_text('a')
        self.assertEqual(self.app._poplabel.get_text(), 'dedo: 1')
        self.prof.set_text('o')
        self.assertEqual(self.app._poplabel.get_text(), 'dedo: 2')
        self.prof.set_text('i')
        self.assertEqual(self.app._poplabel.get_text(), 'dedo: 3')
        self.prof.set_text('')
        self.app._poplabel.set_text('')
        self.app._popover.hide()

    def teste_popup_visivel(self):
        self.prof.set_text('a')
        self.assertEqual(self.app._popover.is_visible(), True)
        self.app._poplabel.set_text('')
        self.app._popover.hide()

    def teste_popup_not_visible(self):
        self.prof.set_text('oi')
        self.aluno.set_text('ola')
        self.assertEqual(self.app._popover.is_visible(), False)
        self.prof.set_text('')
        self.aluno.set_text('')

    def teste_arquivo(self):
        texto_teste = 'as aventuras de um programador testeiro'
        self.app._arquivo.set_filename('testes/texto_teste.txt')
        self.app.arquivo_escolhido(self.app._arquivo)
        self.assertEqual(self.app.texto, [])
        texto_professor = self.prof.get_text(self.prof.get_start_iter(),
                                             self.prof.get_end_iter(), False)
        self.assertEqual(texto_professor, texto_teste)
        self.aluno.set_text(texto_teste)

    def teste_remover_arquivo(self):
        self.app._arquivo.set_filename('testes/texto_teste.txt')
        self.app.arquivo_escolhido(self.app._arquivo)
        self.app.remover_arquivo(self.app._limpar_arquivo)
        self.assertEqual(self.app._arquivo.get_filename(), None)

    def teste_imagens_brancas_vermelhas_e_normais(self):
        pass

    def teste_shift_direito_esquerdo(self):
        pass


if __name__ == '__main__':
    main()
