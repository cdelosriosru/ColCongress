## *******El Parlamento de Santos*******

David Vargas-Mogollón | 2019-11-21

**En el folder:**
-

 1. Este readme explicando el proyecto y sus resultados
 2. Folder code:
		 1. scrapping_Camara_SenadoV3.py : codigo que realiza el scrapping
		 2. Data_clean_up.py : Codigo que une, corrige y organiza los datos Raw.
		 3. data_for_analysis.py  : Código que crea variables adiconales (dummies en genral) para gráficar en Tableau

 3. Folder data:
		 1. Raw: contiene los resultados del web-scrapping sin ninguna modificación.
		 2.  Clean: Datos corregidos y organizados. Ideales para revisar y comprender los datos.
		 3.  For analysis: datos para usar en Tableau y generar las gráficas.


**Descripción y motivación**
-------------------------------------------

Congreso Visible contiene una gran cantidad de información detallada sobre las votaciones y proyectos que toman lugar en el parlamento colombiano. Para este proyecto tomando ventaja de herrameintas de web-scrapping extraje la infomación de las todas las votaciones que tomaron lugar en ambas cámaras (Senado y Cámara de Representantes) duarnte el perido Santos II (2014-2018); esto consiste en 3338 votaciones a lo largo de cuatro años.

**Que motiva el proyecto:**

Pese a que congreso visible ofrece toda la información de manera abierta, no todas las posibles relaciones y usos son aplicables desde su página. Mi intención es proveer una base de datos comprenhensiva que permita entender de forma más sistematica el comportamiento del parlamento durante estos años. Más aún de tener información relevante para evaluar a cada uno de los parlamentarios y partidos, como votan y como se alinea. Algunas preguntas que busco responder son:

 - ¿Cómo cambia la dinamica del parlamento a lo largo que avanza el periodo?
- ¿Cómo son en general los resultados de las votaciones?¿Es verdad que muchas no se llevan a cabo porque no tienen quorum?
- ¿Qué clase de votaciones ocupan más al parlamento?
- ¿Qué se debate más?
- ¿Como se difrencian los partidos? ¿ Quienes proponen?¿Quienes votan?¿Quienes se abstienen?
- ¿Cuales son los congresistas más activos?¿Quienes los menos activos?¿Es grande la diferencia?
- ¿Cómo cambia el soporte a un proyecto segun quién lo propone?

**Metodología**
-----------

**a) Scrapping**

El scrapping se llevo a cabo de la siguiente forma:

1) De la primera pagina de las votaciones para el periodo se determina el número de paginas a visitar. Hasta la fecha de hoy son 668, sin embargo el código está diseñado para ajustarse a algún cambio.

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/1.png)

2) Se visita cada pagina y se extraen los links de cada una de las votaciones allí presentes. Cada página contiene el link a 5 votaciones distintas (a excepción de la última)

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/2.png)

3) Posteriormente se visita cada una de las páginas de cada votación, extrae el nombre de la votación, su estatus, la cámara(s) donde se debatio, las comisiones, la fecha, el tipo y el numero de votos y abstenciones (si están disponibles). Admás se abre el la lista de votos haciendo click sobre "ver más" para ver el reporte detallado.

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/3.png)

4) Con la infomación detallada se determina quien voto, su partido y como voto. Además se determina quien se abstuvo y su partido

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/4.png)

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/5.png)

5) Luego se captura el link del proyecto (si existe) y se visita ese link.

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/6.png)

6) De la página del proyecto se extre, el titulo, los autores (y su partido), su partido, y los tags.

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/7.png)

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/8.png)
![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/9.png)

**b) Limpieza**

Una vez se recolectan los datos estos son organizados y corregidos. En categorias que no son completamente capturadas pero que se pueden calcular de otra forma estás son completadas. Este es el caso del número de votos y de abstenciones. A parte de las bases limpias algunas bases para facilitar análisis son genradas.

**c) Análisis**

Ya que los datos eran abunsdantes y el análisis predominantemente exploratorio se hace uso de Tableau para hacer gráficos que puedan dar respuesta a las preguntas (o al menos alguna indicación sobre las mismas)

**Resultados**

Se evidencia una fuerte caída del número de votos a lo largo del mandato. Con un pico en el segundo año.

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/Picture1.png)

Eso es cierto en todas las cámaras. Además en general el Senado parace más activo.

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/Picture2.png)

Contrario a lo que algunas personas piensan, al menos durnate este periodo, la contidad de debates que no se llevan a cabo por falta de quorum es pequeño.

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/Picture3.png)

Aunque los proyectos de ley contituyen la mayoría de los debates, los impedimentos ocupan casi la misma cantidad del total.

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/Picture4.png)

Los debates se concentaron de forma importante en discusiones de 'Balance institucional' y de 'Equilibrio de poderes'.

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/Picture5.png)

El ejecutivo realizo la gran mayoría de las propuestas de proyectos de ley, seguido por mucho por el partido de gobierno.

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/Picture6.png)

Esto es consistente en el tiempo.

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/Picture7.png)

Hay casi el mismo número de abstenciones que de votos.

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/Picture8.png)

Los congresitas más activos son:

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/Picture9.png)

Los menos activos tienen diferencias importantes con los más activos.

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/Picture10.png)

Muchos de los más activos, también votan activamente (no se abstienen)

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/Picture11.png)

Sin embargo otros tambien se abstienen seguido:

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/Picture12.png)

De los representates de cada partido que participan en un voto dado, menos de la mitad (en casi todos los casos) votan a favor

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/Picture13.png)

El apoyo a las votaciones parece variar de forma importante dependiedo de los partidos que son autores.

![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/Picture14.png)
![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/Picture15.png)
![alt text](https://github.com/davidlvargas/MCPP_david.vargas/blob/master/David_Vargas_MCPP_final/img/Picture16.png)
