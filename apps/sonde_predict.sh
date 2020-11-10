#!/bin/bash
#
#   Example script for grabbing the following week's wind data,
#   and then running predictions of radiosonde launches from a site.
#
#   Mark Jessop <vk5qi@rfhead.net>
#
#   For this script to work, you need
#     - cusf_predictor_wrapper installed and available on the current python path.
#     - get_wind_data.py in this directory (should already be the case)
#     - The 'pred' binary available in this directory.
#
#   New GFS models are available every 6 hours, approximately 3-4 hours after the model
#   start time (00/06/12/18Z).
#
#   I use the following crontab entry to run this script at a time where the model is either available,
#   or close to being available.
#
#   40 3,9,15,21 * * * /home/username/cusf_predictor_wrapper/apps/sonde_predict.sh

# Home location latitude & longitude
LAUNCH_LAT=0.0
LAUNCH_LON=0.0

# Launch site name. Usually a callsign of the WFO
LAUNCH_SITE_STR="TEST"

# Time of first daily launch. Must be in UTC. Default is 00:00Z for NWS launches
LAUNCH_START_TIME="00:00Z"

# Time between launches, starting at LAUNCH_START_TIME. Default is 12 for NWS launches (Twice a day at 00z and 12z)
LAUNCH_STEP=12

# Area to grab data for. +/- 10 degrees is usually plenty!
LATLON_DELTA=10

# How many hours to grab data for. 192 hours = 8 days, which is about the extent of the GFS model
HOUR_RANGE=48

# Set to true for the email notifier to run when sondes are predicted to land nearby
EMAIL_NOTIFY=false

# We assume this script is run from the cusf_predictor_wrapper/apps directory.
# If this is not the case (e.g. if it is run via a cronjob), then you may need
# to modify and uncomment the following line.
#cd /home/username/cusf_predictor_wrapper/apps/

# Clear old GFS data.
rm gfs/*.txt
rm gfs/*.dat
rm sonde_predictions.*

# Download the wind data.
# Note that this will wait up to 3 hours for the latest wind data to become available.
python get_wind_data.py --lat=$LAUNCH_LAT --lon=$LAUNCH_LON --latdelta=$LATLON_DELTA --londelta=$LATLON_DELTA -f $HOUR_RANGE -m 0p25_1hr -o gfs/

# Run predictions
python sonde_predict.py --step=$LAUNCH_STEP --time=$LAUNCH_START_TIME --limit=$HOUR_RANGE --latitude=$LAUNCH_LAT --longitude=$LAUNCH_LON --site=$LAUNCH_SITE_STR

# Run the email script if enabled
if [ "$EMAIL_NOTIFY" = true ] ; then
    python geoLocateCoords.py
fi

# Copy the resultant json file into the web interface directory.
# If the web interface is being hosted elsewhere, you may need to replace this with a SCP
# command to get the json file into the right place, e.g.
# scp sonde_predictions.json mywebserver.com:~/www/sondes/
cp sonde_predictions.json /var/www/html
