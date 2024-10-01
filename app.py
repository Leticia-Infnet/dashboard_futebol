import matplotlib as mpl
import matplotlib.patheffects as path_effects
import pandas as pd
import streamlit as st
import time
from statsbombpy import sb
from mplsoccer import VerticalPitch, Sbopen, FontManager, Pitch
from matplotlib import pyplot as plt
import plotly.graph_objects as go


@st.cache_data
def load_data() -> pd.DataFrame:
    '''
    Carrega os dados da api StatsBomb e filtra as partidas da Copa do Mundo FIFA

    Returns:
        matches (pd.DataFrame): DataFrame com as partidas da Copa do Mundo FIFA
    '''
    competitions = sb.competitions()

    world_cup = competitions[competitions['competition_name']
                             == 'FIFA World Cup']

    matches = pd.DataFrame()

    for season_id in world_cup['season_id']:
        season_matches = sb.matches(
            competition_id=world_cup['competition_id'].values[0],
            season_id=season_id
        )

        matches = pd.concat([matches, season_matches], ignore_index=True)

    return matches


def display_match_info(selected_match):
    '''
    Exibe as informações gerais da partida selecionada na tela do Streamlit 

    Args:
        selected_match (pd.DataFrame): DataFrame com as informações da partida selecionada
    '''
    col1, col2 = st.columns(2)

    col1.markdown("### Competição")
    col1.write(f"{selected_match['competition'].values[0]}")

    col1.markdown("### Data da Partida")
    col1.write(f"{selected_match['match_date'].values[0]}")

    col2.markdown("### Time da Casa")
    col2.write(f"{selected_match['home_team'].values[0]}")

    col2.markdown("### Time Visitante")
    col2.write(f"{selected_match['away_team'].values[0]}")

    col3, col4 = st.columns(2)

    col3.markdown("### Resultado")
    home_team = selected_match['home_team'].values[0]
    away_team = selected_match['away_team'].values[0]
    home_score = selected_match['home_score'].values[0]
    away_score = selected_match['away_score'].values[0]
    col3.write(f"{home_team} {home_score} x {away_score} {away_team}")

    col4.markdown("### Estádio")
    col4.write(selected_match['stadium'].values[0])


