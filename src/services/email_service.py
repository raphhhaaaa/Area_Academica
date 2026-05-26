import json
import smtplib
from src.utils.json_util import extrai_json
from src.config import USUARIO, DOMINIO_INSTITUICAO, EMAIL_REMETENTE, SENHA_REMETENTE
from email.message import EmailMessage

usuario_email = USUARIO + DOMINIO_INSTITUICAO

## configurações do email SMTP
email_remetente = EMAIL_REMETENTE
remetente_senha = SENHA_REMETENTE

def alerta_faltas(disciplina):

    # cria mensagem
    msg = EmailMessage()
    msg['Subject'] = f"Alerta: seu número de faltas em {disciplina['Disciplina']} está alto."
    msg['From'] = email_remetente
    msg['To'] = usuario_email
    msg.set_content(f"Número de faltas em {disciplina['Disciplina']} alto. Faltas: {disciplina['Faltas']}")

    #envia e-mail atraves do servidor SMTP
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_remetente, remetente_senha)
            smtp.send_message(msg)
        print('E-mail enviado com sucesso.')
    except Exception as e:
        print('Erro ao enviar email.', e)

