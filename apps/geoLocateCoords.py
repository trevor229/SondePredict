import json
import geopy.distance
import gmailHandler
from tabulate import tabulate

# If True, calculate distance in miles, not km
useImperial=True
home_latlon=(0.0,0.0)

# Range in your unit to notify when a radiosonde is predicted to land
# You will be notified of landings that are equal to or less than this distance from you
notify_range=50

# Initialize an array for the prediction timestamps and lengths. 
# WIll only contain timestamp/distance pairs for sondes within notify_range
distanceInfo = []

# Open the predictions json and load it
with open('sonde_predictions.json') as f:
    data = json.load(f)

# Loop through json predictions
for i in data['predictions'].values():

    # Save the lat and lon of the last prediction point (the landing) for later use
    sonde_latlon = (i['path'][len(i['path'])-1][0], i['path'][len(i['path'])-1][1])
    
    # If user set their units to Miles
    if useImperial:
        distanceMi = geopy.distance.geodesic(home_latlon, sonde_latlon).miles
        # Check to see if the distance between user and sonde landing is within notify_range
        if distanceMi <= notify_range:
            distanceInfo.append([i['timestamp'], '%.2f' % distanceMi])
    # Otherwise we assume Kilometers
    else:
        distanceKm = geopy.distance.geodesic(home_latlon, sonde_latlon).km
        # Check to see if the distance between user and sonde landing is within notify_range
        if distanceKm <= notify_range:
            distanceInfo.append([i['timestamp'], '%.2f' % distanceKm])

# Check to see if we actually ended up with any nearby landings
if len(distanceInfo) != 0:

  # Sort our nearby sonde predictions by distance from the user
  distanceInfo.sort(key=lambda x: float(x[1]))

  # Check units and then tabulate our data
  if useImperial:
      HTMLTable = tabulate(distanceInfo, headers=["Timestamp", "Distance (mi.)"], floatfmt=".2f", tablefmt="html", numalign="center", stralign="center")
  else:
      HTMLTable = tabulate(distanceInfo, headers=["Timestamp", "Distance (km.)"], floatfmt=".2f", tablefmt="html", numalign="center", stralign="center")

  # Define our HTML message for the email
  email_body = """
  <html>
  <head>
  <style>
  th {
  font-size: 150%;
  }
  td {
  font-size: 125%;
  }
  table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
  }
  th, td {
    padding: 15px;
    text-align: left;
  }
  tr:nth-child(even) {
    background-color: #eee;
  }
  tr:nth-child(odd) {
  background-color: #fff;
  }
  th {
    background-color: black;
    color: white;
  }
  </style>
  <head>
  <body>
  <h2>Heads up, there are some sondes predicted to land near you!</h2>
  """ + HTMLTable + "</body></html>"

  # Finally, run our email module with the subject and body as arguments
  gmailHandler.mail(str(len(distanceInfo)) + " Sonde(s) predicted to land near you!", email_body)

# If no landings nearby, just console log it
else:
  print("No sondes predicted to land near "+ str(home_latlon))
