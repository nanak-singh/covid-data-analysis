import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


def main():
    st.title('Relationship of various parameters of Covid -19 and GDP dataset')

    @st.cache(persist=True, allow_output_mutation=True)
    def load_data():
        cov_dataset = pd.read_csv("Dataset/covdataset.csv", encoding='latin1')
        cov_dataset.drop(["Latitude","Longitude"],axis=1,inplace=True)
        cov_dataset.set_index("Countries", inplace = True)
        return cov_dataset

    df = load_data()

    st.subheader("Explore Dataset")
    if st.checkbox("Show Dataset"):
        number = st.number_input("Number of Rows to View", min_value=1, step=1)
        if st.button("All rows") :
            st.dataframe(df)
        else:
            st.dataframe(df.head(number))
    

    if st.button("Show Countries Names"):
	    st.write(df.index)


    
    #df.loc["United States"].plot()
    #df.loc["Brazil"].plot()
    #df.loc["India"].plot()
    #plt.legend()
    #st.set_option('deprecation.showPyplotGlobalUse', False)
    #st.pyplot()
    #st.pyplot(df.loc[["United States", "Brazil", "India"]])
    #st.write(df.loc["India"].plot())
    #st.pyplot(fig=df.loc["India"].plot(), clear_figure=True)
    
    st.subheader("Comapre Covid Cases in Different Countries")
    all_countries_names = list(df.index.values)
    selected_columns_names = []
    selected_columns_names = st.multiselect("Select Countries To Plot", all_countries_names, default='India', key="compare")
    for i in selected_columns_names:
        df.loc[i].plot()
    plt.legend()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

    #df.loc[selected_columns_names].plot()
    #st.pyplot()
    #cust_plot= df[[selected_columns_names]].plot()
    #st.markdown(selected_columns_names)
    #st.line_chart(cust_plot)

    st.subheader("Max Infection Rate")
    all_countries_name = list(df.index.values)
    selected_columns_names_for_max_infection = []
    selected_columns_names_for_max_infection = st.multiselect("Select Countries To Plot", all_countries_name, default='India', key="max-infection")
    for i in selected_columns_names_for_max_infection:
        max_infection_rate = df.loc[i].diff().max()
        st.write('Max Infection Rate in ' + str(i) + ' = ' + str(max_infection_rate))   

    
    countries = list(df.index)
    df_copy = df.copy()
    max_infection_rates = []
    for c in countries:
        max_infection_rates.append(df_copy.loc[c].diff().max())
    df_copy["max_infection_rate"] = max_infection_rates


    corona_data = pd.DataFrame(df_copy["max_infection_rate"])


    
    
    @st.cache(persist=True)
    def load_data2():
        GDP_dataset = pd.read_csv("Dataset/GDP.csv", encoding='latin1')
        GDP_dataset.drop(["General government net lending/borrowing (% of GDP)","Inflation rate, average consumer prices"],axis=1,inplace=True)
        GDP_dataset.set_index("Countries", inplace = True)
        data = corona_data.join(GDP_dataset, how="inner")
        return data

    df2 = load_data2()

    
    
    st.title("Max Infection Rate vs GDP (Scatter Plot)")
    x = df2["GDP"]
    y = df2["max_infection_rate"]
    sns.scatterplot(x,y)
    
    st.pyplot()

    st.title("LOG(Max Infection Rate) vs GDP (Scatter Plot)")
    sns.scatterplot(x,np.log(y))
    st.pyplot()

    st.title("LOG(Max Infection Rate) vs GDP (Reg Plot)")
    sns.regplot(x, np.log(y))
    st.pyplot()
    
    
    st.title("Max Infection Rate vs Unemployment Rate (Scatter Plot)")
    x = df2["Unemployment rate"]
    y = df2["max_infection_rate"]

    sns.scatterplot(x,y)
    st.pyplot()


    st.title("LOG(Max Infection Rate) vs Unemployment Rate")
    x = df2["Unemployment rate"]
    y = df2["max_infection_rate"]
    sns.scatterplot(x,np.log(y))
    st.pyplot()


    st.title("LOG(Max Infection Rate) vs Unemployment Rate (Reg Plot)")
    sns.regplot(x, np.log(y))
    st.pyplot()



    st.title("Unemployment Rate vs GDP (Scatter Plot)")
    x = df2["GDP"]
    y = df2["Unemployment rate"]
    sns.scatterplot(x,y)
    st.pyplot()


    st.title("Unemployment Rate vs GDP (Scatter Plot)")
    x = df2["GDP"]
    y = df2["Unemployment rate"]
    sns.scatterplot(x,np.log(y))
    st.pyplot()


    st.title("LOG(Unemployment Rate vs GDP (Reg Plot))")
    sns.regplot(x, np.log(y))
    st.pyplot()



    country = list(df.index)
    sum_of_cases = []
    for x in country:
        sum_of_cases.append(df_copy.loc[x].sum())
    df_copy["sum_of_cases"] = sum_of_cases

    total_cases = pd.DataFrame(df_copy["sum_of_cases"])


    st.markdown("Pie Chart - Total COVID cases Distribution")
    plt.pie(sum_of_cases, shadow=True,startangle=90)
    plt.legend(total_cases.index,title="name of countries",loc="center left",bbox_to_anchor=(1, 0, 0.5, 1))
    plt.show()
    st.pyplot()


    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


    st.sidebar.header("About App")
    st.sidebar.info("Industrial Training Project")
    st.sidebar.header("Get Datasets")
    st.sidebar.markdown("[COVID 19 DataSet](https://raw.githubusercontent.com/nanak-singh/covid-data-analysis/main/Dataset/covdataset.csv)")
    st.sidebar.markdown("[GDP DataSet](https://raw.githubusercontent.com/nanak-singh/covid-data-analysis/main/Dataset/GDP.csv)")
    st.sidebar.header("Made By")
    st.sidebar.info("""
        Prabhnoor Kaur\n
        CSE - 2\n
        07413202718
    """)
	
	

if __name__ == '__main__':
    main()
