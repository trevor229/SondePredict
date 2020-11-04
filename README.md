# SondePredict - A fork of the CUSF Predictor Wrapper
![main_image](https://github.com/trevor229/SondePredict/main_image.png)

This is a modified version of the CUSF Predictor Wrapper, which features a somewhat improved web UI, custom icons, and a few new features. This fork is targeted primarily at US based users who wish to predict the flight paths of National Weather Service radiosondes.

## Reasons for changes
------

I personally found the original [CUSF Standalone Predictor](https://github.com/jonsowman/cusf-standalone-predictor/) difficult to setup and could not get it to work properly. In addition, the software is over 10 years old now, which is where most of the difficulty comes from. 

The forked [CUSF Predictor Wrapper](https://github.com/darksidelemm/cusf_predictor_wrapper) is better, but still has some shortcomings and poor features. 


## This version is linux only! The main scripts do not support Windows/OSX. Sorry!

## Setup
------
## 1. Install the Python Wrapper
Clone this repository with:
```
$ git clone https://github.com/trevor229/SondePredict.git
```

The wind data downloader script depends on python-gdal, which needs gdal installed.
GDAL may need to be installed separately using the system package manager, for example:
```
Debian/Ubuntu: apt-get install python-gdal
```

The custpredict python package can then be installed in the usual Python way:
```
$ cd SondePredict
$ sudo python setup.py install
```

This should grab the other required Python dependencies, but if not, they are:
 * python-dateutil
 * shapely
 * fastkml
 * python-gdal (which may have been installed via apt-get previously)
---
## 2. Building the Predictor
The predictor itself is a binary ('pred'), which we (currently) build seperately, using CMake.
You may need to install `cmake` and `libglib2.0-dev` via your package manager before building, i.e.
```
$ sudo apt-get install cmake libglib2.0-dev
```

Then, from within the cusf_predictor_wrapper directory, run the following to build the predictor binary:

```
$ cd src
$ mkdir build
$ cd build
$ cmake ../
$ make
```

The `pred` binary then needs to be copied into the 'apps' directory for SondePredict to work
```
$ cp pred ../../apps/
```
---
## 3. Configuration
There are variables within `sonde_predict.sh` and `index.html` that *must* be changed before running, as well as some optional ones that you can change if you like. Look at [this page in the wiki for details](https://github.com/trevor229/SondePredict/wiki/Configuration).

**Don't forget to make the `sonde_predict.sh` script executable!**

```
$ sudo chmod +x sonde_predict.sh
```

---
## 4. Setting up the webpage
Copy the contents of the `web` folder to a directory that can be served by your favorite web server
  * By default, `sonde_predict.sh` copies the `sonde_predictions.json` file to `/var/www/html` so if you do not have your `index.html` and `static` directory there then make sure to change the `cp` command in `sonde_predict.sh` to reflect your chosen location.

* Dont forget to change the required variables in `index.html`!

---
## 5. Setting up automatic predictions
I opted to used systemd for this since I can never seem to get cron to work. 

Create the systemd service file
```
$ sudo nano /etc/systemd/system/sondepredict.service
```
Then add the following, making sure to change `WorkingDirectory` and `ExecStart` to the location of where the `SondePredict` directory is.
```
[Unit]
Description=SondePredict Service

[Service]
Type=oneshot
WorkingDirectory=<YOUR_WORKING_DIR_HERE>/SondePredict/apps
ExecStart=<YOUR_PATH_HERE>/SondePredict/apps/sonde_predict.sh
```
Save and close the file. Next, create the systemd timer

```
$ sudo nano /etc/systemd/system/sondepredict.timer
```
And add the following. Note the `OnUnitActive` time is 6 hours. This is the interval which should be kept for new GFS data to be downloaded without unnessicarily downloading and rerunning the predictor.
```
[Unit]
Description=SondePredict Service

[Timer]
OnUnitActiveSec=21600s
OnBootSec=10s

[Install]
WantedBy=timers.target
```
Save and close. Make sure to reload the daemon. Then enable and start the timer.

```
$ sudo systemctl daemon-reload
$ sudo systemctl enable sondepredict.timer
$ sudo systemctl start sondepredict.timer
```
---
## 6. (Recommended) Running once to test/startup
Running the `sonde_predict.sh` script once even after enabling/starting the systemd service is recommended to ensure your configuration is correct and to also give the web application a valid `sonde_predictions.json` file to load (The map will not display itself without one!)

Just go to your `SondePredict/apps` directory, and run it

```
$ ./sonde_predict.sh
```
If everything is working, you should see an output similar to this
```
INFO:root:Testing Model: 20201104/06
INFO:root:Testing Model: 20201104/00
INFO:root:Found valid data in model 20201104/00!
INFO:root:Created temporary directory /tmp/tmpoYn4JA
INFO:root:Starting download of wind data...
INFO:root:GRIB request took 4.4 seconds.
INFO:root:Downloaded data for T+000
INFO:root:Processing GRIB file...
INFO:root:GFS data written to: /tmp/tmpoYn4JA/gfs_1604448000_41.0_270.0_10.0_10.0.dat
...
INFO:root:Downloaded data for T+048
INFO:root:Processing GRIB file...
INFO:root:GFS data written to: /tmp/tmpoYn4JA/gfs_1604620800_41.0_270.0_10.0_10.0.dat
INFO:root:Writing out dataset info.
INFO:root:Finished!
Prediction Run: 2020-11-04-0000Z,5.0,5.0
Prediction Run: 2020-11-04-1200Z,5.0,5.0
Prediction Run: 2020-11-05-0000Z,5.0,5.0
Prediction Run: 2020-11-05-1200Z,5.0,5.0
```
---
## Copyrights
The original [CUSF Predictor Wrapper](https://github.com/darksidelemm/cusf_predictor_wrapper) software is [licensed under the GNU General Public License v3.0](https://github.com/darksidelemm/cusf_predictor_wrapper/blob/master/LICENSE). As such this fork is also under the same license

The SVG icons located in the `/apps/web/static/images` folder were created by me and are hereby also licensed under the GNU General Public License v3.0


