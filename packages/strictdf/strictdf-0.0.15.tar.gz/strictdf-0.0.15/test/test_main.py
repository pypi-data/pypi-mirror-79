import pytest
import pandas as pd
from test import StrictDataFrame

uno = {'dato':  [1, 2, 3, 4, 5, 'Hola']}
df_uno = pd.DataFrame (uno, columns = ['dato'])
sdf_uno = StrictDataFrame(df_uno)

dos = {'dato':  [1, 2, 3, 4.5, 5.5, 6.6, 7.7, 8.8, 9.9]}
df_dos = pd.DataFrame (dos, columns = ['dato'])
sdf_dos = StrictDataFrame(df_dos)

tres = {'dato':  [1, 'Dos', 'Tres', 'Cuatro', 'Cinco', 'Hola', 'Chau']}
df_tres = pd.DataFrame (tres, columns = ['dato'])
sdf_tres = StrictDataFrame(df_tres)

df_pyspark = {'dato':  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
             'texto':  ['Uno', 'Dos', 'Tres', 'Cuatro', 'Cinco', 'Seis', 'Siete', 'Ocho', 'Nueve', 'Diez']}
df_pyspark_ = pd.DataFrame (df_pyspark, columns = ['dato', 'texto'])
sdf_df_pyspark  = StrictDataFrame(df_pyspark_)

@pytest.mark.parametrize(
    "data, expected", [
        (sdf_uno, {'dato': 'int64'}),
        (sdf_dos, {'dato': 'float64'}),
        (sdf_tres, {'dato': 'str'}),
    ]
)

def test_dtype(data, expected):
    test = data.dtypes
    assert test == expected


@pytest.mark.parametrize(
    "df_, expected", [
        (sdf_uno, 'DataFrame having shape (6, 1) 0 rows removed from original'),
        (sdf_dos, 'DataFrame having shape (9, 1) 0 rows removed from original'),
        (sdf_tres, 'DataFrame having shape (7, 1) 0 rows removed from original')
    ]
)

def test_report(df_, expected):
    test = df_.report()
    assert test == expected


@pytest.mark.parametrize(
    "df_, expected", [
        (sdf_df_pyspark, 'DataFrame[dato: bigint, texto: string]')
    ]
)

def test_to_spark(df_, expected):
    test = df_.to_spark()
    assert str(test) == expected
