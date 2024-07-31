import re
import shutil
from pathlib import Path


# Renomear memória de cálculo depois de movido
def rename_memo(destination_memo_folder, pdf_file, competencia):
    old_name = ""
    new_name = ""
    
    new_pdf_file = pdf_file.name.replace(f' {competencia}', '').strip()
    
    old_name = destination_memo_folder / pdf_file.name
    new_name = destination_memo_folder / new_pdf_file
    #Path.rename(old_name, new_name)
    return old_name, new_name

async def copy_pdf_to_folder(source_folder, destination_folder):
    # Lista todos os arquivos PDF na pasta fonte (source_folder)
    pdf_files = [file for file in source_folder.iterdir() if file.suffix == '.pdf']

    # Itera sobre os arquivos PDF
    for pdf_file in pdf_files:

        is_folder = True

        # Pega o nome do arquivo PDF
        file_name = pdf_file.name

        # Extrai a competência do atendimento (C7, C8 etc)
        match_competencia = re.search(r'C\d+', file_name)
        competencia = match_competencia.group()

        # Extrai o número do atendimento do nome do arquivo
        match = re.search(r'\d{13}', file_name)
        if match:
            numero_de_atendimento = match.group()

            # Cria a pasta de destino se ela não existir
            destination_folder_name = destination_folder / f'AIH {numero_de_atendimento}'
            if not destination_folder_name.exists():
                destination_folder_name = destination_folder / f'APAC {numero_de_atendimento} {competencia}'
                if not destination_folder_name.exists():
                    is_folder = False

            # Copia o arquivo PDF para a pasta destino
            try:
                if is_folder:
                    shutil.move(pdf_file, destination_folder_name)
                    if 'MEMÓRIA DE CÁLCULO' in file_name:
                        memo_path = rename_memo(destination_folder_name, pdf_file, competencia)
                        Path.rename(memo_path[0], memo_path[1])
            except shutil.Error as e:
                return F"Error: {e}"
    return "Concluído com sucesso"
