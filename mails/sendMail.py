import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mails.infoMail import EmailCadastro, EmailRedefinicaoSenha, Config

def send_email(user_info):
    server = None
    server_smtp = Config.CONECTION
    port = Config.PORT
    sender_email = Config.MAIL
    password = Config.MAIL_PASSWORD
    receive_email = user_info.email
    subject = 'Cadastro Esporte+!'

    body = EmailCadastro(user_info.nome)

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receive_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(server_smtp, port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receive_email, message.as_string())
    except Exception:
        print("Erro: Endereço de E-mail Inválido")
    finally:
        if server:
            server.quit()

def send_email_reset_password(email, nome, token: str):
    server = None
    server_smtp = Config.CONECTION
    port = Config.PORT
    sender_email = Config.MAIL
    password = Config.MAIL_PASSWORD
    receive_email = email
    body = EmailRedefinicaoSenha(nome, token)
    subject = 'Redefinição de Senha Esporte+!'

    

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receive_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(server_smtp, port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receive_email, message.as_string())
    except Exception:
        print("Erro: Endereço de E-mail Inválido")
    finally:
        if server:
            server.quit()