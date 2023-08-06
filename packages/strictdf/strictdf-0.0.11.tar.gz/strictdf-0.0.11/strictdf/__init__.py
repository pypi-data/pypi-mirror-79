import pandas as pd
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import StructType, StructField, StringType

class StrictDataFrame:
    def __init__(self, df):
        self.df = df
        self.old_df = df.copy()
        self.new_df = df.dropna()
        self.dtypes = self._dtypes()

    def report(self):
        text = f"DataFrame having shape '{self.new_df.shape}'({self.old_df.shape[0] - self.new_df.shape[0]}) rows removed from original"""
        return text
    
    def _dtypes(self):
        columnas = self.new_dataframe.columns.to_list()
        df_final = pd.DataFrame(columns= ['columna', 'tipo_dato', 'total', 'checkbool'])

        def check_int(x):
            if isinstance(x,int):
                return 'int64'
            elif isinstance(x,float):
                if (x % 1)==0:
                    return 'int64'
                else:
                    return 'float64'
            else:
                try:
                    y = float(x)
                    if (y % 1)==0:
                        return 'int64'
                    else:
                        return 'float64'
                except:
                    return 'str'

        def check_bool(lista):
            y = [item for item in lista if (item != 1 and item !=0)]
            if(len(y)==0):
                return 'bool'
            else:
                return 'no bool'

        for x in columnas:
            data = self.new_dataframe[x].apply(lambda x : check_int(x)).value_counts()
            for y in range (0, len(data)):
                new_row = {'columna': x, 'tipo_dato': data.index[y], 'total': data[y], 'checkbool': ''}
                df_final = df_final.append(new_row, ignore_index=True)

        df_final['checkbool'] = df_final['columna'].apply(lambda x: check_bool(self.new_df[x]))
        df_final = df_final[df_final.groupby('columna').total.transform('max') == df_final['total']]
        df_final.loc[df_final['checkbool'] == 'bool', 'tipo_dato'] = 'bool'
        df_final = df_final[df_final.columns.to_list()[:-2]]
        df_final = df_final.reset_index(drop=True)
        df_final = df_final.set_index('columna')
        return df_final.to_dict(orient='dict')['tipo_dato']


    def to_spark(self):
        spark = SparkSession.builder.getOrCreate()
        spark_df = spark.createDataFrame(self.new_df)
        return spark_df