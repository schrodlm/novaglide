# CLIENT

## before_login_packet (just to keep the communication running)
{"time":"datetime.datetime.now()",
"sender":"unknown", 
"flag":"change_of_status",
"data":"offline"}

## log_in_packet
{"time":"datetime.datetime.now()",
"sender":"unknown", 
"flag":"log_in_data",
"data":[name, password]}

## request game history packet
{"time":"datetime.datetime.now()",
"sender":"self.client_id", 
"flag":"game_history",
"data":"no_data"}

## request challengers packet
{"time":"datetime.datetime.now()",
"sender":"self.client_id", 
"flag":"challengers",
"data":"no_data"}

# SERVER
## Blueprint
{"time":"datetime.datetime.now()",
"sender":"server", 
"flag":"type of packet ",
"data":"data corresponding to the packet"}

## change_of_status packet 
(for instance indicates that the client 
was accepted to the game)
{"time":"datetime.datetime.now()",
"sender":"server", 
"flag":"change_of_status",
"data":[new_status, aditional info(for instance his id or game)]}

## g1v1 packet
{"time":"datetime.datetime.now()",
"sender":"server", "player_id":1 or 2
"flag":"1v1_game",
"data":[game_time,goals_1,goals_2, p_1_name,p_2_name
,p1_pos_x, p_1_pos_y,p1_mouse_pos_x, 
p_1_mouse_pos_y, p_1_dash_cooldown,p_1_hook_cooldown,
p_2_pos_x, p2_pos_y,p_2_mouse_pos_x, 
p_2_mouse_pos_y, p_2_dash_cooldown,p_2_hook_cooldown]}
