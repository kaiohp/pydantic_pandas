import pandas as pd
import pydantic

dataframe = pd.read_csv("dados.csv", index_col=False)
dataframe["row_id"] = dataframe.index

class MySchema(pydantic.BaseModel):
    id: int
    name: str
    value: float

erros = []
dataframe_erros = pd.DataFrame()

for row in dataframe.to_dict(orient="records"):
    try:
        MySchema.model_validate(row)
    except Exception as e:
        erros.append(row.copy())


dataframe_erros = pd.DataFrame(erros)
dataframe_filtrado = dataframe[~dataframe["row_id"].isin(dataframe_erros["row_id"])].drop(columns=["row_id"])

print(dataframe_erros, dataframe_filtrado, sep="\n\n")