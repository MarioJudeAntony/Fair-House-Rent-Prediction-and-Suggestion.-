# Loading the libraries
import streamlit as st
import numpy as np
import pickle
import pandas as pd
from streamlit_option_menu import option_menu
import time
pd.set_option('display.max_rows', None)

#Loading the dataset

data=pd.read_excel("C:/Users/mario/OneDrive/Desktop/Mini Project/FInal model/final dp.xlsx")
sugg=pd.read_excel("C:/Users/mario/OneDrive/Desktop/Mini Project/FInal model/Chennaic.xlsx")
sugg["Locality"]=sugg["Locality"].str.lower()
data["TO"]=data["TO"].str.lower()  
data["TO"]=data["TO"].str.strip()

#Loading the model
model=pickle.load(open('C:/Users/mario/OneDrive/Desktop/Mini Project/FInal model/finalized_model.sav','rb'))

#Function to predict

def predict_price(seller,bedroom,layout,property_type,locality,area,furnishing,bathroom):
    se,lay,typ,loc,fu=0,0,0,0,0,
    #for seller
    if seller=="OWNER":
        se=0
    elif seller=="AGENT":
        se=1
    elif seller=="BUILDER":
        se=2
    #for layout
    if layout=="RK":
        lay=0
    elif layout=="BHK":
        lay=1
    if property_type=="Studio Apartment":
        typ=0
    elif property_type=="Independent House":
        typ=1
    elif property_type==" Independent Floor":
        typ=2
    elif property_type=="Villa":
        typ=3
    elif property_type=="Apartment":
        typ=4
    #for locality
    if locality=="Perungalathur":
        loc=0
    elif locality=="Chromepet":
        loc=1
    elif locality=="tambaram west":
        loc=2
    elif locality=="Ambattur":
        loc=3
    elif locality=="Pallikaranai":
        loc=4
    elif locality=="Kolathur":
        loc=5
    elif locality=="Medavakkam":
        loc=6
    elif locality=="Madipakkam":
        loc=7
    elif locality=="Perumbakkam":
        loc=9
    elif locality=="Choolaimedu":
        loc=10
    elif locality=="Perungudi":
        loc=11
    elif locality=="Adambakam":
        loc=12
    elif locality=="Velachery":
        loc=13
    elif locality=="Porur":
        loc=14
    elif locality=="Kotivakkam":
        loc=15
    elif locality=="Sholinganallur":
        loc=16
    elif locality=="Kodambakkam":
        loc=17
    elif locality=="West Mambalam":
        loc=18
    elif locality=="Thoraipakkam OMR":
        loc=19
    elif locality=="Neelankarai":
        loc=20
    elif locality=="Vadapalani":
        loc=21
    elif locality=="Nungambakkam":
        loc=22
    elif locality=="Thiruvanmiyur":
        loc=23
    elif locality=="T Nagar":
        loc=24
    elif locality=="Adyar":
        loc=25
    #for furnishing
    if furnishing=="Unfurnished":
        fu=0
    elif furnishing=="Semi-Furnished":
        fu=1
    elif furnishing=="Furnished":
        fu=2
    prediction=np.exp(model.predict([[se,bedroom,lay,typ,loc,area,fu,bathroom]]))
    return prediction

   #Main function for the web app using streamlit
def main():
    
    seller_options=["OWNER","AGENT","BUILDER"]
    bedroom_options=[1,2,3,4]
    layout_options=["RK","BHK"]
    property_type=["Studio Apartment","Independent House"," Independent Floor","Villa","Apartment"]
    locality_options=['Perungalathur','Chromepet','tambaram west','Ambattur','Pallikaranai','Kolathur','Medavakkam','Madipakkam','Perumbakkam','Choolaimedu','Perungudi','Adambakam','Velachery','Porur','Kotivakkam','Sholinganallur','Kodambakkam','West Mambalam','Thoraipakkam OMR','Neelankarai','Vadapalani','Nungambakkam','Thiruvanmiyur','T Nagar','Adyar']
    furnishing_options=["Unfurnished","Semi-Furnished","Furnished"]
    bathroom_options=[1,2,3]
     
    with st.sidebar:
        selected = option_menu("INTELLIGENT HOUSING RECOMMENDATION",["Fair rent estimate","Check for other nearby areas"],icons=["cash-coin","map"],menu_icon="house-door",default_index=0)
        selected
    if selected=="Fair rent estimate":  # Fair rent estimate using machine learning model
        st.title("Fair rent estimate") 
        col1,col2=st.columns(2)
        with col1:
            seller=st.selectbox("Select Seller",seller_options)
        with col2:
            bedroom=st.selectbox("Select Bedroom",bedroom_options)          
        with col1:
            layout=st.selectbox("Select Layout",layout_options)
        with col2:
            property_type=st.selectbox("Select Property Type",property_type)
        with col1:
            locality=st.selectbox("Select Locality",locality_options)
        with col2:
            area=st.number_input("Enter Area")
        with col1:
            furnishing=st.selectbox("Select Furnishing",furnishing_options)
        with col2:
            bathroom=st.selectbox("Select Bathroom",bathroom_options)
        
        if st.button("Predict"):
            start_time=time.time()
            pred=predict_price(seller,bedroom,layout,property_type,locality,area,furnishing,bathroom)
            price=round(pred[0])
            st.success("The estimated fair rent is ₹ {}".format(price))
            end_time=time.time()
            st.info("Time Taken: {} seconds".format(end_time-start_time))
    if selected=="Check for other nearby areas":   # Check for other nearby areas based on user input
        st.title("Check for other nearby areas")
        col1,col2=st.columns(2)
        with col1:
            sel=st.selectbox("Select Seller",seller_options)
        with col2:
            bedr=st.selectbox("Select bedroom",bedroom_options)
        with col1:
            lay=st.selectbox("Select layout",layout_options)
        with col2:
            prop=st.selectbox("Select property type",property_type)
        with col1:
            loca=st.selectbox("Select locality",locality_options)
        with col2:
            ar=st.number_input("Enter area")
        with col1:
            fur=st.selectbox("Select furnishing",furnishing_options)
        with col2:
            bath=st.selectbox("Select bathroom",bathroom_options)
        with col1:
            dist=st.number_input("Enter suitable distance from your required location")
        with col2:
            pric=st.number_input("Enter suitable price")
        if st.button("Show Suggestions"):
            df2=data.loc[(data["From"] == loca) & (data["Distance"] <= dist) ]
            l_list=list(df2["TO"])
            ds=pd.DataFrame()
            for i in l_list:
                ds1=sugg[(sugg["Locality"]==i) & (sugg["Rent"]<=pric)& (sugg["Bedroom"]<=bedr) & (sugg["layout"]==lay) & (sugg["property type"]==prop) & (sugg["Furnishing"]==fur) & (sugg["Bathrooms"]<=bath) & (sugg["area"]<=ar) & (sugg["seller-type"]==sel)]
                ds=pd.concat([ds,ds1],ignore_index=True)                
            if ds.empty:
                st.error("No suggestions found")
            else:
                st.dataframe(ds)

        
if __name__=='__main__':
    main()

