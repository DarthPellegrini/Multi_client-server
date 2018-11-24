try:
    import socket
    import datetime
    import threading
    import requests
    import json
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
except:
    print("Este programa requer Python 3.x e a biblioteca Python-Tk")
    exit(0)

def threaded(function):
    def wrapper(*args, **kwargs):
        threading.Thread(target=function, args=args, kwargs=kwargs).start()
    return wrapper

class Application():
    '''Classe principal'''

    def __init__(self, root):
        '''Construtor da classe, recebe a janela como parâmetro'''
        self.root = root
        self.initComponents()
        self.initServer()
        
    def start(self):
        '''Inicia a aplicação'''
        self.root.mainloop()
        self.sock.close()

    def initComponents(self):
        '''Inicializa os componentes da aplicação'''
        self.status = Text(self.root, width=30, height=30, background="WHITE", foreground="RED")
        self.status.grid(row=0, column=0)
        scrollbar = Scrollbar(self.root, command=self.status.yview)
        scrollbar.grid(row=0,column=1,sticky=N+S)
        self.status['yscrollcommand'] = scrollbar.set
        self.status.insert('end',"### Clientes Conectados ###\n")
        self.status.configure(state=DISABLED)
        self.text = Text(self.root, width=100, height=30, background="BLACK", foreground="LIGHTGREEN")
        self.text.grid(row=0, column=2)
        scroll = Scrollbar(self.root, command=self.text.yview)
        scroll.grid(row=0,column=3,sticky=N+S)
        self.text['yscrollcommand'] = scroll.set
        self.text.configure(state=DISABLED)
        self.client_list = []

    @threaded
    def initServer(self):
        '''inicializa o servidor, aceita as conexões e salva dois parâmetros, conn (que guardará quem é o cliente) e addr (que guardará o endereço do cliente)'''
        self.writeMsg("Servidor","Inicizalizando o servidor...")
        self.sock = socket.socket()
        self.sock.bind((self.get_ip(), 8899))
        self.writeMsg("Servidor", "Servidor Inicializado no endereço: " + str(self.get_ip()))
        self.sock.listen()
        print("começou")
        while True:
            conn, addr = self.sock.accept()
            #adiciona o cliente na lista de clientes ativos
            self.client_list.append(conn)
            self.updateClientList()
            print (addr[0] + " connected")
            self.writeMsg("Console",str(conn) + " se conectou.")
            # cria uma thread individual para cada cliente
            print("criou a thread")
            self.clientThread(conn,addr)

    @threaded
    def clientThread(self, conn, addr):
        '''Cuidará do serviço de mensagens de cada cliente '''
        conn.send("Bem vindo ao servidor!".encode())
        while True:
            try:
                message = conn.recv(4096).decode()
                print("recebeu")
                if message:
                    print("enviou")
                    self.sock.send(str(input(message)).encode())
                else:
                    print("desconectou")
                    self.remove(conn)
            except:
                continue
                
    def remove(self, conn):
        '''Irá remover o cliente que se desconectou da lista de clientes ativos'''
        if conn in self.client_list:
            self.client_list.remove(conn)
            self.updateClientList()
        
    def updateClientList(self):
        '''Atualiza a lista de clientes conectados'''
        print("atualizou")
        self.status.delete(0, 'end')
        self.status.insert('end',"### Clientes Conectados ###\n")
        for client in self.client_list:
            self.status.insert('end',str(client.getpeername()))

    def writeMsg(self,info,message):
        self.text.configure(state=NORMAL)
        self.text.insert('end', "["+info+"]("+str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)+"): "+message+"\n")
        self.text.configure(state=DISABLED)

    def updateStatus(self,info,pos,message):
        self.status.configure(state=NORMAL)
        self.status.insert(pos, "["+info+"]"+message+"\n")
        self.status.configure(state=DISABLED)

    def get_ip(self):
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

    def input(self,message):
        """Metodo usado para tratar uma instrução comando
            Retorna o que será exibido no servidor"""

        #agora pegamos o comando e salvamos numa variavel
        instruction = message.split(" ")[0]
        if instruction == "/server":
            return self.out_server()
        elif instruction == "/data":
            return self.out_data()
        elif instruction == "/ip":
            return self.out_ip()
        elif instruction == "/mac":
            return self.out_mac()
        elif instruction == "/sys":
            return self.out_sys()
        elif instruction == "/dev":
            return self.out_dev()
        elif instruction == "/info":
            return self.out_info()
        elif instruction == "/dolar":
            return self.out_dolar()
        elif instruction == "/calc":
            return self.out_calc(message)
        elif instruction == "/help":
            return self.out_help()
        else:
            return self.out_error()

    def out_server(self):
        """Método que retornará a saida do comando /server"""
        pass

    def out_data(self):
        """Método que retornará a saida do comando /data"""
        pass

    def out_ip(self):
        """Funcão que retornará a saida o do comando /ip"""
        pass

    def out_mac(self):
        """Método que retornará a saida do comando /mac"""
        pass

    def out_sys(self):
        """Método que retornará a saida do comando /sys"""
        pass

    def out_dev(self):
        """Método que retornará a saida do comando /dev"""
        return 'Desenvolvido por:\nÊndril "Awak3n" Castilho' \
               '\nFernando "Alemão de Troia" Kudrna,' \
               '\nLeonardo "Darth" Pellegrini'

    def out_info(self):
        """Funcão que retornará a saida o do comando /info"""
        pass

    def out_dolar(self):
        """Método que retornará a saida do comando /dolar"""
        # mandando uma requisição em  get para a api
        rqs = requests.get('http://api.promasters.net.br/cotacao/v1/valores')
        # pegando a requisição no formato json e jogando o texto na variavel valoratual
        valoratual = json.loads(rqs.text)
        # pega o retorno json busca a chave valores para pegar o preço do dolar
        return valoratual['valores']['USD']['valor']

    def out_calc(self,string):
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

    def out_help(self):
        return "/server     Retorna o nome do servidor\n" \
               "/data       Reotrna a data do sistema do servidor\n" \
               "/ip         Retorna o endereço IP do servidor\n" \
               "/mac        Retorna o endereço MAC do servidor\n" \
               "/sys        Retorna a descrição do sistema operacional do servidor\n" \
               "/dev        Retorna o nome dos desenvolvedores\n" \
               "/info       Retorna mensagens gerais do sistema\n" \
               "/dolar      Retorna a cotação do dólar\n" \
               "/calc       Retorna o resultado de uma operação algébrica\n" \
               "            <número> <operação( + - / * ^ )> <número>\n"

    def out_error(self):
        """Método que retornará a saida do erro"""
        return "Erro - Comando não encontrado"


#inicialização do programa
if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.start()