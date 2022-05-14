import altair as alt
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
plt.style.use('ggplot')
with st.echo(code_location='below'):
    def get_birds():
        return pd.read_csv("https://raw.githubusercontent.com/smthsmthsmthing/birds/main/bird.csv")

    birds = get_birds()

    """
    Here is a dataset that provides information about birds from Natural History Museum of Los Angeles County
    """
    birds.type=birds.type.replace({'SW':'Swimming Birds', 'W':'Wading Birds', 'T':'Terrestrial Birds', 'R': 'Raptors', 'P':'Scansorial Birds', 'SO':'Singing Birds'})
    birds['Length of the leg (mm)']=birds['feml']+birds['tibl']+birds['tarl']
    birds['Length of the arm (mm)']=birds['huml']+birds['ulnal']
    birds.rename(columns={'huml':'Length of Humerus (from shoulder to elbow) (mm)', 'humw':'Diameter of Humerus (from shoulder to elbow) (mm)', 'ulnal':'Length of forearm (Ulna) (mm)', 'ulnaw':'Diameter of forearm (Ulna) (mm)', 'feml':'Length of femur (the upper part of a leg) (mm)', 'femw':'Diameter of femur (the upper part of a leg) (mm)', 'tibl':'Length of tibiotarsus (the middle part of a leg) (mm)', 'tibw':'Diameter of tibiotarsus (the middle part of a leg) (mm)', 'tarl':'Length of tarsometatarsus (the lower part of a leg) (mm)', 'tarw':'Diameter of tarsometatarsus (the lower part of a leg) (mm)'}, inplace =True)

    st.dataframe(birds)

    """
    ## How many and what kinds of birds do we analize anyway?
    """
    types = birds.groupby(birds['type']).size()
    types = types.reset_index()
    types.columns = ['type', 'number']
    types['percentage'] = [str('%.1f' % ((i / sum(types['number'])) * 100)) + '%' for i in types['number']]
    st.dataframe(types.iloc[:, [0, 1]])
    selector = st.selector('choose library for plotting', ('Altair', 'Matplotlib'))
    if selector == 'Altair':
        chart = alt.Chart(types).encode(
            theta=alt.Theta(field="number", type="quantitative", stack=True),
            color=alt.Color(field="type", type="nominal", legend=None), tooltip=['number']
        ).properties(width=600, height=600, title={'text': 'Basic information about the dataset',
                                                   'subtitle': 'total number of birds is ' + str(types.number.sum())})
        pie = chart.mark_arc(outerRadius=180)
        text = pie.mark_text(radius=250, size=15, fill='black').encode(text="type:N")
        percentage = pie.mark_text(radius=100, size=15, fill='black').encode(text='percentage')
        st.altair_chart(pie + text + percentage)
    else:
        fig, ax = plt.subplots()
        ax.text(-0.3, 1.05, 'total count of birds: ' + str(sum(types['number'])), color='black', size=6)
        ax.set_title('Basic information about the dataset')
        ax.pie(types['number'], labels=types['type'], autopct='%1.1f%%')
        ax.axis('equal')
        st.pyplot(fig)

    """
    This chart is here because I spent too much time on it. There is a nicer more interactive chart under it, though
    """

    """
    Hover your cursor for better experience
    """


    """
    ## The type that a bird belongs to actually affects its sceleton structure. Here you can see it for yourself
    """

    grouped = []
    Y= st.selectbox("Choose what feature you want to see", birds.columns)
    for type in birds['type'].unique():
        grouped.append(list(birds.loc[birds['type']==type][Y].dropna()))
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_axes([0, 0, 1, 1])
    bp = ax.boxplot(grouped)
    ax.set_xticklabels(birds['type'].unique())
    plt.ylabel(Y)
    ax.set_title(Y+' of different types of birds')
    st.pyplot(fig)
    """
    Not only that, but different types of birds have different ratios and different dependencies of ratios
    
    For example, consider a fact: the longer the leg the longer the arm. This is true for some types and is wrong for other
    
    See for yourself
    """
    type_of_bird= st.multiselect("Type", birds["type"].value_counts().index)
    Y_axis= st.selectbox("Choose what you want to compare", birds.columns)
    X_axis= st.selectbox("Сhoose what you want to compare to", birds.columns)

    birds_selection = birds[birds['type'].isin(type_of_bird)]

    chart = (
        alt.Chart(birds_selection).mark_circle().encode(x=X_axis, y=Y_axis, tooltip=[Y_axis, X_axis], color='type')
    )

    st.altair_chart(
        (
                chart + chart.transform_loess(X_axis, Y_axis, groupby=['type']).mark_line()
        ).interactive(), True
    )

