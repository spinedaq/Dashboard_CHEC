import os
import shutil
import random
import datetime
import operator
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import date
from datetime import datetime
import matplotlib.pyplot as plt


def load_data():
    
    eventos_interruptor = pd.read_pickle("C:/Users/lucas/OneDrive - Universidad Nacional de Colombia/PC-GCPDS/Documentos/data/Eventos_interruptor.pkl")

    eventos_tramo_linea = pd.read_pickle("C:/Users/lucas/OneDrive - Universidad Nacional de Colombia/PC-GCPDS/Documentos/data/Eventos_tramo_linea.pkl")

    eventos_transformador = pd.read_pickle("C:/Users/lucas/OneDrive - Universidad Nacional de Colombia/PC-GCPDS/Documentos/data/Eventos_transfromador.pkl")

    return eventos_interruptor, eventos_tramo_linea, eventos_transformador

def graph_probabilty(criterias, data_total, probility_text, count):

    if count == 0:

        # Verifica si la carpeta existe
        if not os.path.exists('./outputs'):
            print(f"La carpeta {'./outputs'} no existe.")
            return
        
        # Itera sobre todos los elementos dentro de la carpeta
        for elemento in os.listdir('./outputs'):
            ruta_elemento = os.path.join('./outputs', elemento)
            try:
                # Si es un archivo, lo elimina
                if os.path.isfile(ruta_elemento) or os.path.islink(ruta_elemento):
                    os.remove(ruta_elemento)
                # Si es una carpeta, elimina la carpeta completa
                elif os.path.isdir(ruta_elemento):
                    shutil.rmtree(ruta_elemento)
            except Exception as e:
                print(f"No se pudo eliminar {ruta_elemento}. Error: {e}")


    match criterias[0]:

        case 'Eventos Interruptor':

            data_frame_select = data_total[0]

            for i in range(1,5):
                
                if criterias[i][0] != '':

                    match criterias[i][0]:

                        case 'seleccion':

                            data_frame_select = data_frame_select[data_frame_select[criterias[i][1]] == criterias[i][2]]

                        case 'rango_num':

                            operators = {
                                            '<': operator.lt,
                                            '>': operator.gt,
                                            '==': operator.eq,
                                            '<=': operator.le,
                                            '>=': operator.ge,
                                            '!=': operator.ne
                                        }
                            
                            data_frame_select = data_frame_select[operators[criterias[i][2]](data_frame_select[criterias[i][1]], float(criterias[i][3]))]

                        case 'fecha':

                            data_frame_select = data_frame_select[(data_frame_select[criterias[i][1]] >= criterias[i][2]) & (data_frame_select[criterias[i][1]] <= criterias[i][3])]

                        case _:

                            None

            plt.figure(figsize=(10, 6))
            sns.histplot(data_frame_select[criterias[-1]], kde=True, color='blue', bins=30)
            plt.xlabel(str(criterias[-1]))
            plt.ylabel('Frecuencia/Densidad')
            plt.savefig("./outputs/probability_graph_"+str(count)+".png")
        
        case 'Eventos Tramo':

            data_frame_select = data_total[1]

            for i in range(1,5):
                
                if criterias[i][0] != '':

                    match criterias[i][0]:

                        case 'seleccion':

                            data_frame_select = data_frame_select[data_frame_select[criterias[i][1]] == criterias[i][2]]

                        case 'rango_num':

                            operators = {
                                            '<': operator.lt,
                                            '>': operator.gt,
                                            '==': operator.eq,
                                            '<=': operator.le,
                                            '>=': operator.ge,
                                            '!=': operator.ne
                                        }
                            
                            data_frame_select = data_frame_select[operators[criterias[i][2]](data_frame_select[criterias[i][1]], float(criterias[i][3]))]

                        case 'fecha':

                            data_frame_select = data_frame_select[(data_frame_select[criterias[i][1]] >= criterias[i][2]) & (data_frame_select[criterias[i][1]] <= criterias[i][3])]

                        case _:

                            None


            plt.figure(figsize=(10, 6))
            sns.histplot(data_frame_select[criterias[-1]], kde=True, color='blue', bins=30)
            plt.xlabel(str(criterias[-1]))
            plt.ylabel('Frecuencia/Densidad')
            plt.savefig("./outputs/probability_graph_"+str(count)+".png")

        case 'Eventos Transformador':

            data_frame_select = data_total[2]

            for i in range(1,5):
                
                if criterias[i][0] != '':

                    match criterias[i][0]:

                        case 'seleccion':

                            data_frame_select = data_frame_select[data_frame_select[criterias[i][1]] == criterias[i][2]]

                        case 'rango_num':

                            operators = {
                                            '<': operator.lt,
                                            '>': operator.gt,
                                            '==': operator.eq,
                                            '<=': operator.le,
                                            '>=': operator.ge,
                                            '!=': operator.ne
                                        }
                            
                            data_frame_select = data_frame_select[operators[criterias[i][2]](data_frame_select[criterias[i][1]], float(criterias[i][3]))]

                        case 'fecha':

                            data_frame_select = data_frame_select[(data_frame_select[criterias[i][1]] >= criterias[i][2]) & (data_frame_select[criterias[i][1]] <= criterias[i][3])]

                        case _:

                            None

            plt.figure(figsize=(10, 6))
            sns.histplot(data_frame_select[criterias[-1]], kde=True, color='blue', bins=30)
            plt.xlabel(str(criterias[-1]))
            plt.ylabel('Frecuencia/Densidad')
            plt.savefig("./outputs/probability_graph_"+str(count)+".png")

        case _:

            return None