def display_formations(selected_match):
    '''
    Exibe as formações dos times da partida selecionada na tela do Streamlit

    Args:
        selected_match (pd.DataFrame): DataFrame com as informações da partida selecionada
    '''
    st.write('## Formações')
    parser = Sbopen(dataframe=True)

    roboto_bold = FontManager(
        'https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf')
    path_eff = [path_effects.Stroke(linewidth=3, foreground='white'),
                path_effects.Normal()]

    event, related, freeze, tactics = parser.event(
        selected_match['match_id'].values[0])

    home_team = selected_match['home_team'].values[0]
    away_team = selected_match['away_team'].values[0]

    def get_starting_xi(team_name):
        starting_xi_event = event.loc[((event['type_name'] == 'Starting XI') &
                                       (event['team_name'] == team_name)), ['id', 'tactics_formation']]
        starting_xi = tactics.merge(starting_xi_event, on='id')
        starting_xi['player_name'] = starting_xi['player_name'].apply(lambda name: ' '.join(
            [name.split()[0], name.split()[-1]]) if pd.notnull(name) else name)
        return starting_xi

    home_starting_xi = get_starting_xi(home_team)
    away_starting_xi = get_starting_xi(away_team)

    world_teams_colors = {
        'Argentina': ('#75AADB', '#FFFFFF'),
        'Brazil': ('#F7E03C', '#00A859'),
        'France': ('#002395', '#FFFFFF'),
        'Germany': ('#000000', '#FFFFFF'),
        'Italy': ('#0066CC', '#FFFFFF'),
        'Spain': ('#AA151B', '#FFCC00'),
        'England': ('#FFFFFF', '#CC0000'),
        'Netherlands': ('#FF4B00', '#FFFFFF'),
        'Portugal': ('#FF0000', '#00A859'),
        'Belgium': ('#FFD700', '#000000'),
        'Uruguay': ('#55A3D9', '#FFFFFF'),
        'Croatia': ('#FF0000', '#FFFFFF'),
        'Mexico': ('#006847', '#FFFFFF'),
        'Sweden': ('#FFCC00', '#0000FF'),
        'Denmark': ('#C60C30', '#FFFFFF'),
        'Colombia': ('#FCD116', '#0000FF'),
        'Switzerland': ('#D52B1E', '#FFFFFF'),
        'Russia': ('#D52B1E', '#FFFFFF'),
        'Japan': ('#BC002D', '#FFFFFF'),
        'South Korea': ('#C60C30', '#FFFFFF'),
        'Australia': ('#FFCC00', '#0000FF'),
        'Nigeria': ('#008751', '#FFFFFF'),
        'Senegal': ('#00853F', '#FFFFFF'),
        'Morocco': ('#C1272D', '#FFFFFF'),
        'Iran': ('#DA0000', '#FFFFFF'),
        'Saudi Arabia': ('#006C35', '#FFFFFF'),
        'Serbia': ('#C6363C', '#FFFFFF'),
        'Poland': ('#DC143C', '#FFFFFF'),
        'Peru': ('#D91023', '#FFFFFF'),
        'Iceland': ('#003897', '#FFFFFF'),
        'Costa Rica': ('#002B7F', '#FFFFFF'),
        'Panama': ('#FF0000', '#FFFFFF'),
        'Tunisia': ('#E70013', '#FFFFFF'),
        'Egypt': ('#CE1126', '#FFFFFF'),
        'USA': ('#3C3B6E', '#FFFFFF'),
        'Canada': ('#FF0000', '#FFFFFF'),
        'Qatar': ('#8A1538', '#FFFFFF'),
        'Ghana': ('#006B3F', '#FFFFFF'),
        'Cameroon': ('#007A5E', '#FFFFFF'),
        'Ecuador': ('#FFD100', '#0000FF'),
        'Wales': ('#D52834', '#FFFFFF'),
        'Scotland': ('#003366', '#FFFFFF'),
        'Paraguay': ('#FF0000', '#FFFFFF'),
        'Chile': ('#D52B1E', '#FFFFFF'),
        'Romania': ('#FFCC00', '#0000FF'),
        'Bulgaria': ('#00966E', '#FFFFFF'),
        'Norway': ('#BA0C2F', '#FFFFFF'),
        'Turkey': ('#E30A17', '#FFFFFF'),
        'Greece': ('#0D5EAF', '#FFFFFF'),
        'Czech Republic': ('#D7141A', '#FFFFFF'),
        'Slovakia': ('#0B4EA2', '#FFFFFF'),
        'Slovenia': ('#005DA4', '#FFFFFF'),
        'Ukraine': ('#FFD700', '#0000FF'),
        'Hungary': ('#C8102E', '#FFFFFF'),
        'Austria': ('#ED2939', '#FFFFFF'),
        'South Africa': ('#007749', '#FFFFFF'),
        'Ivory Coast': ('#F77F00', '#FFFFFF'),
        'Algeria': ('#006233', '#FFFFFF'),
        'Angola': ('#FF0000', '#FFFFFF'),
        'Togo': ('#006A4E', '#FFFFFF'),
        'Zaire': ('#FFD700', '#0000FF'),
        'Honduras': ('#0073CF', '#FFFFFF'),
        'El Salvador': ('#005BAC', '#FFFFFF'),
        'Jamaica': ('#FED100', '#000000'),
        'Trinidad and Tobago': ('#EF3340', '#FFFFFF'),
        'New Zealand': ('#000000', '#FFFFFF'),
        'North Korea': ('#C60C30', '#FFFFFF'),
        'China': ('#FFDE00', '#FF0000'),
        'Iraq': ('#007A3D', '#FFFFFF'),
        'Kuwait': ('#007A3D', '#FFFFFF'),
        'United Arab Emirates': ('#00732F', '#FFFFFF'),
        'Israel': ('#0038A8', '#FFFFFF'),
        'Cuba': ('#002A8F', '#FFFFFF'),
        'Haiti': ('#00209F', '#FFFFFF'),
        'Bolivia': ('#007A33', '#FFFFFF'),
        'Venezuela': ('#8B1A1A', '#FFFFFF')
    }

    def plot_formation(team_name, starting_xi, ax):
        formation = starting_xi['tactics_formation'].iloc[0]
        team_colors = world_teams_colors.get(team_name, ('#000000', '#FFFFFF'))

        pitch = VerticalPitch(pitch_color='#a8bc95',
                              line_color='white', goal_type='box')
        pitch.draw(ax=ax)
        ax_text = pitch.formation(formation, positions=starting_xi.position_id, kind='text',
                                  text=starting_xi.player_name.str.replace(
                                      ' ', '\n'),
                                  va='center', ha='center', fontsize=12, ax=ax)
        mpl.rcParams['hatch.linewidth'] = 3
        mpl.rcParams['hatch.color'] = team_colors[0]
        pitch.formation(formation, positions=starting_xi.position_id, kind='scatter',
                        c=team_colors[1], hatch='| |', linewidth=3, s=500,
                        xoffset=-8, ax=ax)
        ax.set_title(f'{team_name}', fontsize=40,
                     fontproperties=roboto_bold.prop, color='black', path_effects=path_eff)

    with st.spinner('Carregando formações...'):
        time.sleep(5)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8.72))
        plot_formation(home_team, home_starting_xi, ax1)
        plot_formation(away_team, away_starting_xi, ax2)

        st.pyplot(fig)


