import requests #PRECISA DESSA LIB COMANDO PARA INSTALAR PIP INSTALL E O NOME DA LIB
import json #PRECISA DESSA LIB COMANDO PARA INSTALAR PIP INSTALL E O NOME DA LIB
## dependendo da api não vai ser return em json
import time #PRECISA DESSA LIB COMANDO PARA INSTALAR PIP INSTALL E O NOME DA LIB
import datetime #PRECISA DESSA LIB COMANDO PARA INSTALAR PIP INSTALL E O NOME DA LIB


while True:

    rqs = requests.get('http://api.promasters.net.br/cotacao/v1/valores') #mandando uma requisição em  get para a api

    valoratual = json.loads(rqs.text) #pegando a requisição no formato json e jogando o texto na variavel valoratual

    print('[+]-COMO USAR SUDO CHMOD +x & SUDO CHMOD 777 & ./NOME.PY-[+]') ##um banner de como usar

    print('[+]-Valor atualizado a cada 30 minutos-[+]', datetime.datetime.now())##pegando o tempo mais a baixo explico o porque na função time.sleep

    print(valoratual['valores']['USD']['valor'], 'USD')#pega o retorno json busca a chave valores para pegar o preço do dolar

    print(valoratual['valores']['BTC']['valor'], 'BTC')#pega o retorno json busca a chave valores para pegar o preço do BTC

    print(valoratual['valores']['EUR']['valor'], 'EUR') #pega o retorno json busca a chave valores para pegar o preço do Euro

    time.sleep(2) ## a api so permite 60 requições por minuto isso funciona como um contador que da 1 segundo a mais de  delay assim não da problemas de mais requisições que o permitido pela api