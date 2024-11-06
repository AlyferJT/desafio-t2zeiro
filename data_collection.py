import re
import sys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException


def get_data(driver, wait, url, search_value, score_threshold, pagination):
    """Coleta dados de produtos do site."""
    data = {'best': [], 'worst': []}

    # Carrega URL com tentativas
    for attempt in range(3):
        try:
            driver.get(url)
            print("Página carregada com sucesso!")
            break
        except WebDriverException:
            print(f"Tentativa {attempt + 1} falhou, tentando novamente...")
            time.sleep(2)
    else:
        print("Site fora do ar")
        sys.exit()

    # Busca produtos
    search_input = wait.until(
        EC.presence_of_element_located((By.ID, "input-search"))
    )
    search_input.send_keys(search_value, Keys.ENTER)

    page_count = get_page_count(wait)
    print(f"Total de páginas: {page_count}")
    for page in range(1, page_count + 1):
    # for page in range(1, 3):
        collect_page_data(data, wait, score_threshold)

        # Paginação
        if page >= page_count or not pagination:
            break
        navigate_to_next_page(wait, page + 1)
        time.sleep(5)

    return data


def get_page_count(wait):
    """Obtém o número total de páginas."""
    try:
        page_count_text = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                '//nav[@aria-label="pagination navigation"]//ul/li[position()=last()-1]/a'
            ))
        ).text
        return int(page_count_text)
    except NoSuchElementException:
        return 1


def collect_page_data(data, wait, score_threshold):
    """Coleta dados de produtos na página atual."""
    product_list_container = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@data-testid="product-list"]'))
    )
    product_cards = product_list_container.find_elements(By.XPATH, './/ul[@data-testid="list"]/li/a')

    for product in product_cards:
        try:
            link = product.get_attribute("href")
            title = product.find_element(By.XPATH, './/h2[@data-testid="product-title"]').text
            score_text = product.find_element(By.XPATH, ".//div[@data-testid='review']/span").text
            score_count = int(re.search(r'\((\d+)\)', score_text).group(1))

            if score_count > 0:
                category = 'best' if score_count >= score_threshold else 'worst'
                data[category].append({
                    'score_count': score_count,
                    'product_title': title,
                    'url': link
                })
        except NoSuchElementException:
            continue
        except:
            continue


def navigate_to_next_page(wait, next_page_number):
    """Navega para a próxima página de resultados."""
    next_page_button = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            f'//a[@role="button" and @title="página {next_page_number}"]'
        ))
    )
    next_page_button.click()
    print(f"=== PÁGINA {next_page_number} ===")
