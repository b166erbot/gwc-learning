from pathlib import Path
from random import shuffle


def pegar_ultimo_nome() -> int:
    local = Path('textos')
    arquivos = list(local.glob('*.texto'))
    nomes = [
        int(arquivo.name.replace('.texto', '')) for arquivo in arquivos
    ]
    return max([0] + nomes)


def main():
    arquivo_original = Path('textos/palavras_nao_treinadas.txt')
    with arquivo_original.open() as arquivo:
        texto = arquivo.readlines()
    shuffle(texto)
    nome = pegar_ultimo_nome() + 1
    nome = f"{nome}.texto"
    novo_arquivo = Path('textos/' + nome)
    with novo_arquivo.open('w') as arquivo:
        arquivo.write(''.join(texto))
    print(f"fim. você já pode abrir o arquivo: {novo_arquivo.absolute()}")


if __name__ == '__main__':
    main()
