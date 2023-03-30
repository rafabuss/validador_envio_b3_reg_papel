RED     = "\033[1;31m"  
BLUE    = "\033[1;34m"
CYAN    = "\033[1;36m"
GREEN   = "\033[0;32m"
RESET   = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

def TamanhoCampo(var):
    return len(var)

def NumberOrString(v):
    new1 = v.replace(" ", "_")
    print('Valor original: ' + new1)
    new = v.replace(" ", "")
    print('Valor sem espaços: ' + new)
    
    if new.isalpha():
        return 'Alpha'
    elif new.isnumeric():
        return 'Numeric'
    elif new.isalnum():
        return 'Alphanumeric'
    elif new.count(" ") == 0:
        return 'Space'
    else:
        return 'N/I'

def ValidaTipoCampo(valor, tipo, requiredDefault):
    global qtderro
    TipoAvaliado = NumberOrString(valor)
    if ((requiredDefault == True) and (TipoAvaliado == tipo)) or ((requiredDefault == False) and ((TipoAvaliado == 'Space') or (TipoAvaliado == tipo))):
        print('Tipo de campo (' + tipo + ') CORRETO')
    else:
        print('Tipo de campo ' + BOLD + RED + 'INCORRETO' + RESET)
        qtderro = qtderro + 1

def ValidaTamanho(xcaracteres, tamanho, espacos):
    global qtderro
    #print(xcaracteres,tamanho)
    if str(xcaracteres) == str(tamanho):
        print('Tamanho do campo (' + str(tamanho) + ') CORRETO')
    elif str(xcaracteres + espacos) == str(tamanho):
        print('Tamanho do campo (preenchidos: "' + str(xcaracteres) + '" + espaços em branco :"' + str(espacos) + '") está CORRETO')
    else:
        print('Tamanho do campo está ' + BOLD + RED + 'INCORRETO: ' + RESET + 'Campo - ' + str(xcaracteres + espacos) + '; Tamanho esperado - ' + str(tamanho))
        qtderro = qtderro + 1

def ErroPreenchimento(tipoif,campo,campovalor):
    global qtderro
    qtderro = qtderro + 1 
    print('- Validado que é ' + tipoif + ', porém o valor para "' + campo + '" não é padrão (' + campovalor + ')')
    print('  Atributo "' + campo + '" está preenchido' + BOLD + RED + ' INCORRETAMENTE' + RESET + ' (' + campovalor + ')!')

def PreenchimentoCorreto(tipoif,campo,campovalor):
    print('- Validado que é ' + tipoif + ' e o valor preenchido é ' + campovalor)
    print('  Atributo "' + campo + '" está preenchido CORRETAMENTE')

def RegistraAcao(campo, campovalor):
    global acao
    global tipoif
    global qtdemitida
    global vluntemissao
    global CConversaoExtincao
    match campo:
        case 'Acao':
            acao = campovalor
        case 'TipoIF':
            tipoif = campovalor
        case 'QuantidadeEmitida':
            qtdemitida = campovalor
        case 'ValorUnitariodeEmissao':
            vluntemissao = campovalor
        case 'ClausuladeConversaoExtincao': 
            CConversaoExtincao = campovalor

def ValidaCampoObrigatorio(campo, valor, requiredDefault):
    global qtderro
    Obrigatorio = True
    CodigoIf = ((campo == 'CodigoIF') and (acao in ('ALTR','DDCP','ATUA')))
    DatadeVencimento = ((campo == 'DatadeVencimento') and (tipoif != 'LFSC'))
    PrazodeEmissao = ((campo == 'PrazodeEmissao') and (tipoif != 'LFSC'))
    Escalonamento = ((campo == 'Escalonamento') and (tipoif in ('CDB','CDBS','CDBV','LF','LFV')))
    CondicaodeResgateAntecipado = ((campo == 'CondicaodeResgateAntecipado') and (tipoif not in ('LF','LFSC','LFSN','DIR','DIRG','DIRP','DIRR','DIRA','DIRB','DIRC','DPGE')))
    DistribuicaoPublica = ((campo =='DistribuicaoPublica') and (tipoif in ('LF','LFSC','LFSN')))
    OpcaodeRecompraResgateEmissor = ((campo =='OpcaodeRecompraResgateEmissor') and (tipoif in ('LFSC','LFSN')))
    ClausuladeConversaoExtincao = ((campo =='ClausuladeConversaoExtincao') and (tipoif in ('LFSC','LFSN')))
    LimiteMaximodeConversibilidade = ((campo =='LimiteMaximodeConversibilidade') and (CConversaoExtincao == 'C'))
    CriteriosparaConversao = ((campo =='CriteriosparaConversao') and (CConversaoExtincao == 'C'))

    if requiredDefault == False:
        Obrigatorio = False
        if CodigoIf or DatadeVencimento or PrazodeEmissao or Escalonamento or CondicaodeResgateAntecipado or DistribuicaoPublica or OpcaodeRecompraResgateEmissor or ClausuladeConversaoExtincao or LimiteMaximodeConversibilidade or CriteriosparaConversao:
            Obrigatorio = True
    if Obrigatorio == True:
        print('- Validado obrigatoriedade de preenchimento:')       
        if len(valor.replace(" ", "")) == 0:
            print('  Atributo "' + campo + '" está NULO' + BOLD + RED + ' INCORRETAMENTE' + RESET )
            qtderro = qtderro + 1
        else:
            print('  Campo Obrigatório PREENCHIDO')
    return Obrigatorio

