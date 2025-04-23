import ccxt
import pandas as pd
import matplotlib.pyplot as plt
import pprint
binance = ccxt.binance()
markets = binance.load_markets()
symbols = [moedas["symbol"] for moedas in markets.values()] ## cria uma lista com "moedas" associadas aos simbolos(pares) no market.values()
timeframe = "1w"
since = binance.parse8601('2017-01-01T00:00:00Z') ## seta uma data inical em formato parse8601 em 'timestamp'

def apresentacao():
    pprint.pprint(f"coin options are {symbols}")
    print("\nThis script allows the extraction, normalization and visualization of data regarding 2 or more crypto pairs.")
    print("\nIt permits better analisys between crypto pairs, \nthus enabling opportunities for financial strategies such as long/short and leveraging")
    print("\nWhen getting yout crypto utilize preferably /stablecoin ")
    print("Scroll upwards to see all available coins")
    return apresentacao
def puxar_tickers(a=None, b=None): ## especifica os dois pares que deseja comparar
    
    print("\Model(crypto/stable), as exemplified at the beggining")
    a = str(input("First pair you want to compare?: ")).upper()
    b = str(input("Second pair you want to compare?: ")).upper()
    return a, b

    
def to_df(): ## puxa as informações ohlcv e coloca num dataframe, renomeando as colunas para melhor visualização
        moeda1 = binance.fetch_ohlcv(a, timeframe, since)
        moeda2 = binance.fetch_ohlcv(b, timeframe, since)
        df1 = pd.DataFrame(moeda1)
        df2 = pd.DataFrame(moeda2)
        df1.columns = ["Data", "open", "max", "low", "close", "volume"]
        df2.columns = ["Data", "open", "max", "low", "close", "volume"]
        df1["Data"] = pd.to_datetime(df1["Data"], unit="ms")
        df2["Data"] = pd.to_datetime(df2["Data"], unit="ms")

        print(df1)
        print(df2)
        
        return df1, df2
       





def merge_normal(df1, df2): ## junta os dois dfs na coluna "Data"  com o o modo "outer", juntando tudo.
    merged = pd.merge(df1,df2, on="Data", how="outer")
    merged = merged.fillna(0)
    return merged



def normalizar(resul):
    colunas = resul[[a, b]]
    colunas = colunas.replace(0, 1)
    normlizads = (colunas - colunas.min()) / (colunas.max() - colunas.min()) ## método min/max evita com que criptos mto grandes baguncem a escala
    normlizads += 1 ## faz com q a escala comece a partir de 1, e não de 0, desse modo facilitano a compreensão da proporção
    
    return normlizads



def plotar(normal): 
    plt.ion() ## liga o modo interativo do pyplot permitino plotar mais de um grafico
    normal.plot()
    plt.plot()
    return normal

def pedir_loc(ilo=None): ## pede uma data para visualiação do usuario
     print("format Y-m-d")
     ilo = str(input("Want to specify a datetime to visualize the spreads DF [y/n]: ")).lower()
     if (ilo == "y"):
        ilo = str(input("Type your chosen date: "))
        ilo = pd.to_datetime(ilo) ## transforma essa data de str para datetime

        print(f"The datetime is: {ilo}")
     else:
          print("No period specified, continuing...")
          ilo = None          
     return ilo

def calculo_spreads(ilo=None): ## calcula os spreads
     
     normal["spread"] = normal[a] - normal[b]
     normal["spread%"] = (normal["spread"]/ normal[b]) * 100
     spreads = pd.DataFrame(normal)
     spreads["spread%"] = spreads["spread%"].apply(lambda x: f"{x:2f}%")
     if (ilo != None):     
        pprint.pprint(spreads.index.tolist())
        print(spreads.loc[ilo])
     return spreads




def datas_disponiveis(spreads):
     datas = pprint.pprint(spreads.index.tolist())
     return datas




     
      
  
apresentacao()
while True:
        ilo = None
        a,b = puxar_tickers()
        df1, df2 = to_df()
        resul = merge_normal(df1,df2)
        resul = resul.rename(columns={"close_x":a, "close_y":b})
        print(resul)
        print(resul.columns)
        resul.index = resul.Data
        normal = normalizar(resul)
        print(normalizar(resul))
        plotar(normal)
        spreads = calculo_spreads()
        datas = datas_disponiveis(spreads)
        ilo = pedir_loc(ilo)
        spreads = calculo_spreads(ilo)

        continuar = str(input("Want to plot other graph? (y/n): ")).lower()
        if(continuar != "y"):
             break
        
    

     



