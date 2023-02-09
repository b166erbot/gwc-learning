from random import choices


def cortar(lista, numero):
    return [lista[x: numero + x] for x in range(0, len(lista) - 1)]


def fazer_string_de_treinamento(conjunto):
    return ' '.join(
        [''.join(choices(conjunto, k=4)) for _ in range(4)]
    )