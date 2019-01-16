from threading import Thread


class Jogo2(Thread):
    def __init__(self, *args):
        Thread.__init__(self)
        self.self2 = ''
        self.args = args

    def run(self):
        if self.self2:
            self.self2._jogo2(*self.args)

    def iniciar(self):
        self.start()
        self.join()


class App(Thread):
    def __init__(self, objeto):
        Thread.__init__(self)
        self.objeto = objeto

    def run(self):
        self.objeto()

    def iniciar(self):
        self.start()
        self.join()
