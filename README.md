# monayvi
Segon projecte Data Science UOC - Business Payments

Autores: Montserrat Lopez, Victor Bassas,  Andres Henao

Descripción: Archivo Readme del proyecto de analisis de la empresa Business Payments

Creado: 27/11/2024
Versión: 1.0  
Correos: cutmountain@uoc.edu, vbassasb@uoc.edu, ahenaoa@uoc.edu

## Estructura de los directorios
### data
Contiene los ficheros .csv originales del proyecto que son:
- cash_request.csv : contiene las peticiones de cash de los clientes y los datos asociados
- fees.csv: contiene las comisiones asociadas a las operaciones de cash request por usuario
- Lexique-Data_Analyst.xlsx : describe los campos de los ficheros anteriores

### notebooks
En esta carpeta se encuentran los ficheros de jupyter notebook utilizados para la elaboración de los análisis y modelos

### utils

Hemos creado este folder para compartir código que se reuse en todo el proyecto.
Funciones en data.py ([data utils]([https://github.com/ahenao/aguacate-aljoan/blob/main/utils/data.py](https://github.com/DataScience-UOC-projects/monayvi/blob/main/utils/data.py))): 
- clase Datasets(): instancia la clase para modificar los datasets
- create_cash_cohorts(): devuelve el nuevo dataframe con los cohhortes para la tabla cash
- get_users_by_cohort(): devuelve un dataframe con número de usuarios por cohorte
- get_original_datasets(): devuelve una tupla con dos dataframes: cash_original y fees_original

Para usar los módulos de utils en scripts se hace 
```
from utils.data import Datasets
```
y para usarlos desde jupyter notebook, hay que agregar el path:

```
import sys, os
sys.path.append(os.getcwd().replace('/notebooks',''))  # Replace '/notebooks' with current directory name
from utils.data import Datasets
```

```
datasets = Datasets()
cash_cohorts = datasets.create_cash_cohorts()
original_cash, original_fees = datasets.get_original_datasets()
users_by_cohort = datasets.get_users_by_cohort()
```
### ini

Contiene el fichero markdown ```enunciado.md``` con el enunciado del proyecto

## Contexto social y económico

Las fechas de estudio coinciden con la explosión de la pandemia de COVID durante el primer trimestre de 2020 y la progresiva recuperación de la actividad en los meses de mayo, junio y julio.
Los intereses para préstamos de dinero interbancario en Europa estaban a tasas negativas y en Estados Unidos y Reino Unido a tasas positivas cercanas al 0%

En esta tabla se muestra el Euribor para el año 2019
![Euribor año 2019](/figures/Euribor2019.png)

Y la tabla correspondiente al año 2020:

![Euribor año 2020](/figures/Euribor2020.png)

En un ejercicio de scrapping básico, hemos obtenido las tablas del euríbor para ser usadas luego posiblemente como variable exógena. Pandas tiene la función de leer tablas html si se encuentran en páginas bien de forma estructuradas:

```
import pandas as pd
link_euribor_2020 = "https://www.euribor-rates.eu/es/tipos-de-interes-euribor-por-ano/2020/"
tablas_2020 = pd.read_html(link_euribor_2020)
euribor2020_df = tablas_2020[0]
euribor2020_df.to_csv("../data/euribor.csv")
```


Para el mercado británico y americano el gráfico muestra el valor del indice LIBOR , equivalente al Euribor para el Euro.

![Libor año 2020](/figures/Libor2020.png)

Valores negativos del índice Euribor implica que _se debería devolver menos dinero que el principal solicitado_. Con intereses negativos un impago de una parte del capital solicitado, no tiene tanto impacto para el banco como en el caso de intereses positivos.

## Análisis e investigaciones de los datos en original_cash y original_fees

**Análisis de operaciones en el tiempo**

En los graficos se presentan las distribuciones de solicitudes por hora y por día. Se encuentra un pico de solicitudes para los martes (una disminución en fines de semana), así como un pico de solicitudes a las 16:00 y una distribución de solicitudes centrada en las horas laborables. Esto nos indica que agregar features como hora y día de la semana puede proveer información a modelos de predicción.La codificación de los días de semana es de 0-6, siendo 0: lunes y 6: Domingo.

![Solicitudes por dia](figures/days_cash.png)

![Solicitudes por hora](figures/hours_cash.png)

## Modelos de clasificación

Hemos encontrado en la tabla original de cash, que alrededor del 70% de status corresponde a money_back y cerca a un 30% a rejected. Las operaciones rejected (en su ayoría) han pasado por un proceso de revisión manual: Una incidencia. Esto implica dedicación horaria de personal que podría dedicarse a tareas que puedan destinarse a mejorar la rentabilidad del negocio (estrategias de mercado, análisis de mercado, etc). Así que un modelo de clasificación que permita predecir si una transacción tiene alta probabilidad de ser cancelada podría limitar el número de incidencias y repercutir en las ganancias del negocio (sin reducir el personal de la empresa, sino haciendo que sus tareas sean de mayor impacto: Automatizar tareas repetitivas).

Hemos comenzado por hacer feature engineering de las variables temporales relevantes, y hemos filtrado las variables de amount, status (0: money_back, 1: rejected), ctranstype_regular (1:regular, 0:instantánea). Además hemos añadido la variable exäogena del euribor para probar su importancia. Además de que es una variable de la cual se hace forecast y puede usarse para predicciones futuras.

![Datos para clasificación](figures/cash_clasifica1.png)

Hemos intentado dos modelos de clasificación: Regresión Logística, y GradientBoosting. Hemos hecho una optimización de hiperparámetros para clasificar el status. En el caso de regresión logística hemos variado la regularización. En el caso de GradientBoosting hemos optimizado número de estimadores, learning_rate, max_depth de los arboles de decisión, min_samples_split. A continuación se muestran los mejores hiperparámetros.

![hiperparametros](figures/hyperparameter_1.png)

Y los resultados de las matrices de confusión, así como de la importancia de las variables de clasificación. Hemos además añadido un análisis de valores Shapley (concepto que nace de la teor¡ia de juegos, para asignar la importancia de cada variable en el rendimiento global del model).

![importancia log](figures/logimp.png)

![importancia gb](figures/gbimp.png)

![confusion_matrix](figures/confmatlgb.png)

![shap](figures/shap.png)

Algunas conclusiones:
- La variable exogena euribor aun no tiene un papel de alta importancia, aunque es relevante en los arboles de decision. Puede conservarse, y refinarse a futuro
- Logistic regression da mucha mas importancia el mes, se necesitan mas datos temporales o tener en cuenta eliminarla del modelo
- Amount grandes de prestamos tienen relativamente bajo impacto en el status. Juegan mas variables como el dia de la semana y la hora
- La hora (shapley) tiene un efecto claro en el arbol de decision: A altas horas se hace mas importante su peso para que el status sea rechazado

## Modelos de aprendizaje no supervisado - clustering como herramienta de segmentacion de clientes

Hemos hecho una prueba de segmentacion de clientes, para dar información al departamento de estrategia y mercadeo para retener buenos clientes y captar nuevos potenciales. Hemos hecho pruebas usando variables tanto de cash como de fees: número de peticiones aprobadas, cantidad total prestada, fees totales pagados, para los usuarios activos.
hemos probado un PCA: Principal component analysis (que puede ser mas facil de interpretar) y un modelo t-SNE que es no lineal.

![PCAseg](figures/pcaseg.png)

![tsneseg](figures/tsneseg.png)

EL algoritmo propone tres categorías de clientes. Debemos definir junto a los expertos del negocio la correspondencia de estas clases (premium, platinum, gold?)

Aún se pueden hacer mejoras y análisis junto a los expertos de negocio para optimizar esta solución algorítimica.

## Análisis de Regresión para Beneficios obtenidos de fees

Centrándonos en maximizar el beneficio para la empresa (Business Payments), nos fijamos en los 100 clientes que han generado mayor beneficio a lo largo del año. Para estos clientes, obtenemos el total de dinero prestado, así como el total de beneficio generado a partir de fees.

![Total amount fees](figures/reg_sum_amounts_table.png)

Tras la codificación mediante get_dummies() y LabelEncoder(), vemos la posible correlación entre las distintas variables.

![Correlation matrix](figures/reg_sum_amounts_corr_matrix.png)

A priori tendría sentido que una mayor cantidad de dinero prestado generase mayor beneficio, ya sea por tratarse de transacciones instantáneas como por el hecho de que a mayor número de transacciones, más probable es que alguna de ellas sufra un incidente de pago y por tanto se cobre una fees.

Generamos un modelo de regresión lineal mediante el cual queremos observar qué características son las que definen a los mejores usuarios, i.e. los que dan más beneficios. Para ellos, tomamos los datos agrupados para todos los meses disponibles except el último, octubre de 2020, para el cual generaremos una predicción.

Al comparar el modelo con los valores reales, comprobamos que la capacidad de predicción es bastante buena.

![Prediction vs Real Values](figures/reg_sum_amounts_y.png)

De hecho, esto queda reflejado en los parámetros que nos indican la calidad del modelo predictivo:

<img src="./figures/reg_sum_amounts_r2.png" alt="R^2 y MSE" width="350" style="margin-left:50px"/>

![Residue](figures/reg_sum_amounts_residuo.png)

Los coeficientes obtenidos nos indican la importancia de cada una de las variables: al contrario de lo que parecía, `amount` no es demasiado significativa, mientras que sí lo son el momento _año/mes_ en que se realizó la solicitud y sobre todo si la cuota se cobró antes o después `fee_charge_moment` de recibir el préstamo.

<img src="./figures/reg_sum_amounts_coefs.png" alt="Intercepto y Coeficientes para la Regresión Lineal" width="350" style="margin-left:50px"/>

Así pues, parece que los préstamos en los que se cobró la cuota después (`after`), son los más provechosos. Casualmente, vemos que esto coincide con los préstamos de recepción inmediata (`instant`), que son los más numerosos.

<img src="./figures/eda_fee_charge_moment.png" alt="Desglose fee_charge_moment en relación a transfer_type" width="330" style="margin-left:50px"/>

Si mostramos estos coeficientes de forma gráfica, será más evidente.

![Coeficientes ordenados según el valor absoluto](figures/reg_sum_amounts_coefs_abs.png)

Aplicando una regulación de Ridge, obtenemos una leve mejora en el MSE del conjunto de prueba (test), pero casi imperceptible.

![Coeficientes Ridge ordenados según el valor absoluto](figures/reg_sum_amounts_coefs_abs_ridge.png)

## Análisis de Regresión ampliando las características

Realizamos ahora el mismo ejercicio pero con un conjunto ampliado de características, aquellas que pensamos que pueden tener un impacto significativo en el pronóstico de beneficios.

La matriz de correlación para las características seleccionadas tiene el siguiente aspecto.

![Correlation matrix](figures/reg_corr_matrix.png)

Destaca un cero rotundo en la correlación entre el `status` con valor `money_back` y la hora de solicitud del préstamo.

En este caso, la calidad del modelo de regresión lineal nos muestra un mejor ajuste del conjunto de entrenamiento (0.94 en lugar de 0.93) pero un peor ajuste del conjunto de pruebas (0.81 en lugar de 0.83).

<img src="./figures/reg_r2.png" alt="R^2 y MSE" width="350" style="margin-left:50px"/>

Esto se ve reflejado en las gráficas de predicción vs valores reales, y residuo.

![Prediction vs Real Values](figures/reg_sum_amounts_y.png)

![Residue](figures/reg_sum_amounts_residuo.png)

Los coeficientes para cada una de las características son:

<img src="./figures/reg_coefs.png" alt="Intercepto y Coeficientes para la Regresión Lineal" width="450" style="margin-left:50px"/>

Observamos que el hecho de tener una cuenta activa (`existing_account`) es determinante en el cálculo de la predicción. También, que el `transfer_type` no sea de tipo `regular` sino `instant`. Para el resto de coeficientes, una visión gráfica nos dará información más interpretable.

![Coeficientes ordenados según el valor absoluto](figures/reg_coefs_abs.png)

![Coeficientes Ridge ordenados según el valor absoluto](figures/reg_coefs_abs_ridge.png)

Parece que el tipo de adelanto es el factor más determinante para la obtención de beneficions, y esto cuadra con el comportamiento de los usuarios en cada cohorte: a cohortes más nuevas, mayor preferencia por el tipo de adelanto isntantáneo, que requiere el pago de una quota.

![Tipo de adelante según cohorte](figures/metricas_tipo_adelanto.png)