"""
Nombre del archivo: eda.py
Autores: Montserrat Lopez, Victor Bassas,  Andres  Henao
Descripción: Archivo que contiene código útil para realizar el EDA
            (Exploratory Data Analysis) para el proyecto de curso Data Scientist de la UOC
Creado: 21/11/2024
Versión: 1.0
Correos: cutmountain@uoc.edu, vbassasb@uoc.edu, ahenaoa@uoc.edu
"""

# Función de análisis univariable
def column_explore (x):
    '''
        Función para el Análisis Exploratorio de Datos (EDA) univariable

        Ejemplo de uso:
            column_explore(df['amount'])
    '''
    print(f"- - - - - Begin EDA of feature '{x.name}' - - - - - - - - - - - - - - - - - - ")    
    print("TOTAL NUMBER OF ROWS: ",len(x))
    print("NUMBER OF UNIQUE VALUES:",x.nunique())
    print(f"NUMBER OF UNIQUE VALUES DIVIDED BY TOTAL VALUES: {round((x.nunique()/len(x)*100),2)}%")
    print(f"PERCENTAGE OF NAN VALUES IS: {round(100*(x.isnull().sum() / len(x)),2)}%")
    print("COLUMN DATA TYPE: ",x.dtype)
    print("COLUMN UNIQUE VALUES: \n",x.unique())
    print("VARIABLE WEIGHT WITHIN THE TOTAL OF THE COLUMN: \n", round((x.value_counts() / x.value_counts().sum())*100,2))
    print("- - - - - End - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")