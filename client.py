try:
    import time
    import socket
    import datetime
    import threading
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    from multiprocessing import Process, Queue
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
        self.startConnection()
        self.connectToServer()
        
    def start(self):
        '''Inicia a aplicação'''
        self.root.mainloop()
        # caso o programa encerre prematuramente
        try:
            self.sock.send("/quit".encode())
            self.sock.close()
        except:
            pass

    def initComponents(self):
        '''Inicializa os componentes da aplicação'''
        self.text = Text(self.root, width=100, height=30, background="BLACK", foreground="LIGHTGREEN")
        self.text.grid(row=0, column=0, sticky=N+S+E+W)
        self.input = Entry(self.root, width=95)
        self.input.grid(row=1,column=0,sticky=N+S+W)
        self.button = Button(self.root, width=3, height=1, text="enviar")
        self.button.grid(row=1,column=0,columnspan=2,sticky=E)
        scroll = Scrollbar(self.root, command=self.text.yview)
        scroll.grid(row=0,column=1,sticky=N+S)
        self.text['yscrollcommand'] = scroll.set
        self.text.configure(state=DISABLED)
        self.input.configure(state=DISABLED)
        self.button.configure(state=DISABLED)

    def startConnection(self):
        '''Configura o endereço IP do cliente'''
        self.writeMsg("Console", "Configurando a conexão do cliente...")
        self.sock = socket.socket()
        try:
            # para uso em máquinas diferentes
            client_address = (self.get_ip(), 8899)
            self.sock.bind(client_address)
        except:
            # para uso na mesma máquina
            try:
                for n in range(1,255):
                    client_address = ('127.0.0.' + str(n), 8899)
                    try:
                        self.sock.bind(client_address)
                        return
                    except:
                        continue
            except:
                print("Erro - Numero máximo de clientes por máquina")
                exit(0)

    @threaded
    def connectToServer(self):
        '''Testa a conexão com o servidor '''
        self.writeMsg("Console","Buscando conexão com o servidor...")
        # procura um servidor operacional na rede local
        server_status = self.findServer()
        # se conseguiu encontrar e se conectar com o servidor
        if server_status is not "Erro":
            self.input.configure(state=NORMAL)  
            self.button.configure(state=NORMAL)
            if server_status == '0':
                self.sock.connect((self.addr_list[0],8899))
                self.writeMsg("Console", "Conectado no servidor " + self.addr_name[0] )
                self.writeMsg("Console", "Para enviar mensagens, digite o caractere ' / ', o comando e pressione enviar")
                self.writeMsg("Console", "Para exibir a lista dos comandos, digite /help")
                self.input.bind("<Return>", self.get_input)
                self.button.bind("<Button-1>", self.get_input)
                self.service()
            else:
                self.input.bind("<Return>", self.get_server)
                self.button.bind("<Button-1>", self.get_server)
                self.writeMsg("Console", "Servidores disponíveis:")
                for n in range(0,len(self.addr_list)):
                    self.writeMsg("Console",str(n+1) + " - " + self.addr_name[n])
        else:
            # senão, informa o erro na busca, espera um tempo e tenta novamente
            self.writeMsg("Console","Erro - Nenhum servidor encontrado.")
            self.writeMsg("Console","Esperando timeout para tentar novamente...")
            time.sleep(3.0)
            self.connectToServer()

    def service(self):
        '''Realiza o recebimento de mensagens'''
        while True:
            try:
                message = self.sock.recv(2048).decode()
                if message == "":
                    self.writeMsg("Console","O servidor foi desconectado.")
                    self.input.configure(state=DISABLED)  
                    self.button.configure(state=DISABLED)
                    return
                self.writeMsg("Servidor",message)
            except:
                return

    def writeMsg(self,info,message):
        self.text.configure(state=NORMAL)
        self.text.insert('end', "["+info+"]("+str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)+"): "+message+"\n")
        self.text.see('end')
        self.text.configure(state=DISABLED)

    def get_ip(self):
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

    def findServer(self):
        ''' Procura na rede local um endereço IP com o port 8899 aberto'''
        # pega o próprio endereço ip
        own_ip = self.get_ip()
        ip_split = own_ip.split('.')
        own_ip = ip_split[:-1]
        # e separa a sub-rede local
        subnet = '.'.join(own_ip)

		# realiza um teste de conexão para cada endereço IP na rede local
        q = Queue()
        processes = []
        for i in range(1, 255):
            ip = subnet + '.' + str(i)
            p = Process(target=self.check_server, args=[ip, q])
            processes.append(p)
            p.start()

        # dá um tempo para processar todas as conexões
        time.sleep(1.0)

        # e procura uma conexão
        self.addr_list = []
        self.addr_name = []
        for idx,p in enumerate(processes):
            # Se não terminou no tempo necessário, termina o processo
            if p.exitcode is None:
                p.terminate()
            else:
                # verificando se a conexão possui o port aberto
                open_ip, address, name = q.get()
                if open_ip:
                    self.addr_list.append(address)
                    self.addr_name.append(name)
        if len(self.addr_list) == 0:
            return "Erro"
        else:
            return str(len(self.addr_list))
    
    def check_server(self, address, queue):
        ''' Verifica a conexão para um determinado endereço IP '''
        s = socket.socket()
        try:
            s.connect((address, 8899))
            s.send("/server".encode())
            queue.put((True, address, s.recv(2048).decode())[5:] )
        except socket.error:
            queue.put((False, address, "none"))
    
    def get_input(self,event):
        ''' Pega o conteúdo do que foi digitado e o envia para o servidor '''
        try:
            input = self.input.get()
            self.writeMsg("Cliente",input)
            self.input.delete(0, 'end')
            self.sock.send(input.encode())
        except:
            self.writeMsg("Console", "Erro - Servidor desconectado.")
            self.button.configure(state=DISABLED)
            self.sock.close()
    
    def get_server(self, event):
        ''' Verifica se o servidor selecionado está disponível '''
        try:
            input = int(self.input.get())-1
            self.input.delete(0, 'end')
            if input > 0 and input < len(self.addr_list):
                self.sock.connect((self.addr_list[input],8899))
                self.writeMsg("Console", "Conectado no servidor " + self.addr_name[input] )
                self.writeMsg("Console", "Para enviar mensagens, digite o caractere ' / ', o comando e pressione enviar")
                self.writeMsg("Console", "Para exibir a lista dos comandos, digite /help")
            else:
                raise Exception
            
        except:
            self.writeMsg("Console", "Erro - Número de servidor inválido.")

    

#inicialização do programa
if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.start()
