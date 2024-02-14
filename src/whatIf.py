import streamlit as st
import pandas as pd
import plotly.graph_objects as go

class WhatIf:
    def main(self):
        def update_df(df_A,df_B):
            merged_df = pd.merge(df_A, df_B, on=['Sex', 'Race/Ethnicity', 'Total Count' ], how='left')

            # Update the values of column C3 in DataFrame A based on the contents of DataFrame B
            merged_df.loc[~merged_df['New Selected'].isnull(), 'Total Selected'] = merged_df['New Selected']

            # Drop the 'New Selected' column (if you don't need it anymore)
            merged_df.drop(columns=['New Selected'], inplace=True)
            merged_df["Selection Rate"] = (merged_df['Total Selected']/merged_df['Total Count']).round(2)
            merged_df['Impact_Ratio'] = (merged_df['Selection Rate']/max(merged_df['Selection Rate'])).round(3)

            return merged_df

    # Session variable
        if 'df_intersectional_counts' not in st.session_state:
            df = pd.read_csv("./data/data.csv", header=0)
            df['IsSelected'] = df['IsSelected'].map({'Yes': True, 'No': False})
            total_counts = df.groupby(['Sex', 'Race/Ethnicity']).size().reset_index(name='Total Count')
            selected_df = df[df['IsSelected']]
            Total_Selected = selected_df.groupby(['Sex', 'Race/Ethnicity']).size().reset_index(name='Total Selected')
            intersectional_counts = pd.merge(total_counts, Total_Selected, on=['Sex', 'Race/Ethnicity'], how='left')
            intersectional_counts["Selection Rate"] = (intersectional_counts['Total Selected']/intersectional_counts['Total Count']).round(2)
            intersectional_counts['Impact_Ratio'] = (intersectional_counts['Selection Rate']/max(intersectional_counts['Selection Rate'])).round(3)
            st.session_state.df_intersectional_counts = intersectional_counts.copy()
        
        if 'display_df' not in st.session_state:
            st.session_state.display_df = st.session_state.df_intersectional_counts.copy()

        if 'sex_option' not in st.session_state:
            st.session_state.sex_option = ''
        if 'race_option' not in st.session_state:
            st.session_state.race_option = ''
        if 'input_selected' not in st.session_state:
            st.session_state.input_selected = ''
        if 'display_total' not in st.session_state:
            st.session_state.display_total = ''
        
        if 'new_df' not in st.session_state:
            st.session_state.new_df = pd.DataFrame()

    #Headers
        st.header("What-If Calculations ", divider= "blue")
        st.subheader("""Update values to see how it affects the calculations""", divider="orange")
        st.write("  ")

    #Input    
        margin_left, sex_content, pad1, race_content, pad2, selected_content,pad3, total_content, margin_right = st.columns([0.05,0.18,0.025,0.6,0.025,0.12,0.05,0.12,0.05])
        st.session_state.sex_option = sex_content.selectbox(
            "Sex",
            (st.session_state.df_intersectional_counts['Sex'].unique()),
            index=0,
            # placeholder="Select sex",
            )

        st.session_state.race_option = race_content.selectbox(
            "Race/Ethnicity",
            (st.session_state.df_intersectional_counts['Race/Ethnicity'].unique()),
            index=0,
            # placeholder="Select Race/Ethnicity",
            )
        
        pad3.title('/')
        
        if st.session_state.sex_option and st.session_state.race_option:
            selected_value = st.session_state.df_intersectional_counts.loc[(st.session_state.df_intersectional_counts['Sex'] == st.session_state.sex_option) & (st.session_state.df_intersectional_counts['Race/Ethnicity'] == st.session_state.race_option), 'Total Selected'].values
            selected_value = selected_value[0]
            st.session_state.input_selected = selected_content.text_input('No of Selected', selected_value)

            total_selected_count = st.session_state.df_intersectional_counts.loc[(st.session_state.df_intersectional_counts['Sex'] == st.session_state.sex_option) & (st.session_state.df_intersectional_counts['Race/Ethnicity'] == st.session_state.race_option), 'Total Count'].values
            st.session_state.display_total = total_selected_count[0]
            total_content.text_input('Total Count', st.session_state.display_total, disabled = True )
        else :
            selected_content.text_input('No of Selected', None)
            total_content.text_input('Total Count', None, disabled = True)

    #Output
        l,m,r = st.columns([.45,.1,.45])
        if m.button('Add'):
            new_data = {'Sex': st.session_state.sex_option,
            'Race/Ethnicity': st.session_state.race_option, 
            'New Selected':int(st.session_state.input_selected),
            'Total Count': st.session_state.display_total, 
            }

            st.session_state.new_df = pd.concat([st.session_state.new_df, pd.DataFrame([new_data])], ignore_index=True)

    # Dataframe update
        if len(st.session_state.new_df)!=0:
            l1,m1,r1 = st.columns([0.1,0.8,0.1])
            m1.dataframe(st.session_state.new_df, width= 800, hide_index= True)

            lft ,upd ,mid ,rst ,rgt = m1.columns([0.29,0.15,0.1,0.15,0.31])
            if upd.button('Update'):
                 st.session_state.display_df = update_df(st.session_state.display_df,st.session_state.new_df)
                
        #reset button
            if rst.button('Cancel', type= 'primary'):
                st.session_state.new_df = pd.DataFrame()
                st.session_state.display_df = st.session_state.df_intersectional_counts
                st.rerun()

    #dataframe view 
        st.markdown(f"<h4 style='text-align: center; text-shadow: 1px 1px 1px blue; '>Audit metrics by category: Race/Ethnicity</h4>", unsafe_allow_html=True)
        l,m,r = st.columns([0.1,0.9,0.1])
        vmin = min(st.session_state.display_df["Impact_Ratio"])
        vmax = max(st.session_state.display_df["Impact_Ratio"])
        m.dataframe(data = st.session_state.display_df.style.text_gradient(subset=["Impact_Ratio"], cmap="RdYlGn", vmin=vmin, vmax=vmax),hide_index=True, height = 527)

    #bar-chart
        st.markdown(f"<h4 style='text-align: center; text-shadow: 1px 1px 1px blue; '>Impact Ratio vs Race/Ethnicity</h4>", unsafe_allow_html=True)
        RaceEthnicity = st.session_state.display_df['Race/Ethnicity'].unique()
        for i, race in enumerate(RaceEthnicity):
            index = race.find('(')
            if i != -1:
                RaceEthnicity[i] = race[:index]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=RaceEthnicity,
            y=st.session_state.display_df.loc[st.session_state.display_df['Sex'] == 'Male', 'Impact_Ratio'].tolist(),
            name='Male',
            marker_color='indianred'
        ))
        fig.add_trace(go.Bar(
            x=RaceEthnicity,
            y=st.session_state.display_df.loc[st.session_state.display_df['Sex'] == 'Female', 'Impact_Ratio'].tolist(),
            name='Female',
            marker_color='lightsalmon'
        ))

        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(barmode='group', height=600)
        st.plotly_chart(fig, use_container_width=True)


        l1,m1,r1 = st.columns([0.4,0.2,0.4])
        if len(st.session_state.new_df)!=0:
            if m1.button('Reset', type= 'primary'):
                st.session_state.new_df = pd.DataFrame()
                st.session_state.display_df = st.session_state.df_intersectional_counts
                st.rerun()


            

