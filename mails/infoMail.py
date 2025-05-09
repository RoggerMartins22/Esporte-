from dotenv import load_dotenv
import os
load_dotenv()  

class Config:
    CONECTION = os.getenv("CONECTION")
    PORT = os.getenv("PORT")
    MAIL = os.getenv("MAIL")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

conexao = Config.CONECTION
porta = Config.PORT
email_de_envio = Config.MAIL
senha = Config.MAIL_PASSWORD

def EmailCadastro(nome):
    body = f"""
        <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <title>Cadastro Confirmado</title>
            </head>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2>Cadastro confirmado!</h2>
                <p>Olá <strong>{nome}</strong>,</p>
                <p>Seu cadastro no sistema <strong>Esporte+</strong> foi realizado com sucesso.</p>
                <p>Agora você pode acessar o sistema e começar a agendar suas quadras esportivas.</p>
                <p>Obrigado por se cadastrar!</p>
                <br>
                <p>Atenciosamente,<br>Equipe Esporte+</p>
            </body>
        </html>
    """
    return body