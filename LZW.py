import sys
import math
from PIL import Image

def executar_lzw_imagem():
    # Verifica se o path da imagem foi passado como argumento
    if len(sys.argv) < 2:
        print("Argumento incorreto, use: python lzw_image.py <caminho_para_imagem>")
        return
    else:
        caminho_imagem = sys.argv[1]

    print("Qual a compressão desejada?")
    print("1 - 144p")
    print("2 - 360p")
    print("3 - 1080p")
    print("9 - Realizar a compressão em 144p, 360p e 1080p de uma vez (gera 3 arquivos de saída).")
    opcao = input("Digite a opção (1, 2, 3 ou 9): ").strip()

    resolucoes = {
        '144': (176, 144),
        '360': (640, 360),
        '1080': (1920, 1080),
        '1': (176, 144),
        '2': (640, 360),
        '3': (1920, 1080)
    }

    # Lista de resoluções a serem processadas
    if opcao == '9':
        lista_processamento = ['144', '360', '1080']

    elif opcao in resolucoes:
        if opcao in ['1', '144']: lista_processamento = ['144']
        elif opcao in ['2', '360']: lista_processamento = ['360']
        elif opcao in ['3', '1080']: lista_processamento = ['1080']

    else:
        print("Opção de resolução inválida! Encerrando...")
        return


    for res_atual in lista_processamento:
        largura, altura = resolucoes[res_atual]

        try: # tenta ler, redimensionar e exibir a imagem
           # L representa a escala de cinza com tamanho de 8  bits
           # "1. Ler uma imagem em escala de cinza."
            img = Image.open(caminho_imagem).convert('L')
            img = img.resize((largura, altura))

            # Exibe a imagem redimensionada
            img.show(title=f"Imagem {res_atual}p")
            
        except Exception as e:
            print(f"Erro ao processar imagem {res_atual}p: {e}")
            continue

        # da squash na matriz pra deixar em vetor
        # "2. Converter a matriz de pixels em um vetor" 
        vetor_pixels = list(img.get_flattened_data())
        quantidade_pixels = len(vetor_pixels)

    #######################################################

        # começa o LZW em si

        # "4. Inicializar o dicionário com os valores de 0 a 255."
        tamanho_dicionario = 256
        dicionario = {tuple([i]): i for i in range(tamanho_dicionario)}

        # "3. Aplicar o algoritmo LZW sobre esse vetor"
        w = ()
        sequencia_codificada = []

        # Preenche o dicionário e gera a sequência codificada
        # " 5. Gerar a sequência codificada"
        for pixel in vetor_pixels:
            wk = w + (pixel,)
            if wk in dicionario:
                w = wk
            else:
                sequencia_codificada.append(dicionario[w])
                dicionario[wk] = tamanho_dicionario
                tamanho_dicionario += 1
                w = (pixel,)

        # Adiciona o último padrão 
        if w:
            sequencia_codificada.append(dicionario[w])

        # 5. Cálculos de tamanho e compressão
        # Tamanho original: cada pixel em escala de cinza tem 8 bits (1 byte)
        tamanho_mensagem_original = quantidade_pixels
        tamanho_original_bits = quantidade_pixels * 8

        # Tamanho comprimido: depende da quantidade de bits necessários para representar o maior índice gerado
        bits_por_indice = math.ceil(math.log2(tamanho_dicionario))
        tamanho_comprimido_bits = len(sequencia_codificada) * bits_por_indice

        porcentagem_compressao = (1 - (tamanho_comprimido_bits / tamanho_original_bits)) * 100

        """    
        6. Saídas Obrigatórias
        6.1 A imagem - entendi que é a imagem já redimensionada e em grayscale, ta lá no começo, linha 53 (dentro do try catch) ;
        6.2 Resolução da imagem;
        6.3 Quantidade total de pixels;
        6.4 Vetor original de pixels;
        6.5 Dicionário final gerado;
        6.6 Sequência codificada;
        6.7 Tamanho da mensagem original;
        6.8 Tamanho original em bits;
        6.9 Tamanho comprimido em bits;
        6.10 Porcentagem de compressão.

        """
        # Salva tudo em uma string pra depois de printar salvar tudo de uma vez (opção 9)
        saida_texto = f"\n{'='*50}\n"
        saida_texto += "SAÍDAS LZW\n"
        saida_texto += f"{'='*50}\n"
        # 6.2 Resolução da imagem
        saida_texto += f"Resolução {largura}x{altura} pixels ({res_atual}p)\n"
        # 6.3 Quantidade total de pixels
        saida_texto += f"Quantidade total de pixels: {quantidade_pixels}\n"
        
        # 6.4 Vetor original de pixels
        # Para não crashar o terminal em imagens hd, mostra so primeiros e últimos elementos
        saida_texto += f"\nVetor original de pixels (começo): {vetor_pixels[:50]}...\n\n"
        saida_texto += f"Vetor original de pixels (final): {vetor_pixels[-50:]}\n"
        
        # 6.5 Dicionário final gerado
        # imprime as ultimas 20 entradas como prova (mais que isso começa a ficar grande demais e pode morrer o terminal)
        saida_texto += f"\nDicionário final gerado (Total de chaves: {tamanho_dicionario})\n"
        saida_texto += "Últimas 20 sequências adicionadas:\n"
        ultimas_entradas = list(dicionario.items())[-20:]
        for chave, valor in ultimas_entradas:
            saida_texto += f"  {chave} : {valor}\n"

        # 6.6 Sequência codificada
        saida_texto += f"\nSequência codificada (começo): {sequencia_codificada[:50]}...\n"
        saida_texto += f"Sequência codificada (final){sequencia_codificada[-50:]}\n"
        
        # 6.7, 6.8 e 6.9 Tamanhos
        saida_texto += f"\nTamanho da mensagem original.: {tamanho_mensagem_original} valores\n"
        saida_texto += f"Tamanho original em bits.....: {tamanho_original_bits} bits\n"
        saida_texto += f"Tamanho comprimido em bits...: {tamanho_comprimido_bits} bits\n"
        
        # 6.10 Porcentagem de compressão
        if porcentagem_compressao > 0:
            saida_texto += f"Porcentagem de compressão....: {porcentagem_compressao:.2f}% (Redução de tamanho)\n"
        else:
            # imagem não foi comprimida, tinha muito ruído -> alg nao foi eficiente então aumentou de tamanho
            saida_texto += f"Porcentagem de compressão....: {porcentagem_compressao:.2f}% (Aumento de tamanho)\n"
        saida_texto += f"{'='*50}\n"

    
        print(saida_texto)

        # Se opção 9, também gera os arquivos de saída de cada resoluçãp em formato .txt 
        if opcao == '9':
            nome_arquivo = f"saida_LZW_{res_atual}p.txt"
            try:
                with open(nome_arquivo, "w", encoding="utf-8") as f:
                    f.write(saida_texto)
                print(f">>> Arquivo de log gerado com sucesso: {nome_arquivo} <<<\n")
            except Exception as e:
                print(f"Erro ao salvar o arquivo {nome_arquivo}: {e}")

if __name__ == "__main__":
    executar_lzw_imagem()