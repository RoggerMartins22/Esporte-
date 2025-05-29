from dotenv import load_dotenv
import os
from datetime import datetime, date, time
load_dotenv()  

class Config:
    CONECTION = os.getenv("CONECTION")
    SMTP_PORT = os.getenv("SMTP_PORT")
    MAIL = os.getenv("MAIL")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

FRONTEND_BASE_URL = os.getenv("FRONTEND_URL")

class InfoMail:

    @staticmethod
    def _base_email_body(content: str, title: str = "Notificação Esporte+"):
        header_color = "#28a745"
        text_color = "#333333"
        accent_color = "#007bff"
        background_color = "#f4f4f4"
        box_background = "#ffffff"
        border_color = "#dddddd"

        return f"""
            <html lang="pt-BR">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>{title}</title>
                </head>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: {text_color}; background-color: {background_color}; margin: 0; padding: 0;">
                    <div style="width: 100%; max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid {border_color}; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); background-color: {box_background};">
                        <h2 style="color: {header_color}; text-align: center; margin-bottom: 20px; font-size: 24px; font-weight: bold;">
                            {title.split(' - ')[0]}
                        </h2>
                        {content}
                        <p style="font-size: 0.9em; color: #777; margin-top: 30px; text-align: center; border-top: 1px solid #eee; padding-top: 15px;">
                            Atenciosamente,<br>Equipe Esporte+
                        </p>
                    </div>
                </body>
            </html>
        """

    @staticmethod
    def EmailCadastro(nome: str):
        content = f"""
            <p style="margin-bottom: 10px;">Olá <strong>{nome}</strong>,</p>
            <p style="margin-bottom: 10px;">Seu cadastro no sistema <strong style="color: #28a745;">Esporte+</strong> foi realizado com sucesso! 🎉</p>
            <p style="margin-bottom: 10px;">Agora você pode acessar sua conta e começar a explorar as quadras disponíveis para seus próximos agendamentos.</p>
            <p style="margin-bottom: 10px;">Estamos animados para ter você em nossa comunidade!</p>
            <br>
        """
        return InfoMail._base_email_body(content, title="Cadastro Confirmado - Esporte+")

    @staticmethod
    def EmailRedefinicaoSenha(nome: str, token: str, frontend_url: str = FRONTEND_BASE_URL):
        reset_link = f"{frontend_url}/redefinir-senha/{token}" 

        content = f"""
            <p style="margin-bottom: 10px;">Olá <strong>{nome}</strong>,</p>
            <p style="margin-bottom: 10px;">Recebemos uma solicitação para redefinir sua senha. 🔑</p>
            <p style="text-align: center; margin-bottom: 20px;">
                Para prosseguir com a redefinição, por favor, clique no botão abaixo:</p>
            <p style="text-align: center;">
                <a href="{reset_link}" style="display: inline-block; padding: 12px 25px; background-color: #007bff; color: #ffffff; text-decoration: none; border-radius: 5px; font-weight: bold;">Redefinir Senha</a>
            </p>
            <p style="margin-top: 20px;">Se o botão acima não funcionar, você pode copiar e colar o link em seu navegador:</p>
            <p style="word-break: break-all; font-size: 0.9em;"><small>{reset_link}</small></p>
            <p style="margin-top: 20px;">Se você não solicitou essa redefinição, por favor, ignore este e-mail. Sua senha permanecerá inalterada.</p>
            <br>
        """
        return InfoMail._base_email_body(content, title="Redefinição de Senha - Esporte+")

    @staticmethod
    def _format_date_for_email(date_obj_or_str) -> str:
        if date_obj_or_str is None:
            return "N/A"
        
        if isinstance(date_obj_or_str, date):
            return date_obj_or_str.strftime('%d/%m/%Y')
        elif isinstance(date_obj_or_str, str):
            try:
                dt_obj = datetime.strptime(date_obj_or_str, '%Y-%m-%d').date()
                return dt_obj.strftime('%d/%m/%Y')
            except ValueError:
                return date_obj_or_str
        return "N/A"

    @staticmethod
    def _format_time_for_email(time_obj_or_str) -> str:
        if time_obj_or_str is None:
            return "N/A"
        
        if isinstance(time_obj_or_str, time):
            return time_obj_or_str.strftime('%H:%M')
        elif isinstance(time_obj_or_str, str): 
            return time_obj_or_str[:5]
        return "N/A"

    @staticmethod
    def EmailConfirmacaoAgendamento(nome: str, agendamento):
        formatted_date = InfoMail._format_date_for_email(getattr(agendamento, 'data', None))
        formatted_horario_inicio = InfoMail._format_time_for_email(getattr(agendamento, 'horario_inicio', None))
        formatted_horario_fim = InfoMail._format_time_for_email(getattr(agendamento, 'horario_fim', None))

        content = f"""
            <p style="margin-bottom: 10px;">Olá <strong>{nome}</strong>,</p>
            <p style="margin-bottom: 10px;">Seu agendamento foi realizado com sucesso. Prepare-se para jogar! ✅</p>
            <p style="font-weight: bold; margin-top: 20px;">Detalhes do seu agendamento:</p>
            <ul style="list-style: none; padding: 0; margin-top: 15px; border-top: 1px solid #eee; padding-top: 15px;">
                <li style="margin-bottom: 8px;"><strong>Quadra:</strong> {getattr(agendamento, 'nome_quadra', 'Não informado')}</li>
                <li style="margin-bottom: 8px;"><strong>Data:</strong> {formatted_date}</li>
                <li style="margin-bottom: 8px;"><strong>Horário:</strong> {formatted_horario_inicio} - {formatted_horario_fim}</li>
            </ul>
            <p style="margin-top: 20px;">Agradecemos a preferência!</p>
            <br>
        """
        return InfoMail._base_email_body(content, title="Agendamento Confirmado - Esporte+")
    
    @staticmethod
    def EmailCancelamentoAgendamento(nome: str, agendamento):
        formatted_date = InfoMail._format_date_for_email(getattr(agendamento, 'data', None))
        formatted_horario_inicio = InfoMail._format_time_for_email(getattr(agendamento, 'horario_inicio', None))
        formatted_horario_fim = InfoMail._format_time_for_email(getattr(agendamento, 'horario_fim', None))

        content = f"""
            <p style="margin-bottom: 10px;">Olá <strong>{nome}</strong>,</p>
            <p style="margin-bottom: 10px;">Seu agendamento foi cancelado. Lamentamos que não possa comparecer. ❌</p>
            <p style="font-weight: bold; margin-top: 20px;">Detalhes do agendamento cancelado:</p>
            <ul style="list-style: none; padding: 0; margin-top: 15px; border-top: 1px solid #eee; padding-top: 15px;">
                <li style="margin-bottom: 8px;"><strong>Quadra:</strong> {getattr(agendamento, 'nome_quadra', 'Não informado')}</li>
                <li style="margin-bottom: 8px;"><strong>Data:</strong> {formatted_date}</li>
                <li style="margin-bottom: 8px;"><strong>Horário:</strong> {formatted_horario_inicio} - {formatted_horario_fim}</li>
            </ul>
            <p style="margin-top: 20px;">Você pode agendar uma nova quadra a qualquer momento. Esperamos vê-lo(a) em breve!</p>
            <br>
        """
        return InfoMail._base_email_body(content, title="Agendamento Cancelado - Esporte+")
    
    @staticmethod
    def EmailRenovacaoAgendamento(nome: str, agendamento):
        formatted_date = InfoMail._format_date_for_email(getattr(agendamento, 'data', None))
        formatted_horario_inicio = InfoMail._format_time_for_email(getattr(agendamento, 'horario_inicio', None))
        formatted_horario_fim = InfoMail._format_time_for_email(getattr(agendamento, 'horario_fim', None))

        content = f"""
            <p style="margin-bottom: 10px;">Olá <strong>{nome}</strong>,</p>
            <p style="margin-bottom: 10px;">Seu agendamento foi renovado com sucesso! Sua paixão pelo esporte continua. 🔁</p>
            <p style="font-weight: bold; margin-top: 20px;">Novos detalhes do seu agendamento:</p>
            <ul style="list-style: none; padding: 0; margin-top: 15px; border-top: 1px solid #eee; padding-top: 15px;">
                <li style="margin-bottom: 8px;"><strong>Quadra:</strong> {getattr(agendamento, 'nome_quadra', 'Não informado')}</li>
                <li style="margin-bottom: 8px;"><strong>Data:</strong> {formatted_date}</li>
                <li style="margin-bottom: 8px;"><strong>Horário:</strong> {formatted_horario_inicio} - {formatted_horario_fim}</li>
            </ul>
            <p style="margin-top: 20px;">Em caso de dúvidas, entre em contato com nosso suporte.</p>
            <br>
        """
        return InfoMail._base_email_body(content, title="Agendamento Renovado - Esporte+")