def ValidarValorFinanceirodeResgate(campo, campovalor):
    global qtderro
    ValorFinanceirodeResgatePreenchido = (campo == 'ValorFinanceirodeResgate') and (len(campovalor) != 0)
    ValorFinanceirodeResgateNulo = (campo == 'ValorFinanceirodeResgate') and (len(campovalor) == 0)
    if ValorFinanceirodeResgatePreenchido and (tipoif in ('LF','LFV','LFSC','LFSN')):
        #print(ValorFinanceirodeResgatePreenchido, str((tipoif in ('LF','LFV','LFSC','LFSN'))==True))
        print('Atributo ' + campo + BOLD + RED + ' deveria estar nulo' + RESET)
        print(campo + ': ' + campovalor)
        print('Preenchimento (' + str(len(campovalor)) + ') ' + BOLD + RED + 'INCORRETO' + RESET)
        qtderro = qtderro + 1
    elif ValorFinanceirodeResgatePreenchido:
        print('Atributo ' + campo + ' está preenchido CORRETAMENTE')
    elif ValorFinanceirodeResgateNulo:
        print('Atributo "' + campo + '" está nulo CORRETAMENTE') 

def ValidaEscalonamento(campo, campovalor):
    global qtderro
    regra1 = (tipoif in ('CDB','CDBS','CDBV','LF','LFV')) and (len(campovalor) != 0)
    regra2 = (tipoif not in ('CDB','CDBS','CDBV','LF','LFV')) and (len(campovalor) == 0)
    erro = (tipoif not in ('CDB','CDBS','CDBV','LF','LFV')) and (len(campovalor) != 0)
    if campo == 'Escalonamento':
        if regra1: 
            if campovalor == 'T':
                print('- Validado que é ' + tipoif + ' e o valor preenchido é ' + campovalor)
                print('  Atributo "' + campo + '" está preenchido CORRETAMENTE')
            else:
                print('- Validado que é ' + tipoif + ', porém o valor do Escalonamento preenchido é ' + campovalor)
                print('  Atributo "' + campo + '" está preenchido' + BOLD + RED + ' INCORRETAMENTE' + RESET)
                qtderro = qtderro + 1
        if regra2:
            print('- Validado que é ' + tipoif + ' e o valor está nulo CORRETAMENTE')           
        if erro:
            print('- Validado que é ' + tipoif + ', porém o valor para Escalonamento está preenchido (' + campovalor + ')')
            print('  Atributo "' + campo + '" está preenchido' + BOLD + RED + ' INCORRETAMENTE' + RESET + ', pois deveria estar NULO')
            qtderro = qtderro + 1

def ValidaCondicaodeResgateAntecipado(campo, campovalor, requiredDefault):
    global qtderro
    regra = ((requiredDefault) and (campovalor in ('S','N','M')))
    erro = ((requiredDefault) and (campovalor not in ('S','N','M')) and (len(campovalor) != 0))
    if (campo == 'CondicaodeResgateAntecipado'):
        if regra:
            print('- Validado que é ' + tipoif + ' e o valor preenchido é ' + campovalor)
            print('  Atributo "' + campo + '" está preenchido CORRETAMENTE')
        elif erro: 
            print('- Validado que é ' + tipoif + ', porém o valor para "CondicaodeResgateAntecipado" não é padrão (' + campovalor + ')')
            print('  Atributo "' + campo + '" está preenchido' + BOLD + RED + ' INCORRETAMENTE' + RESET + ' (' + campovalor + '), pois deveria ter um dos valores a seguir: S,N,M')
            qtderro = qtderro + 1   

