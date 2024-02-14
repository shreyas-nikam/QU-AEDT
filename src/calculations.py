import base64
import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import StringIO


class Calculations:
    def __init__(self):
        self.df = pd.read_csv("./data/data.csv", header=0)

    def main(self):
        if 'df_intersectional_counts' not in st.session_state:
            st.session_state.df_intersectional_counts = pd.DataFrame({'A' : []})

        df_copy = self.df.copy()
        
        st.header("Calculations ", divider= "blue")
        st.subheader("Use the sample data or upload your data", divider = "orange")
        l1,m1,r1 = st.columns([0.02,0.96,0.02])
        m1.dataframe(self.df, hide_index =True)

        st.divider()

        bin_file = 'data/dataSchema.csv'
        with open(bin_file, 'rb') as f:
                data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">sample file.</a>'

        st.markdown(f"""<h6 style='text-align: center;'> Use the above sample dataset or upload your own data using the format in this {href}</h6>""", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            # Can be used wherever a "file-like" object is accepted:
            dataframe = pd.read_csv(uploaded_file, header=0)
            if dataframe.columns != df_copy.columns:
                st.error("Please submit valid data schema. Use the above data schema file link as reference")
            else: 
                st.dataframe(dataframe)
                df_copy = dataframe.copy()
        st.divider()

        df_copy['IsSelected'] = df_copy['IsSelected'].map({'Yes': True, 'No': False})
        Sex_Categories = df_copy.groupby('Sex').agg(Total=('Sex', 'size'), Selected=('IsSelected', 'sum')).reset_index()
        Sex_Categories["Selection_Rate"] = (Sex_Categories['Selected']/Sex_Categories['Total']).round(2)
        Sex_Categories['Impact_Ratio'] = (Sex_Categories['Selection_Rate']/max(Sex_Categories['Selection_Rate'])).round(3)

        Race_Categories = df_copy.groupby('Race/Ethnicity').agg(Total=('Race/Ethnicity', 'size'), Selected=('IsSelected', 'sum')).reset_index()
        Race_Categories["Selection_Rate"] = (Race_Categories['Selected']/Race_Categories['Total']).round(2)
        Race_Categories['Impact_Ratio'] = (Race_Categories['Selection_Rate']/max(Race_Categories['Selection_Rate'])).round(3)

        total_counts = df_copy.groupby(['Sex', 'Race/Ethnicity']).size().reset_index(name='Total Count')
        selected_df = df_copy[df_copy['IsSelected']]
        Total_Selected = selected_df.groupby(['Sex', 'Race/Ethnicity']).size().reset_index(name='Total Selected')
        intersectional_counts = pd.merge(total_counts, Total_Selected, on=['Sex', 'Race/Ethnicity'], how='left')
        intersectional_counts["Selection Rate"] = (intersectional_counts['Total Selected']/intersectional_counts['Total Count']).round(2)
        intersectional_counts['Impact_Ratio'] = (intersectional_counts['Selection Rate']/max(intersectional_counts['Selection Rate'])).round(3)

        st.session_state.df_intersectional_counts = intersectional_counts.copy()

    # Calculating SELECTION RATE and IMPACT RATIO
        st.subheader("Calculating SELECTION RATE and IMPACT RATIO", divider = "orange")
        l,m,r = st.columns([0.1,0.8,0.1])
        # m.markdown(f"<h5 style='text-align: center;'>Calculations for Sex category</h5>", unsafe_allow_html=True)
        with m:
            container = st.container(border=True)
            container.latex(r'''\text{SELECTION RATE} = \frac{Number\ of\ Selected}{Total\ Applicants}''')
            container.write(' \n')
            category = Sex_Categories.iloc[0,0]
            # container.write(f'For {category} applicants:')
            container.markdown(f"<h5 style='text-align: center;'><u>For {category} applicants:</u></h5>", unsafe_allow_html=True)
            total_applicants = Sex_Categories.iloc[0, 1]
            sex_selected = Sex_Categories.iloc[0, 2]
            selection_rate = Sex_Categories.iloc[0, 3]
            latex_code = r'\text{SELECTION RATE} = \frac{Number\ of\ Selected\ }{Total\ Applicants} = \frac{' + str(sex_selected) + '}{' + str(total_applicants) + '} = ' + str(selection_rate)
            container.latex(latex_code)            
        st.write(" ")

        with m:
            container = st.container(border=True)
            container.latex(r'''\text{IMPACT RATIO} = \frac{Selection\ Rate\ for\ a\ Category}{Selection\ Rate\ of\ the\ Most\ Selected\ Category}''')
            container.write(' \n')
            container.markdown(f"<h5 style='text-align: center;'><u>For {category} applicants:</u></h5>", unsafe_allow_html=True)
            impact_ratio = Sex_Categories.iloc[0, 4]
            max_selection_rate = max(Sex_Categories['Selection_Rate'])
            container.latex(r'\text{IMPACT RATIO} = \frac{Selection\ Rate\ for\ a\ Category}{Selection\ Rate\ of\ the\ Most\ Selected\ Category} = \frac{' + str(selection_rate) + '}{' + str(max_selection_rate) + '}= '+str(impact_ratio))

    # Categories : SEX
        st.subheader("Audit metrics by category: Sex ", divider = "orange")

        l,r,m = st.columns([.4,.2,.4])
        if r.toggle('Table View'):
            l1,m1,r1 = st.columns([0.1,0.8,0.1])
            m1.write(" ")
            vmin = min(Sex_Categories["Impact_Ratio"])
            vmax = max(Sex_Categories["Impact_Ratio"])
            st.write(" ")
            m1.dataframe(Sex_Categories.style.text_gradient(subset=["Impact_Ratio"], cmap="RdYlGn", vmin=vmin, vmax=vmax),width= 700,  hide_index=True)
        else:    
            margin_left, col_male , divider, col_female, margin_right = st.columns([0.02,0.48,0.02,0.48,0.02])
            with col_male:
                    container = st.container(border=True)     
                    container.markdown(f"<h4 style='text-align: center; text-shadow: 1px 1px 1px blue; '>{Sex_Categories.iloc[0,0]}</h4>", unsafe_allow_html=True)
                    col1,col2,col3,col4 = container.columns(4)
                    col1.metric(label="Total Applicants", value = Sex_Categories.iloc[0,1])
                    col2.metric(label="Total Selected", value=Sex_Categories.iloc[0,2])
                    col3.metric(label="Selection Rate", value=Sex_Categories.iloc[0,3], help = "The rate at which individuals in a category are either selected to move forward in the hiring process or assigned a classification by an AEDT")
                    col4.metric(label="Impact Ratio", value=Sex_Categories.iloc[0,4], delta=((Sex_Categories.iloc[0,4]-1).round(2)), help = "The selection rate for a category divided by the selection rate of the most selected category")

            with col_female:
                    container = st.container(border=True)     
                    container.markdown(f"<h4 style='text-align: center; text-shadow: 1px 1px 1px blue;'>{Sex_Categories.iloc[1,0]}</h4>", unsafe_allow_html=True)
                    col1,col2,col3,col4 = container.columns(4)
                    col1.metric(label="Total Applicants", value=Sex_Categories.iloc[1,1])
                    col2.metric(label="Total Selected", value=Sex_Categories.iloc[1,2])
                    col3.metric(label="Selection Rate", value=Sex_Categories.iloc[1,3], help = "The rate at which individuals in a category are either selected to move forward in the hiring process or assigned a classification by an AEDT")
                    col4.metric(label="Impact Ratio", value=Sex_Categories.iloc[1,4], delta=((Sex_Categories.iloc[1,4]-1).round(2)), help = "The selection rate for a category divided by the selection rate of the most selected category")

            

    # Race / Ethnicity Categories
        st.subheader("Audit metrics by category: Race/Ethnicity", divider = "orange")
        l1,m1,r1 = st.columns([0.1,0.8,0.1])
        vmin = min(Race_Categories["Impact_Ratio"])
        vmax = max(Race_Categories["Impact_Ratio"])
        m1.dataframe(Race_Categories.style.text_gradient(subset=["Impact_Ratio"], cmap="RdYlGn", vmin=vmin, vmax=vmax),hide_index=True)


    # Intersectional Categories
        st.subheader("Audit metrics by category: Sex + Race/Ethnicity", divider = "orange")
        
        l1,m1,r1 = st.columns([0.05,0.9,0.05])
        vmin = min(intersectional_counts["Impact_Ratio"])
        vmax = max(intersectional_counts["Impact_Ratio"])
        m1.dataframe(data = intersectional_counts.style.text_gradient(subset=["Impact_Ratio"], cmap="RdYlGn", vmin=vmin, vmax=vmax),hide_index=True, height = 527)

        # chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
        # # st.bar_chart(intersectional_counts, )

        RaceEthnicity = intersectional_counts['Race/Ethnicity'].unique()
        for i, race in enumerate(RaceEthnicity):
            index = race.find('(')
            if i != -1:
                RaceEthnicity[i] = race[:index]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=RaceEthnicity,
            y=intersectional_counts.loc[intersectional_counts['Sex'] == 'Male', 'Impact_Ratio'].tolist(),
            name='Male',
            marker_color='indianred'
        ))
        fig.add_trace(go.Bar(
            x=RaceEthnicity,
            y=intersectional_counts.loc[intersectional_counts['Sex'] == 'Female', 'Impact_Ratio'].tolist(),
            name='Female',
            marker_color='lightsalmon'
        ))

        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(barmode='group', height=600)
        st.markdown(f"<h4 style='text-align: center; text-shadow: 1px 1px 1px blue; '>Impact Ratio vs Race/Ethnicity</h4>", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)









