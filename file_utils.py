import os
import pandas as pd
import re


def sanitize_filename(filename):
    """Remove caracteres não permitidos de nomes de arquivo."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename).strip()


def generate_unique_filepath(filename):
    """Gera um caminho de arquivo único caso o nome já exista."""
    file_path = f'./Output/{filename}.xlsx'
    counter = 1
    while os.path.exists(file_path):
        file_path = f'./Output/{filename}({counter}).xlsx'
        counter += 1
    return file_path


def create_excel(data, search_value):
    """Cria e salva um arquivo Excel com os dados coletados."""
    df_best = pd.DataFrame(
        data['best'],
        columns=[
            'product_title',
            'score_count',
            'url'
        ]
    )
    df_worst = pd.DataFrame(
        data['worst'],
        columns=[
            'product_title',
            'score_count',
            'url'
        ]
    )
    df_best.columns = df_worst.columns = ['PRODUTO', 'QTD_AVAL', 'URL']

    if not os.path.exists('Output'):
        os.makedirs('Output')

    sanitized_name = sanitize_filename(search_value)
    file_path = generate_unique_filepath(sanitized_name)

    with pd.ExcelWriter(file_path) as writer:
        df_best.to_excel(writer, sheet_name='MELHORES', index=False)
        df_worst.to_excel(writer, sheet_name='PIORES', index=False)

    print(f"Arquivo '{sanitized_name}.xlsx' criado com sucesso na pasta 'Output'.")
    return file_path
