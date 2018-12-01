import datetime

def show_date():
    month_database = {1:"Janeiro",2:"Fevereiro",3:"Março",4:"Abril",5:"Maio",6:"Junho",7:"Julho",8:"Agosto",9:"Setembro",10:"Outubro",11:"Novembro",12:"Dezembro"}
    date = "Hoje é dia " + str(datetime.datetime.now().day) + " de " + month_database[datetime.datetime.now().month] + " de " + str(datetime.datetime.now().year)
    while (len(date) < 33):
        if len(date) % 2 == 0:
            date += " "
        else:
            date = " " + date
    return date

def show_message():
    time = float(datetime.datetime.now().hour)
    second = float(datetime.datetime.now().second)

    if (time >= 6 and second > 0) and time < 12:
        return " Bom dia! "
    elif (time >= 12 and second > 0) and time <= 19:
        return "Boa tarde!"
    else:
        return "Boa noite!"

def show_ip(ip):
    while len(ip) < 51:
        if len(ip) % 2 == 0:
            ip += " "
        else:
            ip = " " + ip
    return ip

"############################################################" \
"####                                                    ####" \
"####                     " + show_message() + "                     ####" \
"####                                                    ####" \
"####          "+show_date()+"         ####" \
"####                                                    ####" \
"####"+show_ip("O servidor está rodando no endereço 192.168.0.1")+" ####" \
"####                                                    ####" \
"####                 Desenvolvido por:                  ####" \
"####              Êndril \"Awak3n\" Castilho              ####" \ 
"####         Fernando \"Alemão de Troia\" Kudrna          ####" \
"####            Leonardo \"Darth\" Pellegrini             ####" \
"####                                                    ####" \
"############################################################"
