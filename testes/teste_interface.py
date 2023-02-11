from unittest import TestCase
from unittest.mock import patch
from gwc.gwc import Janela
from tkinter import mainloop
import platform
from pathlib import Path
from gwc.gwc import persistencia


class TestInterface(TestCase):
    @classmethod
    def tearDownClass(cls):
        if platform.system() == 'Linux':
            save = Path('save.pkl')
            if save.exists():
                save.unlink()

    def setUp(self):
        self.persistencia = persistencia
        self.interface = Janela()
    
    def tearDown(self):
        for key in self.persistencia:
            del self.persistencia[key]
        self.interface.destroy()
    
    def test_jogo_4_sendo_alterado_para_nenhum_e_retornando_de_onde_parou(self):
        self.interface.combobox_jogos.current(4)
        self.interface.jogo_alterado(None)
        esperado = self.interface._obter_texto('professor')
        self.interface.combobox_jogos.current(0)
        self.interface.jogo_alterado(None)
        self.interface.combobox_jogos.current(4)
        self.interface.jogo_alterado(None)
        resultado = self.interface._obter_texto('professor')
        self.assertEqual(esperado, resultado)
    
    def test_jogo_4_sendo_alterado_para_adivinhe_a_tecla_e_retornando_de_onde_parou(self):
        self.interface.combobox_jogos.current(4)
        self.interface.jogo_alterado(None)
        esperado = self.interface._obter_texto('professor')
        self.interface.combobox_jogos.current(1)
        self.interface.jogo_alterado(None)
        self.interface.combobox_jogos.current(4)
        self.interface.jogo_alterado(None)
        resultado = self.interface._obter_texto('professor')
        self.assertEqual(esperado, resultado)
    
    def test_jogo_4_sendo_alterado_para_digite_a_palavra_e_retornando_de_onde_parou(self):
        self.interface.combobox_jogos.current(4)
        self.interface.jogo_alterado(None)
        esperado = self.interface._obter_texto('professor')
        self.interface.combobox_jogos.current(2)
        self.interface.jogo_alterado(None)
        self.interface.combobox_jogos.current(4)
        self.interface.jogo_alterado(None)
        resultado = self.interface._obter_texto('professor')
        self.assertEqual(esperado, resultado)
    
    def test_jogo_4_sendo_alterado_para_treinar_acentos_e_retornando_de_onde_parou(self):
        self.interface.combobox_jogos.current(4)
        self.interface.jogo_alterado(None)
        esperado = self.interface._obter_texto('professor')
        self.interface.combobox_jogos.current(3)
        self.interface.jogo_alterado(None)
        self.interface.combobox_jogos.current(4)
        self.interface.jogo_alterado(None)
        resultado = self.interface._obter_texto('professor')
        self.assertEqual(esperado, resultado)
    
    def test_jogo_4_sendo_alterado_para_ele_mesmo_e_retornando_de_onde_parou(self):
        self.interface.combobox_jogos.current(4)
        self.interface.jogo_alterado(None)
        esperado = self.interface._obter_texto('professor')
        self.interface.combobox_jogos.current(4)
        self.interface.jogo_alterado(None)
        resultado = self.interface._obter_texto('professor')
        self.assertEqual(esperado, resultado)
    
    def test_jogo_4_replicando_o_mesmo_texto_do_professor_no_aluno_e_texto_do_professor_sendo_alterado(self):
        self.interface.combobox_jogos.current(4)
        self.interface.jogo_alterado(None)
        esperado = self.interface._obter_texto('professor')
        self.interface._text_aluno.insert(1.0, esperado)
        self.interface._jogo(None)
        resultado = self.interface._obter_texto('professor')
        self.assertNotEqual(esperado, resultado)
    
    def test_jogo_4_replicando_texto_do_professor_e_alternando_entre_jogos_e_replicando_texto_do_professor(self):
        self.interface.combobox_jogos.current(4)
        self.interface.jogo_alterado(None)
        texto = self.interface._obter_texto('professor')
        self.interface._text_aluno.insert(1.0, texto)
        self.interface._jogo(None)
        texto = self.interface._obter_texto('professor')
        self.interface._text_aluno.insert(1.0, texto)
        self.interface._jogo(None)
        self.interface.combobox_jogos.current(0)
        self.interface.jogo_alterado(None)
        self.interface.combobox_jogos.current(4)
        self.interface.jogo_alterado(None)
        nao_esperado = self.interface._obter_texto('professor')
        self.interface._text_aluno.insert(1.0, nao_esperado)
        self.interface._jogo(None)
        resultado = self.interface._obter_texto('professor')
        self.assertNotEqual(nao_esperado, resultado)
    
    def test_jogo_4_inserindo_um_novo_texto_caso_o_antigo_seja_replicado_pelo_aluno(self):
        self.interface.combobox_jogos.current(4)
        self.interface.jogo_alterado(None)
        nao_esperado = self.interface._obter_texto('professor')
        self.interface._text_aluno.insert(1.0, nao_esperado)
        self.interface._jogo(None)
        resultado = self.interface._obter_texto('professor')
        self.assertNotEqual(nao_esperado, resultado)
    
    def test_jogo_4_salvando_o_jogo_e_continuando_de_onde_parou_caso_o_programa_seja_fechado_e_reaberto(self):
        self.interface.combobox_jogos.current(4)
        self.interface.jogo_alterado(None)
        texto = self.interface._obter_texto('professor')
        self.interface._text_aluno.insert(1.0, texto)
        self.interface._jogo(None)
        esperado = self.interface._obter_texto('professor')
        self.interface.salvar_estado_jogo_4()
        self.interface.destroy()
        self.interface = Janela()
        self.interface.combobox_jogos.current(4)
        self.interface.jogo_alterado(None)
        resultado = self.interface._obter_texto('professor')
        self.assertEqual(esperado, resultado)
