def edf_lis(path="/Users/joselito/tcc/dataset"):
    import os

    list_edf = []

    for filename in os.listdir(path):
        if filename.endswith(".edf"):
            list_edf.append(filename);
        else:
            continue
    print("Lista de arquivos .edf obtida")
    list_edf = sorted(list_edf);
    return list_edf

def signals(list_edf,i):
    import pyedflib
    '''
    depois alterar para que o canal seja iterativo para varrer o arquivo completo
    '''
    file = list_edf[i]
    [signals, signal_headers, header] = pyedflib.highlevel.read_edf('/Users/joselito/tcc/dataset/' + file, ch_nrs=0,
                                                                    digital=True)

    return signals

def sigtes():
    '''
    Pega o primeiro canal do primeiro paciente do primeiro edf só
    Returns
    -------
    é isso porra
    '''
    import pyedflib
    [signals, signal_headers, header] = pyedflib.highlevel.read_edf('/Users/joselito/tcc/dataset/chb01-chb01_01.edf',
                                                                    ch_nrs=0, digital=True)
    return signals

def bla(list_edf):
    import numpy as np
    '''
    input: list_edf: lista com todos os arquivos dentro da pasta

    :return:
    matrix com todos os valores do mesmo canal em um array
    canal padrão é 0 
    caso queira alterar, criar-se-á lógica
    '''
    matrix = []
    for i in range(len(list_edf)):
        # print("Importando arquivo ",i+1," de ",len(list_edf))
        signals_data = signals(list_edf, i)
        matrix.append(signals_data)
    matrix = np.hstack(matrix)
    print("Todos arquivos foram importados.")
    return matrix

def h5py(data):
    import h5py
    import numpy as np

    '''
    alterar os parâmetros de entrada de nome
    adicionar função de separar em subgrupos,
        os quais serão categorizados por 
        pacientes e talvez por arquivos edf's
    '''

    # Fecha-se o arquivo para que se mude o modo de operação
    hf = h5py.File('test_data.h5', 'w')
    hf.create_dataset("test_dataset", data=data)
    hf.close()

    # Consertar erro do acesso ao arquivo
    hf = h5py.File('test_data.h5', 'r+')
    b = hf['test_dataset'][:]
    '''
    Operações a serem feitas nos dados:
        - Transformar o array em matriz quadrada
        - Pensar se esse deve ser um método chamado fora da def
          ou se deve ficar aqui dentro
          Adaptar a função de baixo
    '''
    return b
    np.allclose(a, b)
    h5f.close()

def array_to_2d(array):

    """
            Parameters
            ----------
            array : array (1xn)
                array containing the signals on a file, on a channel

            Returns
            -------
            - C: 2d array (nxn)
                This array represents the signal on squared format with or not zeropadding to match square format
            - d: int
                This integer represents the amount of zeropadding added to the matrix to match squared format
    """

    import numpy as np
    import math

    a = array.size
    b = math.ceil(math.sqrt(a))
    c = b*b
    B = np.pad(array, (0, c-a), 'constant')
    C = B.reshape(int(b), int(b))
    d = c-a
    return C,d

def matrix_to_im(matrix):

    """
            Parameters
            ----------
            matrix : array (nxn)
                This array represents the signal on squared format with or not zeropadding to match square format

            Returns
            -------
            - C: 2d array (nxn)
                This array represents the signal on squared format with or not zeropadding to match square format
            - d: int
                This integer represents the amount of zeropadding added to the matrix to match square format
    """

    import numpy as np
    from PIL import Image
    import matplotlib.pyplot as plt

    img = Image.fromarray(matrix, 'L')
    plt.imshow(img, cmap="gray")
    plt.show()
    img.save('test.png')

def tensor(list_edf, mode="combined"):
    import pyedflib
    import numpy as np
    import math
    from PIL import Image

    """
    Parameters
    ----------
    list : list
        list containing all the edf file names on the path.
    mode : str, "single" or "combined"
        "single": the function will create a matrix for each edf file
        "combined": the function will create a matrix combined with all edf files available on the path

    Returns
    -------
    tensor
    """
    chn = 0
    str = ''.join(list_edf)
    n = len(list_edf)
    assert mode == "single" or mode == "combined", "Mode Error: mode not chosen properly!"

    if mode == "single":
        for i in list_edf:
            print(list_edf.index(i))
            [signals, signal_headers, header] = pyedflib.highlevel.read_edf('/Users/joselito/ENV1/edf_file/' + i,
                                                                            ch_nrs=0, digital=True)
            matrix = signals
            a = math.sqrt(signals.size)
            a = math.ceil(a)
            b = signals.size - a * a
            c = np.zeros((b), dtype=int)
            # matrix = np.vstack((matrix,c))
            print(matrix.size, c.size)
            matrix_2d = np.concatenate([matrix, c])
            img = Image.fromarray(matrix_2d, 'L')
            img.show()
            print(i)
    return img

    """
    Percorrer os arquivos edfs ok
    Extrair as colunas ok
    Colocar cada uma em uma matrix
    Concatenar cada uma
    Retornar a matrixzona
    """

    """
    extrair as matrizes
    perguntar se quer matriz de cada arquivo ou se quer de todos
        caso queira de cada arquivo - OK
            verificar cada arquivo possui o mesmo tamanho
                se forem, criar as 23 matrizes aka um tensor
                    retornar tensor e tamanho de zeropadding em cada arquivo que será nulo
                caso não sejam
                    pegar o tamanho da maior
                    preencher as outras de zero
                        retornar tensor e tamanho de zeropadding em cada arquivo que será não nulo

        caso queira uma matriz com todos os valores de um canal
            Varrer a list de edf's
                concatenar todas
                verificar se o número é raíz quadrada
                    se for
                        reshape para sqrt(size da matriz) 
                            retornar o tensor e o tamanho de zeropadding no arquivo
                    se não for
                        arredonde sqrt(size) para ceil
                        zero padding
                        reshape para ceil.sqrt(size)
                            retornar o tensor e o tamanho de zeropadding no arquivo

    """
