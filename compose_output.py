import logging
import os
import time

import yaml
from dotenv import load_dotenv

import fetch_data

load_dotenv()

# use this function to log function names for debugging
def log_function_name(func):
    def wrapper(*args, **kwargs):
        function_name = func.__name__
        logging.debug(f"Entering function: {function_name}")
        return func(*args, **kwargs)
    return wrapper


# fetch the teams' data from dota openapi, 
# if the team's data == None, this team does not count in the top n teams
def compose_output_data(teams, num_teams):
    data_to_save = []
    team_cnt = 0
    start_time = time.time()
    logging.info(f"{os.environ.get('MSG_INFO_RETRIVE_TEAMS_DATA_START')} {start_time}")
    for team in teams:
        if team_cnt == num_teams:
             break
        id = team.team_id
        if id is not None: 
            team_data = fetch_data.get_team_data(id)
            if team_data is not None:
                overall_team_data = composeTeamData(team_data, team)
                for player in team.player_list:
                    player_data = composePlayersData(player)
                    overall_team_data[os.environ.get("OUTPUT_FIELD_FOR_EACH_PLAYER")].append(player_data)
                data_to_save.append(overall_team_data)
                team_cnt+=1
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"{os.environ.get('MSG_INFO_RETRIVE_TEAMS_DATA_END')} {elapsed_time:.2f} seconds")
    logging.info(f"Total teams: {team_cnt}")            
    return data_to_save
compose_output_data = log_function_name(compose_output_data)

# compose team data including pre-calculated team experience and the team_name fetched by /team/{team_id}
def composeTeamData(team_data, team):
    oeverall_team_data = {
        os.environ.get("OUTPUT_FIELD_TEAM_ID"): team.team_id,
        # "Team Name": list(team_name_set),
        os.environ.get("OUTPUT_FIELD_TEAM_NAME"): team_data[os.environ.get("TEAM_DATA_FIELD_NAME")],
        os.environ.get("OUTPUT_FIELD_WINS"): team_data[os.environ.get("TEAM_DATA_FIELD_WINS")],
        os.environ.get("OUTPUT_FIELD_LOSSES"): team_data[os.environ.get("TEAM_DATA_FIELD_LOSSES")],
        os.environ.get("OUTPUT_FIELD_Rating"): team_data[os.environ.get("TEAM_DATA_FIELD_RATING")], 
        os.environ.get("OUTPUT_FIELD_TEAM_EXP"): team.team_experience,
        os.environ.get("OUTPUT_FIELD_FOR_EACH_PLAYER"): []
    }
    return oeverall_team_data


# compose players name, pre-calculated experience and country code from the players_list in teamsDAO
def composePlayersData(player):
    player_data = {
        os.environ.get("OUTPUT_FIELD_PLAYER_NAME"): player.personaname,
        os.environ.get("OUTPUT_FIELD_PLAYER_EXP"): player.player_experience,
        os.environ.get("OUTPUT_FIELD_PLAYER_CTRY_CD"): player.country_code
    }
    return player_data

def save_data_to_yaml(data, output_file):
    with open(output_file, "w") as yaml_file:
        yaml.dump(data, yaml_file, sort_keys=False, allow_unicode=True)
save_data_to_yaml = log_function_name(save_data_to_yaml)

