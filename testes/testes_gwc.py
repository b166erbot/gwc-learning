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
        self.aluno.set_text('oi')

    def teste_mostar_e_recolher_imagem(self):
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
        # self.assertEqual(colorir('\nola', 0, 'green'),
        #                  '\n<span color="green">ola</span>')
        # não está passando este teste final nem a pal

    def teste_funcao_dr(self):
        self.assertEqual(list(dr('á')), ['agudo', 'a'])
        self.assertEqual(dr('['), 'colchete_esquerdo')
        self.assertEqual(list(dr('à')), ['agudo', 'shift_esquerdo', 'a'])
        self.assertEqual(list(dr('{')), ['shift_esquerdo',
                                         'colchete_esquerdo'])
        self.assertEqual(list(dr('À')), ['agudo', 'shift_esquerdo', 'a'])
        self.assertEqual(list(dr('!')), ['shift_esquerdo', '1'])

    def teste_popup_dedos_corretos(self):
        self.prof.set_text('a')
        self.assertEqual(self.app._poplabel.get_text(), 'dedo: 1')
        self.prof.set_text('O')
        self.assertEqual(self.app._poplabel.get_text(), 'dedo: 2')
        self.prof.set_text('1')
        self.assertEqual(self.app._poplabel.get_text(), 'dedo: 1')
        self.prof.set_text('-')
        self.assertEqual(self.app._poplabel.get_text(), 'dedo: 1')
        self.prof.set_text('_')
        self.assertEqual(self.app._poplabel.get_text(), 'dedo: 1')
        self.prof.set_text('\\')
        self.assertEqual(self.app._poplabel.get_text(), 'dedo: 1')
        self.prof.set_text('\'')
        self.assertEqual(self.app._poplabel.get_text(), 'dedo: 1')
        self.prof.set_text('"')
        self.assertEqual(self.app._poplabel.get_text(), 'dedo: 1')
        self.prof.set_text('')
        self.assertEqual(self.app._popover.is_visible(), False)

    def teste_popup_visivel(self):
        self.prof.set_text('a')
        self.assertEqual(self.app._popover.is_visible(), True)
        self.aluno.set_text('oi')
        self.assertEqual(self.app._popover.is_visible(), True)
        self.aluno.set_text('a')
        self.assertEqual(self.app._popover.is_visible(), False)
        self.app._poplabel.set_text('')

    def teste_popup_nao_visivel(self):
        self.aluno.set_text('asdf')
        self.assertEqual(self.app._popover.is_visible(), False)
        self.prof.set_text('oi')
        self.aluno.set_text('oi')
        self.assertEqual(self.app._popover.is_visible(), False)

    def teste_arquivo(self):
        texto_teste = 'as aventuras de um programador testeiro\n'
        self.assertEqual(self.app._arquivo.get_filename(), None)
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

    # def teste_imagens_brancas_vermelhas_e_normais(self):
    #     pass

    # def teste_shift_direito_esquerdo(self):
    #     pass

    def teste_jogo_alterado_removendo_arquivo(self):
        self.app._arquivo.set_filename('testes/texto_teste.txt')
        self.app.arquivo_escolhido(self.app._arquivo)
        self.app.jogo_alterado(self.app._jogos)
        self.assertEqual(self.app._arquivo.get_filename(), None)
        self.assertEqual(self.app.jogo_escolhido, '0')

    def teste_jogo_alterado_area_arquivo_nao_sensivel(self):
        self.app._jogos.set_active_id('1')
        self.assertEqual(self.app._area_arquivo.is_sensitive(), False)
        self.app._jogos.set_active_id('2')
        self.assertEqual(self.app._area_arquivo.is_sensitive(), False)
        self.app._jogos.set_active_id('0')
        self.assertEqual(self.app._area_arquivo.is_sensitive(), True)

    def teste_jogo_alterado_niveis_visiveis(self):
        self.assertEqual(self.app._jogos.get_active_id(), '0')
        self.app._jogos.set_active_id('1')
        self.assertEqual(self.app._niveis.is_visible(), True)
        self.app._jogos.set_active_id('0')
        self.assertEqual(self.app._niveis.is_visible(), False)

    def teste_jogo_professor_nao_sensivel(self):
        self.app._jogos.set_active_id('1')
        self.assertEqual(self.app._professor.is_sensitive(), False)
        self.app._jogos.set_active_id('2')
        self.assertEqual(self.app._professor.is_sensitive(), False)
        self.app._jogos.set_active_id('3')
        self.assertEqual(self.app._professor.is_sensitive(), False)
        self.app._jogos.set_active_id('0')
        self.assertEqual(self.app._professor.is_sensitive(), True)

    def teste_jogo_caracter_altera_no_acerto(self):
        self.assertEqual(self.app.cache, '')
        self.app._jogos.set_active_id('1')
        cache = self.app.cache
        self.aluno.set_text(self.app.cache)
        self.assertNotEqual(self.app.cache, cache) # not equal é o certo
        self.app._jogos.set_active_id('0')
        self.assertEqual(self.app.cache, '')

    def teste_cache(self):
        self.assertEqual(self.app.cache, '')
        self.prof.set_text('olar')
        self.assertEqual(self.app.cache, '')
        self.aluno.set_text('o')
        self.assertEqual(self.app.cache, 'l')
        self.aluno.set_text('ola')
        self.assertEqual(self.app.cache, 'r')
        self.aluno.set_text('olar')
        self.assertEqual(self.app.cache, '')

    def teste_red_cache(self):
        self.assertEqual(self.app.red_cache, '')
        self.prof.set_text('olar')
        self.assertEqual(self.app.red_cache, '')
        self.aluno.set_text('oi')
        self.assertEqual(self.app.red_cache, 'i')
        self.aluno.set_text('consagrado')
        self.assertEqual(self.app.red_cache, 'o')
        self.aluno.set_text('olar')
        self.assertEqual(self.app.red_cache, '')

    def teste_prof_cache(self):
        self.assertEqual(self.app.prof_cache, '')
        self.prof.set_text('o')
        self.assertEqual(self.app.prof_cache, 'o')
        self.prof.set_text('c')
        self.assertEqual(self.app.prof_cache, 'c')
        self.prof.set_text('e')
        self.assertEqual(self.app.prof_cache, 'e')
        self.prof.set_text('')

    def teste_insercao_de_texto_variado_1(self):
        self.prof.set_text('áàÁÀ \noL´[{Ç^,.')
        self.aluno.set_text('á')
        self.aluno.set_text('áà')
        self.aluno.set_text('áàÁ')
        self.aluno.set_text('áàÁÀ')
        self.aluno.set_text('áàÁÀ\n')
        self.aluno.set_text('áàÁÀ\no')
        self.aluno.set_text('áàÁÀ\noL')
        self.aluno.set_text('áàÁÀ\noL´')
        self.aluno.set_text('áàÁÀ\noL´[')
        self.aluno.set_text('áàÁÀ\noL´[{')
        self.aluno.set_text('áàÁÀ\noL´[{Ç')
        self.aluno.set_text('áàÁÀ\noL´[{Ç^')
        self.aluno.set_text('áàÁÀ\noL´[{Ç^,')
        self.aluno.set_text('áàÁÀ\noL´[{Ç^,.')
        self.aluno.set_text('áàÁÀ\noL´[{Ç^,.<')
        self.aluno.set_text('áàÁÀ\noL´[{Ç^,.<>')
        self.prof.set_text('')
        self.aluno.set_text('')
        self.assertEqual(self.app.cache, self.app.prof_cache)

    def teste_insercao_de_texto_variado_2(self):
        self.prof.set_text('67890-=yuiophjklçnm,.;/~]´[`È')
        self.aluno.set_text('6')
        self.aluno.set_text('67')
        self.aluno.set_text('678')
        self.aluno.set_text('6789')
        self.aluno.set_text('67890')
        self.aluno.set_text('67890-')
        self.aluno.set_text('67890-=')
        self.aluno.set_text('67890-=y')
        self.aluno.set_text('67890-=yu')
        self.aluno.set_text('67890-=yui')
        self.aluno.set_text('67890-=yuio')
        self.aluno.set_text('67890-=yuiop')
        self.aluno.set_text('67890-=yuioph')
        self.aluno.set_text('67890-=yuiophj')
        self.aluno.set_text('67890-=yuiophjk')
        self.aluno.set_text('67890-=yuiophjkl')
        self.aluno.set_text('67890-=yuiophjklç')
        self.aluno.set_text('67890-=yuiophjklçn')
        self.aluno.set_text('67890-=yuiophjklçnm')
        self.aluno.set_text('67890-=yuiophjklçnm,')
        self.aluno.set_text('67890-=yuiophjklçnm,.')
        self.aluno.set_text('67890-=yuiophjklçnm,.;')
        self.aluno.set_text('67890-=yuiophjklçnm,.;/')
        self.aluno.set_text('67890-=yuiophjklçnm,.;/~')
        self.aluno.set_text('67890-=yuiophjklçnm,.;/~]')
        self.aluno.set_text('67890-=yuiophjklçnm,.;/~]´')
        self.aluno.set_text('67890-=yuiophjklçnm,.;/~]´[`')
        self.aluno.set_text('67890-=yuiophjklçnm,.;/~]´[`È')
        self.prof.set_text('')
        self.aluno.set_text('')
        self.assertEqual(self.app.cache, self.app.prof_cache)


if __name__ == '__main__':
    main()
