[![Build](https://img.shields.io/badge/dev-gorpo-brightgreen.svg)]()
[![Stage](https://img.shields.io/badge/Release-Stable-brightgreen.svg)]()
[![Build](https://img.shields.io/badge/python-v3.7-blue.svg)]()
[![Build](https://img.shields.io/badge/windows-7%208%2010-blue.svg)]()
[![Build](https://img.shields.io/badge/Linux-Ubuntu%20Debian-orange.svg)]()
[![Build](https://img.shields.io/badge/arquiterura-64bits-blue.svg)]()

<h6 align="center">
   <img src="https://raw.githubusercontent.com/gorpo/Manicomio-Boot-Theme/master/manicomio/boot.png" width="55%"></img>
       <h2 align="center">Manicomio | Python Telegram Bot | com Database e Conversão de Audio em  Texto</h2>
  </h6>
<h3>Telegram Bot com CRUD Mysql + Python</h3><br>

<p>Telegram Bot Python com Banco de dados Mysql e CRUD interno, gravando comandos, reescrevendo comandos ja gravados(editando), deletando comandos diretamente pela interface do bot.</p>

# Requisitos:
- Python3.7 (não testado em outros)
- telepot
- speech_recognition 
- pydub 
- pymysql

# Requisitos:
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