def ValidaFormadePagamento(campo, campovalor, tipoif):
    global qtderro
    ErroRegra1 = ((tipoif in ('LF','LFS','LFV')) and (campovalor not in ('01','02','05')))
    ErroRegra2 = ((tipoif in ('CDB','CDBV','DI','DII','DIM','DIR','DIRG','DIRP','DIRR','DIRA','DIRB','DIRC','DPGE','LE','RDB')) and (campovalor not in ('01','02','03','04','05','06','12')))
    ErroRegra3 = ((tipoif == "LFSN") and (campovalor not in ('01','02','05','14','15')))
    ErroRegra4 = ((tipoif == "LFSC") and (campovalor not in ('13','14','15')))
    if ErroRegra1 or ErroRegra2 or ErroRegra3 or ErroRegra4:
        ErroPreenchimento(tipoif,campo,campovalor)
        match tipoif:
            case tipoif if tipoif in ['CDB','CDBV','DI','DII','DIM','DIR','DIRG','DIRP','DIRR','DIRA','DIRB','DIRC','DPGE','LE','RDB']:
                print('  Valor deveria ser 01, 02, 03, 04, 05, 06 ou 12')
            case tipoif if tipoif in ['LF','LFS','LFV']:
                print('  Valor deveria ser 01, 02, ou 05')
            case 'LFSN':
                print('  Valor deveria ser 01, 02, 05, 14 ou 15')
            case 'LFSC':
                print('  Valor deveria ser 13, 14 ou 15')
    else:
        PreenchimentoCorreto(tipoif,campo,campovalor)

def ValidaRentabilidadeIndexadorTaxa(campo, campovalor, tipoif):
    ErroRegraDolar = ((campovalor == '0015') and (tipoif not in ('LFSC','LFSN')))
    if ErroRegraDolar:
        ErroPreenchimento(tipoif,campo,campovalor)
        print('  Valor ' + campovalor + ' (US$ Com.) é aplicado apenas para LFSC e LFSN')
    else:
        PreenchimentoCorreto(tipoif,campo,campovalor)

def ValidaPeriodicidadedeCorrecao(campo, campovalor, tipoif):
    ErroRegra = ((tipoif == 'LFSC') and (campovalor not in ('M','E')))
    if (campovalor != '') and ErroRegra:
        ErroPreenchimento(tipoif,campo,campovalor)
        print('  Para ' + tipoif + ' o preenchimento deve ser M ou E')

def ValidaDistribuicaoPublica(campo, campovalor, tipoif):
    ErroRegra1 = ((tipoif in ('LF','LFSC','LFSN')) and (campovalor not in ('S','N')))
    ErroRegra2 = ((tipoif not in ('LF','LFSC','LFSN')) and (campovalor != ''))
    if ErroRegra1 or ErroRegra2:
        ErroPreenchimento(tipoif,campo,campovalor)
        print('  Só deve ser preenchido para "LF","LFSC" ou "LFSN", e deve ser "S" ou "N"')
    else:
        PreenchimentoCorreto(tipoif,campo,campovalor)

def ValidaOpcaodeRecompraResgateEmissor(campo, campovalor, tipoif):
    ErroRegra1 = ((tipoif in ('LF','LFV','LFSC','LFSN')) and (campovalor not in ('S','N','')))
    ErroRegra2 = ((tipoif not in ('LF','LFV','LFSC','LFSN')) and (campovalor != ''))
    ErroRegra3 = ((tipoif in ('LFSC','LFSN')) and (campovalor == ''))
    if ErroRegra1 or ErroRegra2 or ErroRegra3:
        ErroPreenchimento(tipoif,campo,campovalor)
        match tipoif:
            case tipoif if tipoif in ['LFSC','LFSN']:
                print('  Para "LFSC" e "LFSN" deve ser preenchido "S" ou "N" somente!')
            case tipoif if tipoif in ['LF','LFV']:
                print('  Para "LFSC", "LFSN", "LFV" e "LF" deve ser preenchido "S", "N" ou nulo somente!')
            case tipoif if tipoif not in ['LF','LFV','LFSC','LFSN']:
                print('  Para "'+ tipoif + '" não deve ser preenchido valor!')
    else:
        PreenchimentoCorreto(tipoif,campo,campovalor)
        
