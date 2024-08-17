# Trabalho Prático 1 - Computação Gráfica
### Alexandre Mendes, Hugo Leonardo

## Instruções para execução

O projeto supõe a pré instalação de python e pip.
As demais dependências do projeto estão localizadas em [requirements.txt](./requirements.txt).
Para fácil instalação das dependências e execução do projeto, pode ser executado o script [run.sh](./run.sh) em um terminal com BASH. (Caso esteja em Windows, pode ser usado o Git BASH do [Git for Windows](https://gitforwindows.org/), por exemplo).

As dependências também podem ser instaladas rodando as linhas do script manualmente, ou por alguma IDE. O código do projeto está localizado em [src/main.py](./src/main.py), e pode ser executado com o comando python main.py no diretório que se encontra este arquivo.

## Descrição
Este programa é capaz de ler um arquivo contendo informações a respeito de objetos a serem desenhados da window e da viewport, desenha tais objetos, e gera um arquivo de saída contendo os objetos no sistema de coordenadas da viewport.
Também é possível inserir novos objetos ao sistema de visualização, sendo possível adicionar um ponto individual, uma reta, ou um polígono qualquer.
Além disso, é possível alterar a window, sendo possível movimentar para cima, baixo, esquerda e direita, rotacionar a esquerda ou a direita, e ampliar e reduzir a window(zoom in e zoom out). Todas as alterações da window são compostas com matrizes de transformações do sistemas de coordenadas do mundo para a janela.