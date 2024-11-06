from selenium.webdriver.support.ui import WebDriverWait

from config import (
    URL,
    SEARCH_VALUE,
    PAGINATION,
    SCORE_THRESHOLD,
    SENDER_EMAIL,
    SENDER_PASSWORD,
    RECEIVER_EMAIL
)
from driver_utils import configure_driver
from data_collection import get_data
from file_utils import create_excel
from email_utils import send_email


def main():
    """Configura o WebDriver, coleta dados, cria um arquivo Excel e envia por e-mail."""
    # Configurar WebDriver
    driver = configure_driver()
    wait = WebDriverWait(driver, 10)

    try:
        # Coletar dados do site
        data = get_data(
            driver, wait, URL, SEARCH_VALUE, SCORE_THRESHOLD, PAGINATION
        )

        # Criar o arquivo Excel com os dados coletados
        file_path = create_excel(data, SEARCH_VALUE)

        # Resumo dos dados coletados
        data_summary = {
            'total': len(data['best']) + len(data['worst']),
            'best': len(data['best']),
            'worst': len(data['worst'])
        }

        # Enviar e-mail com o arquivo anexado
        send_email(
            file_path,
            data_summary,
            SENDER_EMAIL,
            SENDER_PASSWORD,
            RECEIVER_EMAIL,
            SEARCH_VALUE
        )

    finally:
        # Fechar o driver após a execução
        driver.quit()


if __name__ == "__main__":
    main()
