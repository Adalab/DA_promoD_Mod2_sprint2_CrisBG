import requests
import pandas as pd
import numpy as np
import sys
sys.path.append("../")
from src import variables as var
import mysql.connector

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="cris")

class Unis_Countries:
    """_summary_clase para extracción de datos de la API "Universities Hipolabs", utilizando países para la extracción
    """

    def __init__(self, country_list):
        """_summary_constructor de la clase que toma un argumento

        Args:
            country_list (list): lista de países sobre cuyas universidades se quiere consultar
        """

        self.country_list = country_list

    def calling_api(self):
        """_summary_llamada a la API

        Returns:
            _pd.df_: _description_dataframe con los datos de los países solicitados
        """

        dataframe = pd.DataFrame()

        for country in self.country_list:
            
            api_url = f'http://universities.hipolabs.com/search?country={country}'
            response_country = requests.get(api_url)
            status = response_country.status_code
            status_reason = response_country.reason
            if status == 200:
                print('La peticion se ha realizado correctamente, se ha devuelto el código de estado:', status,' y como razón del código de estado: ', status_reason)
            elif status == 402:
                print('No se ha podido autorizar usario, se ha devuelto el código de estado:', status,' y como razón del código de estado: ', status_reason)
            elif status == 404:
                print('Algo ha salido mal, el recurso no se ha encontrado,se ha devuelto el código de estado:', status,' y como razón del código de estado: ', status_reason)
            else:
                print('Algo inesperado ha ocurrido, se ha devuelto el código de estado:', status,' y como razón del código de estado: ', status_reason)

            dataframe = pd.concat([dataframe, pd.DataFrame(response_country.json())], axis = 0)
    
        return dataframe
    
    def clean(self, dataframe):
        """_summary_homgeneización de columnas y limpieza de columnas redundantes para los datos obtenidos

        Args:
            dataframe (pandas.dataframe): _description_el dataframe obtenido de la llamada a la API con el que se trabaja

        Returns:
            _pandas.dataframe_: _description_ dataframe depurado
        """

        self.dataframe = dataframe

        new_columns = {col: col.replace("-", "_") for col in dataframe.columns}
        dataframe.rename(columns = new_columns, inplace = True)
        dataframe.drop(["domains"], axis = 1, inplace = True)
        return dataframe
    
    def expand_rows(self, dataframe, column):
        """_summary_expansión de los datos de las columnas que lo requieran en filas

        Args:
            dataframe (pandas.dataframe): _description_ dataframe de trabajo
            column (pandas.Series): _description_columna a tratar

        Returns:
            _pandas.dataframe_: _description_dataframe con las líneas aumentadas en función de la columna en la que se ha realizado el expand
        """

        self.dataframe = dataframe
        self.column = column

        dataframe = dataframe.explode(column, ignore_index=True)
        return dataframe
    
    def locating_duplicates_unis(self, dataframe, uni_names):
        """_summary_búsqueda de duplicados

        Args:
            dataframe (pandas.dataframe): _description_ dataframe de trabajo
            uni_names (pandas.Series): _description_columna sobre la que buscar duplicados

        Returns:
            _str_: _description_ frase con el conteo de duplicados de la columna especificada
        """

        self.dataframe = dataframe
        self.uni_names = uni_names

        return f"En la columna {uni_names} hay {dataframe.duplicated(uni_names).sum()} nombres de universidades duplicados."

    
    def erasing_duplicates (self, dataframe, column):
        """_summary_borrado de líneas duplicadas por criterio columna

        Args:
            dataframe (pandas.dataframe): _description_ dataframe de trabajo
            column (pandas.Series): _description_ columna para el criterio de borrado

        Returns:
            _str_: confirmación de borrado
        """

        self.dataframe = dataframe
        self.column = column

        if dataframe.duplicated(column).sum() > 0:
            dataframe.drop_duplicates(subset=[column], inplace = True)
        else:
            pass
        return f"Ahora hay {dataframe.duplicated(column).sum()} duplicados."
    
    def change_null (self, dataframe, column):
        """_summary_reemplazo de nulos

        Args:
            dataframe (pandas.dataframe_): _description_dataframe de trabajo
            column (pandas.Series): _description_columnas para aplicar los reemplazos

        Returns:
            _pandas.dataframe_: _description_dataframe con limpieza de nulos según criterios especificados
        """

        self.dataframe = dataframe
        self.column = column
        
        dataframe[column].replace("None", np.nan, inplace = True)
        dataframe[column].replace(np.nan, "Unknown", inplace = True)
        return dataframe
    
    def incluir_coordenadas (self, dataframe, state_column):
        """_summary_solicitud a API e inclusión en el dataframe de trabajo de coordenadas(latitud, longitud) de los estados del dataframe

        Args:
            dataframe (pandas.dataframe): _description_ dataframe de trabajo
            state_column (pandas.Series): _description_ columna correspondiente a las ubicaciones, estados o provincias

        Returns:
            _pandas.dataframe_: _description_ dataframe original con las columnas añadidas de latitud y longitud
        """

        self.dataframe = dataframe
        self.state_column = state_column

        dataframe[state_column] = dataframe[state_column].replace(var.dict)

        dict_lat = {}
        dict_lon = {}
        for elem in list(dataframe[state_column].unique()):
            location = geolocator.geocode(elem)
            dict_lat.update({elem:(location.latitude)})
            dict_lon.update({elem:(location.longitude)})

    
        dataframe["latitud"] = dataframe[state_column]
        dataframe["longitud"] = dataframe[state_column]

        dataframe["latitud"] = dataframe["latitud"].map(dict_lat)
        dataframe["longitud"] = dataframe["longitud"].map(dict_lon)

        return dataframe

    def create_bbdd(self, nombre_base_datos, contraseña):
        """_summary_creación de base de datos en mysql

        Args:
            nombre_base_datos (string): _description_ nombre de la bbdd
            contraseña (string): _description_ contraseña de acceso al servidor
        
        Comentario: de haber incluido más contenido de la parte de inserción de datos, se habría optado por generar otra clase con 
        esta parte y así, el nombre de la bases de datos y la contraseña estarían definidos en el constructor de esa clase
        """

        self.nombre_base_datos = nombre_base_datos
        self.contraseña = contraseña

        mydb = mysql.connector.connect(host="localhost",
                                       user="root",
                                       password=f'{contraseña}') 
        mycursor = mydb.cursor()
        print("Conexión realizada con éxito")

        try:
            mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {nombre_base_datos};")
            
        except:
            print("La BBDD ya existe")
    
    def create_tables(self, nombre_base_datos, contraseña):
        """_summary_creación de tablas de la base de datos
        """

        for table in var.querys_list:
        
            mydb = mysql.connector.connect(host="localhost",
                                        user="root",
                                        password=f'{contraseña}', 
                                        database=f"{nombre_base_datos}") 
            mycursor = mydb.cursor()
        
            try:
                mycursor.execute(table)
                mydb.commit()
          
            except mysql.connector.Error as err:
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)