def display_events_dataframe(selected_match_id):
    '''
    Exibe um DataFrame com os eventos da partida selecionada na tela do Streamlit

    Args:
        selected_match_id (int): ID da partida selecionada 
    '''
    st.write('## Eventos da partida')
    events = sb.events(match_id=selected_match_id)

    event_types = events['type'].unique()
    selected_event_type = st.selectbox(
        'Selecione o tipo de evento', event_types, key='event_type_selectbox')

    filtered_events = events[events['type'] == selected_event_type]

    filtered_events = filtered_events.dropna(axis=1, how='all')

    st.write(filtered_events)


def display_pass_map(selected_match_id, home_team, away_team):
    '''
    Exibe um mapa de passes de um jogador selecionado na tela do Streamlit

    Args:
        selected_match_id (int): ID da partida selecionada
        home_team (str): Nome do time da casa
        away_team (str): Nome do time visitante
    '''
    st.write('## Mapa de Passe')
    st.write('Selecione um time e um jogador para visualizar o mapa de passes')

    selected_team = st.selectbox(
        'Selecione time', [home_team, away_team], key='pass_team_selectbox')
    events = sb.events(match_id=selected_match_id)
    team_events = events[events['team'] == selected_team]
    players = team_events['player'].unique()
    players = players[~pd.isna(players)]
    selected_player = st.selectbox(
        'Selecione jogador', players, key='pass_player_selectbox', index=0)

    with st.spinner('Carregando mapa de passes...'):
        time.sleep(5)

        player_events = team_events[team_events['player'] == selected_player]

        pitch = Pitch(pitch_color='grass',
                      line_color='white', line_zorder=2)
        fig, ax = pitch.draw()

        pass_events = player_events[player_events['type'] == 'Pass']

        for _, event in pass_events.iterrows():
            x = event['location'][0]
            y = event['location'][1]
            pass_end_location = event['pass_end_location']
            x_end = pass_end_location[0]
            y_end = pass_end_location[1]
            pass_outcome = event['pass_outcome']

            if pd.isna(pass_outcome):
                color = 'blue'
                alpha = 0.7
                label = 'Passes Concluídos'
            else:
                color = 'red'
                alpha = 0.5
                label = 'Passes Incompletos'

            pitch.arrows(x, y, x_end, y_end, color=color,
                         alpha=alpha, ax=ax, width=2, label=label)

        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(),
                  loc='upper left', fontsize='small')

        st.pyplot(fig)

        csv = player_events.to_csv(index=False)
        st.download_button(
            label="Download dos eventos do jogador",
            data=csv,
            file_name=f'{selected_player}_events.csv',
            mime='text/csv',
            key='pass_map_download_button'
        )


