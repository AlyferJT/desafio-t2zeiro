from selenium import webdriver


def configure_driver():
    """Configura e retorna o WebDriver."""
    chrome_options = webdriver.ChromeOptions()
    # Mantém o navegador aberto após a execução
    chrome_options.add_experimental_option("detach", True)
    # Inicializa o WebDriver com as opções configuradas
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()  # Maximiza a janela do navegador
    return driver
