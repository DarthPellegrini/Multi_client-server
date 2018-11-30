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
        self.sock.close()
        exit(0)

    def initComponents(self):
        '''Inicializa os componentes da aplicação'''
        self.text = Text(self.root, width=100, height=30, background="BLACK", foreground="LIGHTGREEN")
        self.text.grid(row=0, column=0)
        self.input = Entry(self.root, width=95)
        self.input.grid(row=1,column=0,sticky=N+S+W)
        self.button = Button(self.root, width=3, height=1, text="enviar")
        self.button.grid(row=1,column=0,columnspan=2,sticky=E)
        scroll = Scrollbar(self.root, command=self.text.yview)
        scroll.grid(row=0,column=1,sticky=N+S)
        self.text['yscrollcommand'] = scroll.set
        self.text.configure(state=DISABLED)
        self.input.bind("<Return>",self.get_input)
        self.input.configure(state=DISABLED)  
        self.button.configure(state=DISABLED)


    def startConnection(self):
        self.writeMsg("Console", "Configurando a conexão do cliente...")
        self.sock = socket.socket()
        # para uso na mesma máquina
        client_address = (socket.gethostbyname(socket.gethostname()), 8899)
        #para uso em máquinas diferentes
        #client_address = (self.get_ip(), 8899)
        self.sock.bind(client_address)

    @threaded
    def connectToServer(self):
        '''Testa a conexão com o servidor '''
        self.writeMsg("Console","Buscando conexão com o servidor...")
        server_address = self.findServer()
        if server_address is not "Erro":
            self.sock.connect((server_address,8899))
            print("deu certo porra")
            self.writeMsg("Console", "Conectado no servidor: " + server_address)
            self.writeMsg("Console", "Para enviar mensagens, digite o caractere ' / ', a mensagem e pressione enviar")
            self.writeMsg("Console", "Para exibir a lista dos comandos, digite /help")
            self.button.bind("<Button-1>", self.get_input)
            self.input.configure(state=NORMAL)  
            self.button.configure(state=NORMAL)
            self.service()
            exit(0)
        else:
            #informa o erro na busca e tenta novamente
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
                print("messsage: "+message)
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
            # não precisa ser alcançável
            s.connect(('8.8.8.8', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def findServer(self):
        ''' Procura na rede local um endereço IP com o port 8899 aberto'''
        own_ip = self.get_ip()
        #print("Got own ip: " + str(own_ip))
        ip_split = own_ip.split('.')
        own_ip = ip_split[:-1]
        subnet = '.'.join(own_ip)

		# iniciará um teste de conexão para cada endereço IP na rede local
        q = Queue()
        processes = []
        for i in range(1, 255):
            ip = subnet + '.' + str(i)
            p = Process(target=self.check_server, args=[ip, q])
            processes.append(p)
            p.start()
        # Dá um tempo para processar
        time.sleep(1.0)

        for idx,p in enumerate(processes):
            # Se não terminou no tempo necessário, termina o processo
            if p.exitcode is None:
                p.terminate()
            else:
                # verificando se a conexão possui o port aberto
                open_ip, address = q.get()
                if open_ip:
                    return address
        return "Erro"
    
    def check_server(self, address, queue):
        ''' Verifica a conexão para um determinado endereço IP '''
        s = socket.socket()
        try:
            s.connect((address, 8899))
            queue.put((True, address))
        except socket.error:
            queue.put((False, address))
    
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
            exit(0)

#inicialização do programa
if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.start()