def display_shot_map(selected_match_id, home_team, away_team):
    '''
    Exibe um mapa de chutes de um jogador selecionado na tela do Streamlit

    Args:
        selected_match_id (int): ID da partida selecionada
        home_team (str): Nome do time da casa
        away_team (str): Nome do time visitante
    '''
    st.write('## Mapa de Chute')
    st.write('Selecione um time e um jogador para visualizar o mapa de chutes')

    selected_team = st.selectbox(
        'Selecione time', [home_team, away_team], key='shot_team_selectbox')

    events = sb.events(match_id=selected_match_id)
    team_events = events[events['team'] == selected_team]
    shot_events = team_events[team_events['type'] == 'Shot']
    players_with_shots = shot_events['player'].unique()
    players_with_shots = players_with_shots[~pd.isna(players_with_shots)]

    selected_player = st.selectbox(
        'Selecione jogador', players_with_shots, key='shot_player_selectbox', index=0)

    with st.spinner('Carregando mapa de chutes...'):
        time.sleep(5)

        player_events = team_events[team_events['player'] == selected_player]

        pitch = Pitch(pitch_color='grass',
                      line_color='white', line_zorder=2)
        fig, ax = pitch.draw()

        player_shot_events = player_events[player_events['type'] == 'Shot']

        for _, event in player_shot_events.iterrows():
            x = event['location'][0]
            y = event['location'][1]
            shot_outcome = event['shot_outcome']

            if shot_outcome == 'Goal':
                color = 'blue'
                marker = 'o'
                label = 'Gol'
            else:
                color = 'red'
                marker = 'x'
                label = 'Chute'

            pitch.scatter(x, y, color=color, marker=marker, ax=ax, label=label)

        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(),
                  loc='upper left', fontsize='small')

        st.pyplot(fig)

        csv = player_events.to_csv(index=False)
        st.download_button(
            label="Download dos eventos do jogador",
            data=csv,
            file_name=f'{selected_player}_events.csv',
            mime='text/csv',
            key='shot_map_download_button'
        )


