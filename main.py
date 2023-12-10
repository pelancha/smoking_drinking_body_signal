import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_csv("data/smoking_driking_dataset_Ver01.csv")

st.title("Smoking and drinking influence")

# Rename columns
mapping_smk = {1: "never smoked", 2: "used to smoke", 3: "still smoke"}
df.SMK_stat_type_cd = df.SMK_stat_type_cd.astype(int)
df.SMK_stat_type_cd = df.SMK_stat_type_cd.apply(lambda x: mapping_smk.get(x, "never smoked"))
mapping_drk = {"Y": "drink", "N": "not drink"}
df["DRK_YN"] = df["DRK_YN"].apply(lambda x: mapping_drk.get(x, "do not drink"))

# Obtain sunburst

target_columns = ["sex", "SMK_stat_type_cd", "DRK_YN"]
tab2 = df.loc[:, target_columns]

fig1 = px.sunburst(tab2, path=['sex', 'SMK_stat_type_cd', "DRK_YN"], color='sex', width=600, height=600,
                   color_discrete_sequence=["#ED9ED6", "#7071E8"],
                   title="Proportion of smoking and drinking people among women and men")

# Obtain Average SGOT ALT

fig2 = px.box(df[:10000], x="age", y="SGOT_ALT",
              color_discrete_sequence=["#7071E8"],
              title="Average SGOT ALT in each age group (zoom for details)")

# Obtain Average SGOT ALT

tab2 = df[["age", "SGOT_AST"]].groupby(by=["age"], as_index=False, sort=True).mean()

fig3 = px.line(tab2, x='age', y='SGOT_AST', markers=True,
               color_discrete_sequence=["#7071E8"],
               title="Change of average SGOT AST between each age group")

# Obtain Distribution of men and women's SBP and DBP depending on their smoking state

fig4 = px.strip(df[:100000], x="SBP", y="SMK_stat_type_cd", orientation="h", color="sex",
                labels={"SMK_stat_type_cd": "smoking state"},
                color_discrete_sequence=["#7071E8", "#ED9ED6"],
                title="Distribution of men and women's systolic blood pressure depending on their smoking state")

fig5 = px.strip(df[:10000], x="DBP", y="SMK_stat_type_cd", orientation="h", color="sex",
                labels={"SMK_stat_type_cd": "smoking state"},
                color_discrete_sequence=["#7071E8", "#ED9ED6"],
                title="Distribution of men and women's diastolic blood pressure depending on their smoking state")

# Obtain chole

tab2 = df.loc[:, ["sex", "age", "tot_chole", "HDL_chole", "LDL_chole"]]
mapping_chole = {"Female": 0, "Male": 1}
mapping_smk = {"never smoked": 1, "used to smoke": 2, "still smoke": 3}
tab2.sex = tab2.sex.apply(lambda x: mapping_chole.get(x, 0))
df.SMK_stat_type_cd = df.SMK_stat_type_cd.apply(lambda x: mapping_smk.get(x, "1"))
tab3 = df.loc[:, ["SMK_stat_type_cd", "age", "tot_chole", "HDL_chole", "LDL_chole"]]

fig6 = px.parallel_coordinates(tab2[:200], color="sex", labels={"sex": "Sex",
                                                                "age": "Age", "tot_chole": "total cholesterol",
                                                                "HDL_chole": "HDL cholesterol",
                                                                "LDL_chole": "LDL cholesterol"},
                               color_continuous_scale=px.colors.diverging.Portland,
                               title="Correlation between sex, age and cholesterol")

fig7 = px.parallel_coordinates(tab3[:500], color="SMK_stat_type_cd", labels={"SMK_stat_type_cd": "Smoking state",
                                                                             "age": "Age",
                                                                             "tot_chole": "Total cholesterol",
                                                                             "HDL_chole": "HDL cholesterol",
                                                                             "LDL_chole": "LDL cholesterol"},
                               color_continuous_scale=px.colors.sequential.Viridis,
                               title="Correlation between smoking, age and cholesterol")

# Obtain 4x4 figure

tab2 = df.loc[:, ["SGOT_AST", "SGOT_ALT", "gamma_GTP", "SMK_stat_type_cd", "serum_creatinine"]]
mapping_pairplot = {"SGOT_AST": "SGOT AST", "SGOT_ALT": "SGOT ALT", "gamma_GTP": "gamma GTP",
                    "serum_creatinine": "serum creatinine", "SMK_stat_type_cd": "smoking state"}
tab2 = tab2.rename(columns=mapping_pairplot)

fig8 = px.scatter_matrix(tab2[:500], dimensions=["SGOT AST", "SGOT ALT", "gamma GTP", "serum creatinine"],
                         color="smoking state",
                         color_continuous_scale=px.colors.sequential.Plasma,
                         height=700, title="Correlation between indicators of liver and kidney function")

# table
target_columns = ["age", "sex", "SMK_stat_type_cd", "DRK_YN"]
tab2 = df[target_columns]
mapping_smk = {1: "never smoked", 2:"used to smoke", 3: "still smoke"}
tab2.SMK_stat_type_cd = tab2.SMK_stat_type_cd.apply(lambda x: mapping_smk.get(x, "1"))
mapping_tab2 = {"age": "average age"}
tab2 = tab2.rename(columns=mapping_tab2)
tab2 = tab2.groupby(by=["sex","SMK_stat_type_cd","DRK_YN"]).mean()

# Add buttons on the right

respondents = st.sidebar.button("Smokers and drinkers")
press = st.sidebar.button("Blood pressure")
chole = st.sidebar.button("Cholesterol")
organs = st.sidebar.button("Influence of smoking on organs")

if respondents:
    st.subheader("Proportion of smoking and drinking people")
    st.plotly_chart(fig1)
    st.table(tab2)

if press:
    st.subheader("Influence of smoking on pressure")
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)
    st.plotly_chart(fig5)

if chole:
    st.subheader("Influence of smoking on cholesterol")
    st.plotly_chart(fig6)
    st.plotly_chart(fig7)

if organs:
    st.subheader("Correlations between four parametres")
    st.plotly_chart(fig8)
