import telepot
import subprocess
import time
import speech_recognition as sr
from pydub import AudioSegment
import pymysql.cursors
"""
PARA CONECTAR A UMA DATABASE EXTERNA:
1. de permissão a maquina que vai conectar no seu serviço mysql:
    sudo mysql -u root -p
    GRANT ALL  ON * . * TO 'usuario'@'ip da maquina que vai conectar' IDENTIFIED BY 'senha';
    FLUSH PRIVILEGES;

2. edite o arquivo de configuração do mysql caso necessario:    
    sudo nano  /etc/mysql/mariadb.conf.d/50-server.cnf
troque por: 
    bind-address  = 0.0.0.0

3. libere a porta para conexao externa no firewall:
    sudo ufw allow 3306
    sudo ufw allow 3306/tcp
    sudo ufw allow 3306/udp
"""

#api do bot----------------------------------------->
api = 'API do BOT'
bot = telepot.Bot(api)
bot.deleteWebhook()
"""
#faz a conexao com o banco de dados----------------->
conexao = pymysql.connect(host = 'ip do host',
                          port= 3306,
                          user = 'usuario mysql',
                          password = 'senha mysql',
                          db = 'banco de dados mysql',
                          charset = 'utf8mb4',
                          cursorclass = pymysql.cursors.DictCursor)
#tenta criar as tabelas da Database---------------->
try:
    with conexao.cursor() as cursor:  # faz a conexao com o cursor do mysql
        tabela = f'create table comandos ({"comando varchar(5000), resposta varchar(5000)"})'
        cursor.execute(tabela)  # execução do comando no banco de dados
        conexao.commit()  # gravação do comando no banco de dados
        cursor.close()
    print('Tabela criada na Database com sucesso')
except Exception as e:
    print(e)
    pass
"""


