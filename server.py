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
        self.initServer()
        
    def start(self):
        '''Inicia a aplicação'''
        self.root.mainloop()

    def initComponents(self):
        '''Inicializa os componentes da aplicação'''
        self.status = Text(self.root, width=40, height=30, background="WHITE", foreground="RED")
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

    def initServer(self):
        self.writeMsg("Servidor","Inicizalizando o servidor...")
        self.sock = socket.socket()
        hostname = socket.gethostname()
        server_address = (hostname, 8899)
        self.sock.bind(server_address)
        self.writeMsg("Servidor", "Servidor Inicializado!")
        
    def writeMsg(self,info,message):
        self.text.configure(state=NORMAL)
        self.text.insert('end', "["+info+"]("+str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)+"): "+message+"\n")
        self.text.configure(state=DISABLED)

    def updateStatus(self,info,pos,message):
        self.status.configure(state=NORMAL)
        self.status.insert(pos, "["+info+"]"+message+"\n")
        self.status.configure(state=DISABLED)


        
#inicialização do programa
if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.start()