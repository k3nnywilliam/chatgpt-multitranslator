from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from chatgpt_utils.translate_utils import Translator
import logging

data = {
    'LANGUAGE': ['German', 'French', 'Danish', 'Indonesian'],
    'TRANSLATION': ['Hallo', 'Bonjour', 'Hej', 'Halo']
}

df = pd.DataFrame(data)

app = Dash(__name__)

app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='/assets/styles.css'  # Path to your CSS file relative to your app's root
    ),
    
    html.H1("Multi Translator", className='custom-h1'),
    
    dcc.Dropdown(
        id='language-dropdown',
        options=[
            {'label': 'German', 'value': 'German'},
            {'label': 'Russian', 'value': 'Russian'},
            {'label': 'Spanish', 'value': 'Spanish'},
            {'label': 'Indonesian', 'value': 'Indonesian'},
        ],
        value='German',  # Default selected language
        style={'width': '50%'} 
        #multi=True,  # Allow multiple selections
    ),
    
    html.Br(),
    
    # Text input for filtering based on entered text
    dcc.Input(id='text-input', type='text', placeholder='Enter text...', style={'width': '80%'}),
    html.Br(),
    
    # Button to trigger the display of the DataFrame
    html.Button('TRANSLATE', id='display-button'),
    html.Br(),
    
    dash_table.DataTable(
        id='datatable',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=[],
        style_table={'height': '300px', 'overflowY': 'auto'}
    ),
])


def chat_translate(selected_language, text_input):
    print(f"Selected Language: {selected_language}")
    translator = Translator()
    answers_ls =[]
    logging.info(f"Translating to: {selected_language}")
    logging.info("Awaiting responses...")
    answers_ls = translator.split_chat_processing([text_input], [selected_language])
    parsed_responses = translator.parse_responses(answers_ls)
    logging.info(f"reply: {parsed_responses}")
    split_list = parsed_responses[0].split("\n")
    df2 = pd.DataFrame()
    if len(split_list)==1:
        df2 = pd.DataFrame({
        'LANGUAGE': [selected_language],
        'TRANSLATION': split_list}) 
    else:
        df2 = pd.DataFrame({
        'LANGUAGE': [selected_language],
        'TRANSLATION': split_list}) 
    #answer_dt = translator.format_answers_to_dataframe(parsed_responses)
    print(df2.head())
    df = df2
    return df

@callback(
    Output('datatable', 'data'),
    Input('display-button', 'n_clicks'),
    #Input('language-dropdown', 'value'),
    State('language-dropdown', 'value'),
    State('text-input', 'value')
)
def update_datatable(n_clicks, selected_language, text_input):
    if n_clicks:
        response_dt = chat_translate(selected_language, text_input)
        return response_dt.to_dict('records')
    else:
        return []

if __name__ == '__main__':
    app.run(debug=True)