def ValidaClausuladeConversaoExtincao(campo, campovalor, tipoif):
    ErroRegra = ((tipoif in ('LFSC','LFSN')) and (campovalor not in ('C', 'E')))
    if ErroRegra:
        ErroPreenchimento(tipoif,campo,campovalor)
        print('  Para "LFSC" e "LFSN" deve ser preenchido "C" ou "E" somente!')
    else:
        PreenchimentoCorreto(tipoif,campo,campovalor)

def ValidaCampo(campo, nlinha, linha, posicao1, posicao2, tipo, tamanho, requiredDefault):
    global acao 
    global atributo
    atributo = atributo + 1
    print('Validando campo "' + str(atributo) + ' - ' + campo + '" da linha ' + str(nlinha))
    campovalor = linha[posicao1:posicao2]
    requiredDefault = ValidaCampoObrigatorio(campo, campovalor, requiredDefault)
    ValidaTipoCampo(campovalor, tipo, requiredDefault)
    numeroEspacos = campovalor.count(" ")
    ValidaTamanho(TamanhoCampo(campovalor.replace(" ", "")), tamanho, numeroEspacos)
    RegistraAcao(campo, campovalor.replace(" ", ""))
    
    match str(atributo),campo:
        ### regra do atributo 16
        case '16','ValorFinanceirodeResgate':
            ValidarValorFinanceirodeResgate(campo, campovalor.replace(" ", ""))
        ### regra do atributo 18
        case '18','Escalonamento':
            ValidaEscalonamento(campo, campovalor.replace(" ", ""))
        ### regra do atributo 20
        case '20','CondicaodeResgateAntecipado':
            ValidaCondicaodeResgateAntecipado(campo, campovalor, requiredDefault)
        ### regra do atributo 21
        case '21','FormadePagamento':
            ValidaFormadePagamento(campo, campovalor, tipoif)
        ### regra do atributo 22
        case '22','RentabilidadeIndexadorTaxa':
            ValidaRentabilidadeIndexadorTaxa(campo, campovalor, tipoif)
        ### regra do atributo 23
        case '23','PeriodicidadedeCorrecao':
            ValidaPeriodicidadedeCorrecao(campo, campovalor, tipoif)
        ### regra do atributo 76
        case '76','DistribuicaoPublica':
            ValidaDistribuicaoPublica(campo, campovalor, tipoif)
        ### regra do atributo 78
        case '78','OpcaodeRecompraResgateEmissor':
            ValidaOpcaodeRecompraResgateEmissor(campo, campovalor, tipoif)
        ### regra do atributo 79
        case '79','ClausuladeConversaoExtincao':
            ValidaClausuladeConversaoExtincao(campo, campovalor, tipoif)
   

    print('-------')    

def DefiniCampos(linhaatualcampo):
    global desccampo
    global tipocaracter
    global tamanhocampo
    global required
    global posicao1campo
    global posicao2campo
    desccampo = linhaatualcampo[3:37].replace(" ", "")
    tipocaraccampo = linhaatualcampo[37:39].replace(" ", "")
    tamanhocampo = linhaatualcampo[40:43].replace(" ", "")
    required = linhaatualcampo[45:46].replace(" ", "")
    posicao1campo = int(linhaatualcampo[47:53].replace(" ", ""))
    posicao2campo = int(linhaatualcampo[54:63].replace(" ", ""))
    match tipocaraccampo:
        case 'X':
            tipocaracter = 'Alpha'
        case 'X1':
            tipocaracter = 'Alphanumeric'
        case '9':
            tipocaracter = 'Numeric'
    if required == 'S':
        required = True
    else:
        required = False
        
####   Início das avaliações   ####

print('######VALIDAÇÃO DO ARQUIVO######')
print('')

## Lê arquivo com a declaração dos campos
arqcampos = open("Campos.txt")
linhasCampos = arqcampos.readlines()
##

## Lê arquivo exportado pelo sistema
arq = open("TESTE.txt")
linhas = arq.readlines()
nlinha = 0
qtderro = 0
for linhaatual in linhas:
    if linhaatual != linhas[0]:
        atributo = 0
        nlinha = nlinha + 1
        print('')
        print('#### VALIDANDO LINHA ' + str(nlinha) + ' ####')
        print('')
        print('Linha do arquivo:')
        print(linhaatual)
        print('--------------------')
        ## Inicia validação de cada campo/atributo da linha
        for campoatual in linhasCampos:
            DefiniCampos(campoatual)
            ValidaCampo(desccampo,nlinha,linhaatual,posicao1campo,posicao2campo,tipocaracter,tamanhocampo,required)
        ##
        print('--------------------') 
##

print('Quantidade de erros encontrados: ' + BOLD + RED + str(qtderro) + RESET)