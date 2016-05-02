from urllib2 import Request, urlopen, URLError
import json
import time, calendar
from optparse import OptionParser
import os
def main():
	parser = OptionParser()
	parser.add_option("-i", "--id", dest="steamid",
                  help="steamID of user", default="76561198028369477")
	parser.add_option("-t", "--track", action="store_true", dest="track",
					help="track the user for a timeline", default=False)
	parser.add_option("-s", "--seconds", dest="seconds",
					help="seconds between api calls", default=60)
	(options, args) = parser.parse_args()

	f = open("apikey.txt","r");
	key = f.read()
	steamID = str(options.steamid)
	tracking = bool(options.track)
	seconds = int(options.seconds)
	if seconds < 5:
		seconds = 5
	url = url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + key + "&steamids=" + steamID

	request = Request(url)
	response = urlopen(request)
	predata = response.read()
	data = json.loads(predata)
	data["response"]["players"][0]["time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	data["response"]["players"][0]["absolutetime"] = calendar.timegm(time.gmtime())
	#print predata
	lastlogoff = time.strftime('%d %B %Y, %I:%M %p', time.localtime(data["response"]["players"][0]["lastlogoff"]))
	created = time.strftime('%d %B %Y, %I:%M %p', time.localtime(data["response"]["players"][0]["timecreated"]))
	print "Profile name: " + data["response"]["players"][0]["personaname"]
	print "Visibility: " + ("Private" if data["response"]["players"][0]["communityvisibilitystate"] == "1" else "Public") 
	print "Last logged off: " + lastlogoff
	print "Created: " + created
	print "Profile URL: " + data["response"]["players"][0]["profileurl"]
	print "SteamID: " + data["response"]["players"][0]["steamid"]
	print "Currently " + ("Offline" if data["response"]["players"][0]["personastate"] == 0 else "Online")
	if tracking:
		print ""
		print "Tracking SteamID " + data["response"]["players"][0]["steamid"] + " with interval "+ str(seconds)+"s"
		while True:
			stored_data = []
			with open(data["response"]["players"][0]["steamid"]+".json", "r") as outfile:			
				try:
					stored_data = json.load(outfile)
				except ValueError:
					stored_data = []

			with open(data["response"]["players"][0]["steamid"]+".json", "w") as outfile:
				stored_data.append(data["response"]["players"][0])
				json.dump(stored_data,outfile, indent=4)

			time.sleep(seconds)
			request = Request(url)
			response = urlopen(request)
			predata = response.read()
			data = json.loads(predata)
			data["response"]["players"][0]["time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
			data["response"]["players"][0]["absolutetime"] = calendar.timegm(time.gmtime())

			print ""
			print "Profile name: " + data["response"]["players"][0]["personaname"]
			print "Visibility: " + ("Private" if data["response"]["players"][0]["communityvisibilitystate"] == "1" else "Public") 
			print "Last logged off: " + lastlogoff
			print "Created: " + created
			print "Profile URL: " + data["response"]["players"][0]["profileurl"]
			print "SteamID: " + data["response"]["players"][0]["steamid"]
			print "Currently " + ("Offline" if data["response"]["players"][0]["personastate"] == 0 else "Online")
if __name__ == "__main__":
	main()
