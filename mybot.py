import os
import time
import re
from slackclient import SlackClient
import time
import json



slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None
users_avg={}
bot_counter=0
bot_average=0
# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
INTERVAL=60

	
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def calc_average(number,user):
	global users_avg
	global bot_counter
	global bot_average
	current_user=user
	new_average=0
	if not current_user in users_avg:
		users_avg.update({current_user:{'average':number,'counter':1}})
		new_average=number
	else:
		current_average=users_avg[current_user]['average']
		current_counter=users_avg[current_user]['counter']
		new_average=((current_average*current_counter)+number)/(current_counter+1)
		users_avg[current_user]['average']=new_average
		users_avg[current_user]['counter']=current_counter+1
	temp=((bot_average*bot_counter)+number)/(bot_counter+1)
	bot_average=temp
	bot_counter=bot_counter+1
	with open('bot_avg.json', 'w') as f:
		data = {'average' : bot_average}
		json.dump(data,f)
	with open('users_avg.json', 'w') as f:
		json.dump(users_avg,f)
	
	return new_average
	
def parse_bot_commands(slack_events):
	for event in slack_events:
		if event["type"] == "message" and not "subtype" in event:
			message = event["text"]
			user = event["user"]
			channel = event["channel"]
			return message,user,channel
	return None, None, None
	
def handle_command(message, user, channel):
	response = None
	if is_number(message): 
		number = float(message)
		new_average=calc_average(number,user)
		response=str(new_average)
		slack_client.api_call( "chat.postMessage",channel=channel,text=response )

if __name__ == "__main__":
	if slack_client.rtm_connect(with_team_state=False):
		print("Starter Bot connected and running!")
		old_time=time.time()
		prev_average=0
		while True:
			message, user, channel = parse_bot_commands(slack_client.rtm_read())
			if message:
				handle_command(message,user, channel)
			curr_time=time.time()
			if curr_time-old_time > INTERVAL and (not prev_average == bot_average):
				old_time=curr_time
				ch=slack_client.api_call("channels.list", exclude_archived=1)['channels'][0]['id']
				slack_client.api_call( "chat.postMessage",channel=ch,text=str(bot_average))
				prev_average=bot_average
				
			time.sleep(RTM_READ_DELAY)
	else:
		print("Connection failed. Exception traceback printed above.")
        
