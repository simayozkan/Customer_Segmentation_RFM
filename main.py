#Customer Segmentation with RFM
#The dataset is not shared because it's exclusive to Miuul Data Science Bootcamp
#Online Store

#Variables :
#InvoiceNo: Invoice number. "C" means returned
#StockCode: Product code
#Description: Product name
#Quantity: Product number
#InvoiceDate: Invoice date and time
#UnitPrice: Product price
#CustomerID: Unique customer number
#Country: Country name (Where customer live)



import datetime as dt
import pandas as pd

df_ = pd.read_excel("datasets", sheet_name="Year 2009-2010")

#Copy of dataframe
df = df_.copy()

#First look to dataframe
df.head()

df.shape

#Check for null values
df.isnull().sum()

#Create "Total Price"
df["TotalPrice"] = df["Quantity"] * df["Price"]

#For each "Invoice", sum of "Total Price"
df.groupby("Invoice").agg({"TotalPrice": "sum"}).head()

#Drop null values
df.dropna(inplace=True)

#"C" represents returned invoices. Do not include in the dataset for further research
df = df[~df["Invoice"].str.contains("C", na=False)]

#Calculating RFM Metrics

#Last invoice date
df["InvoiceDate"].max()

#2 days added to the data set
today_date = dt.datetime(2010, 12, 11)

type(today_date)

#Calculating RFM metrics
rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days,
                                     'Invoice': lambda Invoice: Invoice.nunique(),
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})
rfm.head()

#Change variable names
rfm.columns = ['recency', 'frequency', 'monetary']

rfm = rfm[rfm["monetary"] > 0]

rfm.shape

#Calculating RFM Scores

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])

# 0-100, 0-20, 20-40, 40-60, 60-80, 80-100

rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

#Recency = 5 and Frequency = 5 (champions)
rfm[rfm["RFM_SCORE"] == "55"]

#Recency = 1 and Frequency = 1 (hibernating)
rfm[rfm["RFM_SCORE"] == "11"]

#Creating & Analysing RFM Segments

#Give names to RFM
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

rfm[rfm["segment"] == "cant_loose"].head()
rfm[rfm["segment"] == "cant_loose"].index

#Create new dataframe
new_df = pd.DataFrame()
new_df["new_customer_id"] = rfm[rfm["segment"] == "new_customers"].index

new_df["new_customer_id"] = new_df["new_customer_id"].astype(int)

new_df.to_csv("new_customers.csv")

rfm.to_csv("rfm.csv")

#All process is functionalized

def create_rfm(dataframe, csv=False):


    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]


    today_date = dt.datetime(2011, 12, 11)
    rfm = dataframe.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                                'Invoice': lambda num: num.nunique(),
                                                "TotalPrice": lambda price: price.sum()})
    rfm.columns = ['recency', 'frequency', "monetary"]
    rfm = rfm[(rfm['monetary'] > 0)]


    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])


    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                        rfm['frequency_score'].astype(str))



    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }

    rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
    rfm = rfm[["recency", "frequency", "monetary", "segment"]]
    rfm.index = rfm.index.astype(int)

    if csv:
        rfm.to_csv("rfm.csv")

    return rfm

df = df_.copy()

rfm_new = create_rfm(df, csv=True)C