def display_comparison_chart(selected_match):
    '''
    Exibe um gráfico de comparação entre dois jogadores selecionados na tela do Streamlit

    Args:
        selected_match (pd.DataFrame): DataFrame com as informações da partida selecionada
    '''
    st.write('## Comparação de Jogadores')
    st.write('Selecione dois jogadores para comparar')

    home_team = selected_match['home_team'].values[0]
    away_team = selected_match['away_team'].values[0]

    events = sb.events(match_id=selected_match['match_id'].values[0])
    home_team_events = events[events['team'] == home_team]
    away_team_events = events[events['team'] == away_team]

    home_team_players = home_team_events['player'].unique()
    home_team_players = home_team_players[~pd.isna(home_team_players)]
    away_team_players = away_team_events['player'].unique()
    away_team_players = away_team_players[~pd.isna(away_team_players)]

    selected_home_player = st.selectbox(
        'Selecione jogador do time da casa', home_team_players, key='home_player_selectbox', index=0)
    selected_away_player = st.selectbox(
        'Selecione jogador do time visitante', away_team_players, key='away_player_selectbox', index=0)

    home_player_events = home_team_events[home_team_events['player']
                                          == selected_home_player]
    away_player_events = away_team_events[away_team_events['player']
                                          == selected_away_player]

    home_player_completed_dribbles = home_player_events[(home_player_events['type'] == 'Dribble') & (
        home_player_events['dribble_outcome'] == 'Complete')]
    away_player_completed_dribbles = away_player_events[(away_player_events['type'] == 'Dribble') & (
        away_player_events['dribble_outcome'] == 'Complete')]

    home_player_completed_dribbles_count = home_player_completed_dribbles.shape[0]
    away_player_completed_dribbles_count = away_player_completed_dribbles.shape[0]

    home_player_non_penalty_goals = home_player_events[(home_player_events['type'] == 'Shot') & (
        home_player_events['shot_outcome'] == 'Goal') & (home_player_events['shot_type'] != 'Penalty')]
    away_player_non_penalty_goals = away_player_events[(away_player_events['type'] == 'Shot') & (
        away_player_events['shot_outcome'] == 'Goal') & (away_player_events['shot_type'] != 'Penalty')]

    home_player_non_penalty_goals_count = home_player_non_penalty_goals.shape[0]
    away_player_non_penalty_goals_count = away_player_non_penalty_goals.shape[0]

    home_player_ball_recoveries = home_player_events[home_player_events['type']
                                                     == 'Ball Recovery']
    away_player_ball_recoveries = away_player_events[away_player_events['type']
                                                     == 'Ball Recovery']

    home_player_ball_recoveries_count = home_player_ball_recoveries.shape[0]
    away_player_ball_recoveries_count = away_player_ball_recoveries.shape[0]

    home_player_tackles = home_player_events[(home_player_events['type'] == 'Duel') &
                                             (home_player_events['duel_type'] == 'Tackle') &
                                             (home_player_events['duel_outcome'] == 'Won')]

    away_player_tackles = away_player_events[(away_player_events['type'] == 'Duel') &
                                             (away_player_events['duel_type'] == 'Tackle') &
                                             (away_player_events['duel_outcome'] == 'Won')]

    home_player_tackles_count = home_player_tackles.shape[0]
    away_player_tackles_count = away_player_tackles.shape[0]

    home_player_blocks = home_player_events[(
        home_player_events['type'] == 'Block')]
    away_player_blocks = away_player_events[(
        away_player_events['type'] == 'Block')]

    home_player_blocks_count = home_player_blocks.shape[0]
    away_player_blocks_count = away_player_blocks.shape[0]

    categories = ['Dribles Completados', 'Gols (exceto pênaltis)', 'Recuperações de Bola',
                  'Desarmes', 'Bloqueios']

    with st.spinner('Carregando gráfico de comparação...'):
        time.sleep(5)
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=[home_player_completed_dribbles_count, home_player_non_penalty_goals_count,
                home_player_ball_recoveries_count, home_player_tackles_count, home_player_blocks_count],
            theta=categories,
            fill='toself',
            name=selected_home_player
        ))
        fig.add_trace(go.Scatterpolar(
            r=[away_player_completed_dribbles_count, away_player_non_penalty_goals_count,
                away_player_ball_recoveries_count, away_player_tackles_count, away_player_blocks_count],
            theta=categories,
            fill='toself',
            name=selected_away_player
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )),
            showlegend=True
        )

        st.plotly_chart(fig)


def main():
    matches = load_data()

    st.title('Partidas de Copa do Mundo :soccer:')
    st.write('Selecione uma temporada e uma partida para visualizar as informações')

    seasons = matches['season'].unique()
    selected_season = st.sidebar.selectbox(
        'Selecione temporada', seasons, key='season_selectbox')
    filtered_matches = matches[matches['season'] == selected_season]

    match_dict = {
        row['match_id']: f"{row['home_team']} x {row['away_team']}"
        for _, row in filtered_matches.iterrows()
    }

    selected_match_str = st.sidebar.selectbox(
        'Selecione partida', list(match_dict.values()), key='match_selectbox')
    reverse_match_dict = {v: k for k, v in match_dict.items()}
    selected_match_id = reverse_match_dict[selected_match_str]
    selected_match = filtered_matches[filtered_matches['match_id']
                                      == selected_match_id]

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Informações Gerais", "Mapa de Passe", "Mapa de Chute", "Comparação de Jogadores"])

    with tab1:
        display_match_info(selected_match)
        display_formations(selected_match)
        lineups = sb.lineups(match_id=selected_match_id)
        display_events_dataframe(selected_match_id)

    with tab2:
        home_team = selected_match['home_team'].values[0]
        away_team = selected_match['away_team'].values[0]
        display_pass_map(selected_match_id, home_team, away_team)

    with tab3:
        home_team = selected_match['home_team'].values[0]
        away_team = selected_match['away_team'].values[0]
        display_shot_map(selected_match_id, home_team, away_team)

    with tab4:
        display_comparison_chart(selected_match)


if __name__ == "__main__":
    main()
