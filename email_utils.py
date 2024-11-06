import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(file_path, data_summary, sender_email, sender_password, receiver_email, search_value):
    """Envia um e-mail com o arquivo anexado."""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Relatório {search_value.capitalize()}"

    body = (
        f"Olá, aqui está o seu relatório dos {search_value}.\n\n"
        f"Produtos:\n"
        f"Total: {data_summary['total']} produtos\n"
        f"Melhores: {data_summary['best']} produtos\n"
        f"Piores: {data_summary['worst']} produtos\n\n"
        "Atenciosamente,\nRobô"
    )
    msg.attach(MIMEText(body, 'plain'))

    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename(file_path)}'
        )
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
    finally:
        server.quit()
