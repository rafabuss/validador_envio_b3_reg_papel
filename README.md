# Validador de arquivo de envio para B3, para registrar CDB/CDBS/CDBV/DI/DII/DIM/DIR/DIRG/DIRP/DIRR/DIRA/DIRB/DIRC/DPGE/LC/ LF/LFS/LFSC/LFSN/LFV/RDB
Valida as posições e valores dos atributos no arquivo, com base no layout fornecido pela B3.

## Pré-requisitos
* Python instalado:

Abrir o CMD e executar:
```
c:>python --version
```
Se o python estiver instalado, aparecerá um texto como o abaixo:

```
Python 3.11.0
```

## Configuração do "Validador":
O projeto possui um arquivo que estipula os atributos e suas posições, com base no layout da fornecido pela B3. O arquivo "Campos.txt" lista a ordem dos atributos, sua descrição, o tipo de preenchimento, se é obrigatório ou não, a quantidade de caractere e a posição.

Veja em detalhes abaixo:

* O número da ordem do campo
   * Ex.: 04
* A descrição do campo
   * Ex.: Codigo IF
* O tipo de campo: 
   * X - string | X1 - alphanumeric | 9 - numeric
* O tamanho do campo
   * Ex.: ( 14)
* Obrigatoriedade do preenchimento do campo no arquivo de envio:
   * (S ou N)
* A posição deste campo na linha do arquivo (primeira e última posição)
   * Ex.: 10      24

Cada informação está em uma posição especifica neste txt, por isso, caso seja necessário incluir algum valor ou alterar, as posições devem ser preservadas.

Exemplo de parte do arquivo:
```
01 Tipo IF                           X (  5) N 0       5    
02 Tipo de Registro                  9 (  1) N 5       6    
03 Acao                              X (  4) N 6       10   
04 Codigo IF                         X1( 14) N 10      24   
05 Quantidade de linhas adicionais   9 (  4) S 24      28   
06 Conta do Registrador              9 (  8) N 28      36 
```

## Como rodar o "Validador"?

* Baixar o projeto em arquivo ZIP, ou fazer um clone.
* Se baixou o ZIP, descompactar
* Cole na pasta do projeto (descompactado ou clonado) o arquivo gerado no sistema, para envio no B3.
* Renomeie o arquivo para TESTE.txt
* No CMD, na pasta do projeto, execute:

```
python .\ValidaArquivo.py
```
* Confira o relatório e corrija o que for necessário.