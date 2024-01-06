## Blueprint
{"time":datetime.datetime.now(),
"sender":"server/client_id/unknown", 
"flag":"type of packet",
"data":[data corresponding to the packet]}

# CLIENT

## share status packet
{"time":datetime.datetime.now(),
"sender":"unknown"/self.id, 
"flag":self.status,
"data":["no_data"]}

## log_in_packet
{"time":datetime.datetime.now(),
"sender":"unknown", 
"flag":"log_in_data",
"data":[name, password]}

## request game history packet
{"time":datetime.datetime.now(),
"sender":self.client_id, 
"flag":"game_history",
"data":[self.game.user_credentials["name"]]}

## request challengers packet
{"time":datetime.datetime.now(),
"sender":self.client_id, 
"flag":"get_challengers",
"data":["no_data"]}

## request elo packet
{"time":datetime.datetime.now(),
"sender":self.client_id, 
"flag":"get_elo",
"data":[self.game.user_credentials["name"]]}

## request game history packet
{"time":datetime.datetime.now(),
"sender":self.client_id, 
"flag":"game_history",
"data":[self.game.user_credentials["name"]]}

## get in soloque
{"time":datetime.datetime.now(),
"sender":self.client_id, 
"flag":"queued_solo",
"data":["no_data"]}

## waiting for opponent
{"time":datetime.datetime.now(),
"sender":self.client_id, 
"flag":"waiting_for_opponent",
"data":["no_data"]}

# SERVER

## change_of_status packet 
{"time":datetime.datetime.now(),
"sender":"server", 
"flag":"change_of_status",
"data":[new_status, aditional info(for instance his id)]}

## g1v1 packet
{"time":datetime.datetime.now(),
"sender":"server", "player_id":1 or 2
"flag":"game_state_1",
"data":["your_side",self.remaining_time, self.score[0], self.score[1],
                self.p1.name, self.p2.name,
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, self.p1.hook_coords.x, 
            self.p1.hook_coords.y,
            self.p2.hook_coords.x, self.p2.hook_coords.y, self.dash_time_1,
            self.hook_time_1, self.dash_time_2 ,self.hook_time_2,
            self.ball.x, self.ball.y, self.p1.hooking,self.p2.hooking, self.tiebreak]}

## waiting for opponent
{"time":datetime.datetime.now(),
"sender":"server", 
"flag":"Waiting_for_opponent",
"data":["no_data"]}

## challengers
{"time":datetime.datetime.now(),
"sender":"server", 
"flag":"challengers",
"data":[self.db_query.query_data("get_challengers")]}

## winrate 
{"time":datetime.datetime.now(),
"sender":"server", 
"flag":"winrate",
"data":[self.db_query.get_user_winrate(message["data"][0])[0]]}
