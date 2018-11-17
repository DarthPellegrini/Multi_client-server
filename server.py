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

    def input(self,message):
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
        elif instruction == "/dolar":
            return out_dolar()
        elif instruction == "/calc":
            return out_calc(message)
        elif instruction == "/help":
            return out_help()
        else:
            return out_error()

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
        return "R$ %s" % valoratual['valores']['USD']['valor']
        pass

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
        is_a_operator = ["+","-","/","*"]
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
               "            <número> <+|-|/|*> <número>\n"

    def out_error(self):
        """Método que retornará a saida do erro"""
        return "Erro - Comando não encontrado"

#inicialização do programa
if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.start()