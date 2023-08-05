from pyspark import Row
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql import DataFrame
from itertools import chain
import pyspark.sql.functions as F
from pyspark import SparkContext

def listcode_check(df, variabel, kodeliste):
    '''
    
    This function checks the values of a variable in a dataframe against a given list of codes
    and makes a new dataframe containing these values, a count of how many times the value occurs
    and a variable indicating whether or not this value existed in the code list or not.
    In addition, the function returns a Boolean variable indicating whether the variable included
    one or more values outside the code list or not.
     
    :param df: Spark dataframe containing variable to be controlled
    :param variabel: variable to be checked against the code list 
    :param kodeliste: list of codes that the variable should be checked against, sent as a Python list
    
    :type df: Spark dataframe
    :type variabel: string 
    :type kodeliste: list
    
    Returns: Boolean variable and a dataframe in that order.
    Boolean variable: A Boolean variable indicating wheteher or not there exists one or more values in
               the variable that did not exist in the codelist.
    Dataframe: A data frame (Spark) consisting of the values found in the variabel,
               the number of times the value occurs and a Boolean value telling wheter or not
               the value exists in the relevant code list or not.
    
    '''  
 
    #Sjekker om parametre er av korrekt format       
    if (isinstance(df, DataFrame)) & (isinstance(variabel, str)) & (isinstance(kodeliste, type([]))):
            
        #Kopierer over spark context og setter opp peker til context som brukes i forbindelse med oppretting av nytt datasett
        sc = SparkContext.getOrCreate()
        sqlContext = SQLContext(sc)
        
        #initialiserer variabler
        sjekk_listedf = []
        sjekk_bol = True
        
        #Grupperer variabelene i datasettet og teller opp instanser av ulike verdier
        koder_df = df.groupby(variabel).count().withColumnRenamed('count', 'antall')
        
        #Går gjennom verdier på variabel og sjekker om de er med i kodeliste, for hver verdi blir det laget en record  
        #Hvis det finnes 1 eller flere verdier som ikke er i kodelisten blir en boolsk verdi (sjekk_bol) satt til False
        for row in koder_df.rdd.collect():
            dRow = {}
            dRow['kode'] = row[variabel]
            dRow['antall'] = row['antall']
            if row[variabel] in kodeliste:
                dRow['i_kodeliste'] = True
            else:
                dRow['i_kodeliste'] = False
                sjekk_bol = False
            sjekk_listedf.append(dRow)
        
        #Oppretter dataframe for resultatet av gjennomgangen ovenfor
        field_kl = [StructField('kode', StringType(), False),\
                        StructField('antall', IntegerType(), True),\
                        StructField('i_kodeliste', BooleanType(), False)]
        schema_kl = StructType(field_kl)
        rdd_sl = sc.parallelize(sjekk_listedf)
        sjekk_df = sqlContext.createDataFrame(rdd_sl, schema_kl)
        
        #Returner opprettet dataframe og boolsk verdi
        return sjekk_bol, sjekk_df
    else:
        #Hvis ikke parametre sendt med funksjonen er korrekt format skrives det ut en feilmelding
        if not (isinstance(df, DataFrame)):
            raise Exception('Første parameter må være en dataframe som har variabelen som skal sjekkes')
            return
        if not (isinstance(variabel, str)):
            raise Exception('Andre parameter må være en string med navnet på variabel som skal sjekkes')
            return
        
        if not (isinstance(kodeliste, type([]))):
            raise Exception('Tredje parameter må være en python liste som inneholder kodelisten variabel skal sjekkes mot')
            return
            
