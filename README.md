# Purpose of the service
list the top n teams with some team attributes and players with attributes

# All files in the zip
.env(hidden)
compose_output.py
dota2_team_data.py
fetch_data.py
README.md
team_player.py

# import libraries 
import logging
import os
import time
import datetime
import yaml
from dotenv import load_dotenv
import argparse

# execution command 
python3 dota2_team_data.py {the number of top teams} {the name of output file with .yaml extention} {logger severity}


# When user input top n number but there are only m valid/non-null teams, where n > m
The program will directly show top m teams in the output file

# output file format
Team id: fetch data from /teams/{team_id}
Team name: fetch data from /teams/{team_id}
    NOTE: There are multiple team_names from fetching /proPlayers 
    It is ambiguous that which team _name should be displayed so I used the name from /teams/{team_id}. The result is only one record. We can also concatenate team_name from the Players record 
Wins: fetch data from /teams/{team_id}
Losses: fetch data from /teams/{team_id}
Rating: fetch data from /teams/{team_id}
Team experience: sum(player_experience) 
For each player:
    Player: get player's name from teamDAO
    Player Experience: calculated from currentTime - full_history_time. 
    Country Code: get player's name from teamDAO

*NOTE*
1. the teams are sorted by team_experience in decreasing order
2. if the result from fetching /team/{team_id} is null or response error, the whole team will not be displayed in the output list
3. YAML was set default lexicographical sorting by the field name, but here we use specific display according to the requirement
4. The players with null full_history_time may be displayed in the list. 
5. The field "Player Experience" might be null because the data source, full_history_time, is null.
6. The player experience is calculated in UTC time format


# Serivce flow
fetch /proPlayers > 
save Player's data to PlayerDAO(Data Access Object) > 
calculate player's experience > 
aggregate player's data to TeamDAO > 
calculate team experience > 
get team attributes by fetching /teams/{team_id} with the number of top teams > 
compose output data > 
dump data to YAML file

# Future enhancement
1. Unit test: We can use pytest to do unit test and ensure the functions are robust and prevent corner cases.
2. centralize the strings or configurations to prevent typo and make it easier for code change in the future


# The reason of using DAO 
1. DAO provides a clear separation between the application's business logic and the underlying data storage mechanism (e.g., a database). This separation allows changes in the data storage technology or database schema without affecting the rest of the application's code. 
2. By abstracting data access, DAO promotes code reusability. Different parts of the application can use the same DAO methods to access and manipulate data, reducing code duplication and improving consistency.