def funcaoBot(msg):
    # faz a conexao com o banco de dados----------------->
    conexao = pymysql.connect(host = 'ip do host',
                              port= 3306,
                          	  user = 'usuario mysql',
                          	  password = 'senha mysql',
                          	  db = 'banco de dados mysql',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
    # FUNÇÕES DO BOT------------------------------------->
    content_type, chat_type, chat_id = telepot.glance(msg)

    #transcodifica vox em texto, recebendo audio do usuario e reenviando em texto no grupo
    if content_type == 'voice':  # or msg.get('reply_to_message')
        bot.download_file(msg['voice']['file_id'], 'audio_usuario.ogg')
        sound = AudioSegment.from_file("audio_usuario.ogg")
        sound.export("audio_usuario.wav", format="wav", bitrate="128k")
        r = sr.Recognizer()
        with sr.WavFile('audio_usuario.wav') as source:
            audio = r.record(source)
        texto = r.recognize_google(audio, language='pt-BR')
        bot.sendMessage(chat_id, f"{msg['from']['first_name']} estava com preguiça de falar, ele disse:\n{texto}")


#MENSAGENS DE TEXTO-------------------------------->
    if msg.get('text'):
        texto = msg['text']
        # sistema de RESPOSTA com database---------->
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from comandos')
                resultados = cursor.fetchall()  # pega todos resultados da db
                cursor.close()
                for resultado in resultados:
                    comando = resultado['comando']
                    resposta = resultado['resposta']
                    if comando == texto:
                        bot.sendMessage(chat_id, f"{resposta}" ) #reply_to_message_id=msg['message_id']    para pegar username {msg['from']['first_name']}
        except Exception as e:
            print(e)
            pass

        # sistema de CADASTRO de respostas------------>
        if texto.startswith('cadastrar'):
            texto_cadastro = texto[10:]                   #tira do texto o  comando 'cadastrar'
            texto_split = texto_cadastro.split('=')       #splita o texto pelo sinal de =
            comando = str(texto_split[0])                 #gera o texto do comando
            resposta = str(texto_split[1])                #gera o texto da resposta
            with conexao.cursor() as cursor:              # faz a conexao com o cursor do mysql
                try:
                    cursor.execute('select * from comandos')  #seleciona tudo na tabela usuarios
                    resultados = cursor.fetchall()            #tras os resultados da tabela mysql
                    cursor.close()                            #sempre fechar a conexao para nao dar erro no mysql
                    existe_cadastro = 0                       #contador para verificar se o comando ja existe
                    for res in resultados:                    #loop em todos resultados da Database
                        if res['comando'] == comando:         #se o comando ja existir o valor existe_cadastro passa ser 1
                            existe_cadastro = 1               #troca o valor de existe_cadastro para 1
                    if existe_cadastro == 1:                  #se o valor existe_cadastro esta como 1 ele avisa que ja existe cadastro
                        bot.sendMessage(chat_id, "Comando já cadastrado, tente outro")
                    elif existe_cadastro == 0:                 #se o valor de existe_cadastro nao foi alterado ele cadastra novo comando
                        with conexao.cursor() as cursor:
                            cursor.execute(f"insert into comandos values ('{comando}','{resposta}')") #insere os valores na tabela
                            conexao.commit()                   # gravação do comando no banco de dados
                            cursor.close()
                            bot.sendMessage(chat_id,  f"Comando cadastrado: {comando}\nResposta cadastrada: {resposta}")
                except Exception as e:
                    print(e)
                    pass

        # sistema de RECADASTRO de respostas------------>
        if texto.startswith('recadastrar'):
            texto_cadastro = texto[12:]  # tira do texto o  comando 'cadastrar'
            texto_split = texto_cadastro.split('=')  # splita o texto pelo sinal de =
            comando = str(texto_split[0])  # gera o texto do comando
            resposta = str(texto_split[1])  # gera o texto da resposta
            with conexao.cursor() as cursor:
                cursor.execute(f"DELETE FROM comandos WHERE comando='{comando}'")  #executa o codigo mysql no banco de dados
                conexao.commit() # grava o codigo no banco de dados
                cursor.close()
                bot.sendMessage(chat_id,f'Comando: {comando} apagado do sistema.')
            with conexao.cursor() as cursor:
                cursor.execute(f"insert into comandos values ('{comando}','{resposta}')")  # insere os valores na tabela
                conexao.commit()  # gravação do comando no banco de dados
                cursor.close()
                bot.sendMessage(chat_id, f"Comando recadastrado: {comando}\nResposta recadastrada: {resposta}")

        # sistema DELETAR respostas------------>
        if texto.startswith('deletar'):
            comando = texto[8:]  # tira do texto o  comando 'cadastrar'
            try:
                with conexao.cursor() as cursor:
                    cursor.execute(f"DELETE FROM comandos WHERE comando='{comando}';")  # executa o codigo mysql no banco de dados
                    conexao.commit()  # grava o codigo no banco de dados
                    cursor.close()
                    bot.sendMessage(chat_id, f'Comando: {comando} apagado do sistema.')
            except:
                bot.sendMessage(chat_id, f'Comando {comando} inexistente ou ocorreu um erro.')

        # sistema LISTAR comandos------------>
        if texto == 'comando':
            try:
                with conexao.cursor() as cursor:  # faz a conexao com o cursor do mysql
                    cursor.execute('select * from comandos')  # seleciona tudo na tabela usuarios
                    resultados = cursor.fetchall()  # tras os resultados da tabela mysql
                    cursor.close()  # sempre fechar a conexao para nao dar erro no mysql
                    todos_comandos = []
                    separador = ' '
                    for result in resultados:
                        todos_comandos.append(result['comando'])
                bot.sendMessage(chat_id, f'Aqui estão todos os meus comandos:\n{separador.join(map(str, todos_comandos))}') #separador.join(map(str, todos_comandos)) descompacta lista em uma coisa so
            except Exception as e:
                print(e)
                pass


        #comandos internos------------------------>
        if texto == 'oi':
           bot.sendMessage(chat_id, 'ola')


#chama a função e deixa o bot em um loop para ficar ativo
bot.message_loop(funcaoBot)
print ('Bot esta online, para desativar o bot feche o programa!')
while 1:
        pass
