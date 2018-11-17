try:
    import socket
    import datetime
    import threading
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
except:
    print("Este programa requer Python 3.x e a biblioteca Python-Tk")
    exit(0)

class Application():
    '''Classe principal'''

    def __init__(self, root):
        '''Construtor da classe, recebe a janela como parâmetro'''
        self.root = root
        self.initComponents()
        self.connectToServer()
        
    def start(self):
        '''Inicia a aplicação'''
        self.root.mainloop()

    def initComponents(self):
        '''Inicializa os componentes da aplicação'''
        self.text = Text(self.root, width=100, height=30, background="BLACK", foreground="LIGHTGREEN")
        self.text.grid(row=0, column=0)
        self.input = Entry(self.root, width=95)
        self.input.grid(row=1,column=0,sticky=N+S+W)
        self.button = Button(self.root, width=3, height=1,text="enviar")
        self.button.grid(row=1,column=0,columnspan=2,sticky=E)
        scroll = Scrollbar(self.root, command=self.text.yview)
        scroll.grid(row=0,column=1,sticky=N+S)
        self.text['yscrollcommand'] = scroll.set
        self.text.configure(state=DISABLED)

    def connectToServer(self):
        self.writeMsg("Cliente","Iniciazalizando as configurações de conexão...")
        self.sock = socket.socket()
        hostname = socket.gethostname()
        client_address = (hostname, 8899)
        self.sock.bind(client_address)
        self.writeMsg("Cliente","Buscando conexão com o servidor...")
        
    def writeMsg(self,info,message):
        self.text.configure(state=NORMAL)
        self.text.insert('end', "["+info+"]("+str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)+"): "+message+"\n")
        self.text.configure(state=DISABLED)


        
#inicialização do programa
if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.start()