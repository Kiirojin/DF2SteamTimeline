import plotly
print plotly.__version__  # version >1.9.4 required
from plotly.graph_objs import Scatter, Layout
from optparse import OptionParser
import json
def main():
	parser = OptionParser()
	parser.add_option("-i", "--id", dest="steamid",
                  help="steamID of user", default="76561198028369477")
	(options, args) = parser.parse_args()
	steamID = str(options.steamid)

	with open(steamID+".json") as f:
		data = json.load(f)
	
	x = []
	y = []
	traces = []
	count = 0
	prevtime = 0
	for num in range(len(data)):
		i = data[num]
		status = "Offline" if i["personastate"] == 0 else "Online"
		if count == 0:
			x.append(i["time"])
			y.append(status)
		elif num < len(data)-1:
			if y[len(y)-1] != status:
				if i["absolutetime"] - prevtime > 600:
					traces.append(Scatter(x=x, y=y))
					count = 0
					x=[]
					y=[]
					x.append(i["time"])
					y.append(status)
				else:
					x.append(i["time"])
					y.append("Online" if status == "Offline" else "Offline")
					x.append(i["time"])
					y.append(status)
				
			else:
				if i["absolutetime"] - prevtime > 600:
					traces.append(Scatter(x=x, y=y))
					count = 0
					x=[]
					y=[]
				x.append(i["time"])
				y.append(status)	
		else:
			traces.append(Scatter(x=x, y=y))
		count += 1
		prevtime = i["absolutetime"]

	plotly.offline.plot({
	"data": traces,
	"layout": Layout(
	    title="Timeline for " + data[0]["personaname"] + "(id:"+data[0]["steamid"]+")"
	)
	})

if __name__ == "__main__":
	main()
