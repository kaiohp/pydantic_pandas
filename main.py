import pandas as pd
import pydantic

dataframe = pd.read_csv("dados.csv", index_col=False)
dataframe["row_id"] = dataframe.index

class MySchema(pydantic.BaseModel):
    id: int
    name: str
    value: float

erros = {"row_id":[], "error":[]}

for row in dataframe.to_dict(orient="records"):
    try:
        MySchema.model_validate(row)
    except pydantic.ValidationError as e:
        erros["row_id"].append(row["row_id"])
        erros["error"].append(e.json())

dataframe_erros = dataframe[dataframe["row_id"].isin(erros.get("row_id"))]
dataframe_filtrado = dataframe[~dataframe["row_id"].isin(erros)].drop(columns=["row_id"])

print(dataframe_erros, erros["error"], dataframe_filtrado, sep="\n\n")