# DA_promoD_Mod2_sprint2_CrisBG
Segunda evaluación del módulo 2 de DA

Se han utilizado las siguientes librerías:

NumPy https://numpy.org/
Pandas https://pandas.pydata.org/
sys https://docs.python.org/es/3.10/library/sys.html
requests https://pypi.org/project/requests/
mysql connector https://www.mysql.com/products/connector/
geopy geocoders https://pypi.org/project/geopy/

Como partida de la propuesta de ejercicio, la API "Universities Hipolabs" (http://universities.hipolabs.com/)

Tras la realización del trabajo y la toma de algunas decisiones el repositorio consta de un archivo y dos carpetas de archivos.

La carpeta src contiene dos archivos.py. El archivo variables.py contiene como su nombre indica variables y algún otro contenedor que se utiliza en el archivo de soporte. El archivo soporte.py contiene la clase creada para llevar a cabo los trabajos propuestos. Sobre este archivo:

- El trabajo planteado centraba el criterio selección en países, no en otros datos que pudiera ofrecer la API sobre la que se centraba el ejercicio. Por ello, se ha definido en el constructor de la clase la lista de países a requerir. De esta forma, solo sirve para solicitudes de datos en base al criterio país. 

- Algunos trabajos de limpieza eran bastante específicos de los datos a manejar. Se ha procurado crear las funciones de la forma más universal posible, pero en algún caso para posteriores aplicaciones debería revisarse. 

- En la obtención de coordenadas se ha obviado el tratamiento de las localizaciones recogidas como "unknown", para las cuales geopy si arroja unas coordenadas. En simulaciones individuales puede excluirse pero no parece tener sentido para una función universal cuando no sabemos el tipo de datos a recibir y donde estarán estos "unknown". Por otro lado, en las pruebas individuales, quitarlo de la solicitud de coordenadas supone asumir el retorno de np.nan, que en este caso, ya habían sido previamente limpiados(siempre pueden volver a limpiarse). 

- Tras la obtención de coordenadas se ha seguido un método que se ha considerado más sencillo a la hora de incorporar estos nuevos datos al dataframe original. 

- Se han incluido en la clase la creación de bbdd y de tablas en mysql. Como se comenta en la propia clase, de haber realizado la insercción de datos se habría optado por separar toda esta parte en una clase distinta. 

La carpeta files contiene tres archivos .csv donde se ha guardado el dataframe de trabajo en diferentes momentos del proceso. 

El archivo global.ipynb es un Jupyter Notebook donde se instancia y ejecuta la clase y sus funciones. 




