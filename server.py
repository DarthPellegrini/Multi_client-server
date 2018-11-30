try:
    import time
    import json
    import urllib.request
    import socket
    import getmac
    import requests
    import datetime
    import threading
    import multiprocessing
    from platform import platform
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
except:
    print("Este programa requer Python 3.x e as bibliotecas Python-Tk e getmac")
    exit(0)

def waitInput(server,t1):
    while True:
        if input("Comando: ") == "sair":
            server.close()
            t1.terminate()
            exit(0)

def startService():
    while True:
        #aceita a conexão de qualquer cliente
        conn, addr = server.accept()
        
        #adiciona a conexão na lista de clientes
        client_list.append(conn)
        #print (addr[0] + " se conectou")
        
        #Cria uma thread individual para cada cliente
        threading.Thread(target=clientThread, args=(conn, addr)).start()
    conn.close()

def clientThread(conn, addr):
    '''Thread que controla o fluxo de mensagens do cliente'''
    #conn.send("Bem vindo ao servidor!".encode())
    while True:
        try:
            message = conn.recv(2048).decode()    
            if message:
                #print ("<" + addr[0] + "> " + message)
                conn.send(str(get_input(message)).encode())
                #print("aqui")
            else:
                #print("e agora aqui")
                remove(conn)
                return
        except:
            pass

def remove(conn):
    '''Remove a conexão do cliente da lista de conexões '''
    if conn in client_list:
        client_list.remove(conn)
        conn.close()

def get_ip():
    '''Metodo que retorna o endereço IP do servidor '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # não precisa ser alcançável
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_input(message):
    """Metodo usado para tratar uma instrução comando
        Retorna o que será exibido no servidor"""

    #agora pegamos o comando e salvamos numa variavel
    instruction = message.split(" ")[0]
    if instruction == "/server":
        return out_server()
    elif instruction == "/data":
        return out_data()
    elif instruction == "/ip":
        return out_ip()
    elif instruction == "/mac":
        return out_mac()
    elif instruction == "/sys":
        return out_sys()
    elif instruction == "/dev":
        return out_dev()
    elif instruction == "/info":
        return out_info()
    elif instruction == "/bitcoin":
        return out_bitcoin()
    elif instruction == "/calc":
        return out_calc(message)
    elif instruction == "/help":
        return out_help()
    elif instruction == "/omaeWaMouShindeiru":
        return "NANI????"
    else:
        return out_error()

def out_server():
    """Método que retornará a saida do comando /server"""
    return "Nome- "+socket.gethostname()

def out_data():
    """Método que retornará a saida do comando /data"""
    return "Data e hora- "+str(datetime.datetime.now())

def out_ip():
    """Funcão que retornará a saida o do comando /ip"""
    return "IP- "+get_ip()

def out_mac():
    """Método que retornará a saida do comando /mac"""
    return "MAC- "+getmac.get_mac_address()

def out_sys():
    """Método que retornará a saida do comando /sys"""
    return "Sistema Operacional- "+platform()

def out_dev():
    """Método que retornará a saida do comando /dev"""
    return 'Desenvolvido por:\n### Êndril "Awak3n" Castilho' \
            '\n### Fernando "Alemão de Troia" Kudrna,' \
            '\n### Leonardo "Darth" Pellegrini'

def out_info():
    """Funcão que retornará a saida o do comando /info"""
    return  "Informações sobre o sistema\n" \
            "Hora atual "+str(datetime.datetime.now())+"\n" \
            "Servidor rodando no endereço- "+get_ip()+"\n" \
            "Servidor com MAC- "+getmac.get_mac_address()+"\n" \
            "Servidor utilizando o SO- "+platform()+"\n" 

def out_calc(string):
    """Método que retornará a saida do comando /calc"""
    # primeiro vamos remover o /calc da string
    string = string[5:]
    # agora vamos remover todos os espaços em branco antes do primeiro operando se houverem
    while string[0] == " ":
        string = string[1:]
    # definiremos o que são os números aceitos (caracteres)
    is_a_number = ["0","1","2","3","4","5","6","7","8","9",",","."]
    # definiremos as operações conhecidas
    is_a_operator = ["+","-","/","*","^"]
    # retiramos todos os espaços da string se houverem
    string.strip(' ')
    # começaremos agora a lógica de busca dos operandos
    firstOp = True
    op1 = ""
    op2 = ""
    operator = ""
    for caractere in string:
        if caractere in is_a_number:
            if caractere == ",":
                caractere = "."
            if firstOp == True:
                op1 += caractere
            else:
                op2 += caractere
        elif caractere in is_a_operator:
            operator = caractere
            firstOp = False
    # convertemos os operandos para
    try:
        op1 = float(op1)
        op2 = float(op2)
    except:
        return "Erro - Um ou mais operandos são inválidos"
    if operator == "":
        return "Erro - Operador não encontrado"
    elif operator == "+":
        return op1 + op2
    elif operator == "-":
        return op1 - op2
    elif operator == "/":
        return op1 / op2
    elif operator == "*":
        return op1 * op2
    elif operator == "^":
        return op1 ** op2

def out_help():
    return "Informação sobre os comandos disponíveis: \n" \
            "/server     Retorna o nome do servidor\n" \
            "/data       Reotrna a data do sistema do servidor\n" \
            "/ip         Retorna o endereço IP do servidor\n" \
            "/mac        Retorna o endereço MAC do servidor\n" \
            "/sys        Retorna a descrição do sistema operacional do servidor\n" \
            "/dev        Retorna o nome dos desenvolvedores\n" \
            "/info       Retorna mensagens gerais do sistema\n" \
            "/bitcoin    Retorna a cotação de uma bitcoin em dólares\n" \
            "/calc       Retorna o resultado de uma operação algébrica\n" \
            "            <número> <operação( + - / * ^ )> <número>\n"

def out_bitcoin():
    try:
        url = "http://api.coindesk.com/v1/bpi/currentprice.json"
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode('utf-8'))
            valor = float(data['bpi']['USD']['rate'].replace(",", ""))
            return "1 Bitcoin equivale a "+str(valor)+" dólares!"
    except urllib.error.HTTPError:
        print('URL inexistente!')

def out_error():
    """Método que retornará a saida do erro"""
    return "Erro - Comando não encontrado"

#inicialização do programa
if __name__ == '__main__':
    #inicializa o servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((get_ip(), 8899))
    client_list = []
    server.listen()
    print("##################################")
    print("####                          ####")
    print("####  Servidor inicializado!  ####")
    print("####                          ####")
    print("#### Para finalizar o serviço ####")
    print("####      escreva 'sair'      ####")
    print("####                          ####")
    print("##################################")
    t1 = multiprocessing.Process(target=startService)
    t1.start()
    threading.Thread(target=waitInput,args=(server,t1,)).start()

    
