try:
    import json
    import urllib.request
    import socket
    import getmac
    import requests
    import datetime
    import threading
    import multiprocessing
    from platform import platform
except:
    print("Este programa requer Python 3.x e a biblioteca getmac")
    exit(0)

def waitInput(server, t1):
    """Esperará o comando de saída"""
    while True:
        if input("Comando: ") == "sair":
            server.close()
            t1.terminate()
            exit(0)

def startService():
    '''Contém o loop da thread principal do servidor
       que cuidará de receber e configurar as conexões dos clientes'''
    client_list = []
    while True:
        #aceita a conexão de qualquer cliente
        conn, addr = server.accept()
        
        #adiciona a conexão na lista de clientes
        client_list.append(conn)
            
        #Cria uma thread individual para cada cliente
        threading.Thread(target=clientThread, args=(conn, addr, client_list)).start()
    conn.close()

def clientThread(conn, addr, client_list):
    '''Thread que controla o fluxo de mensagens do cliente'''
    while True:
        try:
            # recebe a mensagem do cliente
            message = conn.recv(2048).decode()
            if message:
                response = str(get_input(message))

                # caso cliente se desconecte
                if response == "exit":
                   remove(conn, client_list)
                   
                # responde a mensagem baseado nos comandos existentes
                conn.send(response.encode())
            else:
                #caso não receba, remove o cliente da lista de clientes
                remove(conn,client_list)
                pass
        except:
            pass

def remove(conn,client_list):
    '''Remove a conexão do cliente da lista de conexões '''
    if conn in client_list:
        client_list.remove(conn)
        conn.close()

def get_ip():
    '''Metodo que retorna o endereço IP do servidor '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # não precisa ser um endereço alcançável
        # pois iremos apenas pegar o endereço IP
        # que este socket utilizou na interface de rede
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except:
        #caso não haja conexão, utilizará o localhost
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_input(message):
    """Metodo usado para tratar uma instrução comando
        Retorna o que será exibido no servidor"""
    #o método identifica o comando e executa a operação correspondente
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
    elif instruction == "/quit":
        return "exit"
    else:
        return "Erro - Comando não encontrado"

def out_server():
    """Método que retornará a saida do comando /server"""
    return "Nome: "+socket.gethostname()

def out_data():
    """Método que retornará a saida do comando /data"""
    month_database = {1:"Janeiro",2:"Fevereiro",3:"Março",4:"Abril",5:"Maio",6:"Junho",7:"Julho",8:"Agosto",9:"Setembro",10:"Outubro",11:"Novembro",12:"Dezembro"}
    date = "Hoje é dia " + str(datetime.datetime.now().day) + " de " + month_database[datetime.datetime.now().month] + " de " + str(datetime.datetime.now().year)
    while (len(date) < 33):
        if len(date) % 2 == 0:
            date += " "
        else:
            date = " " + date
    return date

def out_ip():
    """Funcão que retornará a saida o do comando /ip"""
    return "IP: "+get_ip()

def out_mac():
    """Método que retornará a saida do comando /mac"""
    return "MAC: "+getmac.get_mac_address()

def out_sys():
    """Método que retornará a saida do comando /sys"""
    return "Sistema Operacional: "+platform()

def out_dev():
    """Método que retornará a saida do comando /dev"""
    return 'Desenvolvido por:\n### Êndril "Awak3n" Castilho' \
            '\n### Fernando "Alemão de Troia" Kudrna,' \
            '\n### Leonardo "Darth" Pellegrini'

def out_info():
    """Funcão que retornará a saida o do comando /info"""
    time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
    return  "Informações sobre o sistema\n" \
            "############################################################\n" \
            "####                                                    ####\n" \
            "####"+format_str(show_message()) + "####\n" \
            "####                                                    ####\n" \
            "####"+format_str(out_data())+"####\n" \
            "####                                                    ####\n" \
            "####"+format_str("Hora atual: " + time)+"####\n" \
            "####                                                    ####\n" \
            "####"+format_str("O servidor \'"+ socket.gethostname()+ "\' está funcionando")+"####\n" \
            "####" + format_str("no endereço \'" + get_ip() + "\'") + "####\n" \
            "####                                                    ####\n" \
            "####                 Desenvolvido por:                  ####\n" \
            "####              Êndril \"Awak3n\" Castilho              ####\n" \
            "####         Fernando \"Alemão de Troia\" Kudrna          ####\n" \
            "####            Leonardo \"Darth\" Pellegrini             ####\n" \
            "####                                                    ####\n" \
            "############################################################"

def out_calc(string):
    """Método que retornará a saida do comando /calc"""
    op = string.split(" ")
    operator_list = ["+", "-", "/", "*", "^"]
    try:
        # verifica se o operador é um operador válido
        if op[2] in operator_list:
            # realiza a operação baseada nos valores informados
            if op[2] == "":
                return "Erro - Operador não válido"
            elif op[2] == "+":
                return float(op[1]) + float(op[3])
            elif op[2] == "-":
                return float(op[1]) - float(op[3])
            elif op[2] == "/":
                return float(op[1]) / float(op[3])
            elif op[2] == "*":
                return float(op[1]) * float(op[3])
            elif op[2] == "^":
                return float(op[1]) ** float(op[3])
        else:
            # caso um dos operando não seja numérico, levanta uma exceção
            raise Exception
    except:
        return "Erro - Um ou mais operandos são inválidos"

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
            "            <número> <operação( + - / * ^ )> <número>\n" \
            "/quit       Irá encerrar a conexão. "

def out_bitcoin():
    """Retorna a cotação atual do Bitcoin em dólares"""
    try:
        url = "http://api.coindesk.com/v1/bpi/currentprice.json"
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode('utf-8'))
            valor = float(data['bpi']['USD']['rate'].replace(",", ""))
            return "1 Bitcoin equivale a "+str(valor)+" dólares!"
    except urllib.error.HTTPError:
        print('URL inexistente!')

def show_message():
    """Retorna uma mensagem de saudação baseada no horário atual"""
    time = float(datetime.datetime.now().hour)
    second = float(datetime.datetime.now().second)
    if (time >= 6 and second > 0) and time < 12:
        return " Bom dia! "
    elif (time >= 12 and second > 0) and time <= 19:
        return "Boa tarde!"
    else:
        return "Boa noite!"

def format_str(str):
    """Centraliza uma string do comando /info"""
    while len(str) < 52:
        if len(str) % 2 == 0:
            str += " "
        else:
            str = " " + str
    return str

#inicialização do programa
if __name__ == '__main__':
    #inicializa o socket do servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((get_ip(), 8899))
    server.listen()
    print("##################################")
    print("####                          ####")
    print("####  Servidor inicializado!  ####")
    print("####                          ####")
    print("#### Para finalizar o serviço ####")
    print("####      escreva 'sair'      ####")
    print("####                          ####")
    print("##################################")
    #inicializa o serviço de rede e espera de comando de saída
    t1 = multiprocessing.Process(target=startService)
    t1.start()
    threading.Thread(target=waitInput,args=(server,t1,)).start()

    
