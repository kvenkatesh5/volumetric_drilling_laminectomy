# Hardware installation manual

## Geomaigc Touch/ Phantom Omni
```bash
sudo PHANToMConfiguration
mkdir catkin_ws
cd catkin_ws/
mkdir src
cd src/
catkin_init_workspace 
git clone git@github.com:WPI-AIM/ros_geomagic.git
cd ..
catkin_make
source devel/setup.bash 
roslaunch geomagic_control geomagic_headless.launch 
sudo chmod a+x /dev/fw*
roslaunch geomagic_control geomagic_headless.launch device_name:="Default PHANToM"

cd ambf/
cd external/chai3d/extras/hdPhantom/
ls
sudo ./linux-installation.sh 
```

## JONATHAN HERE: https://github.com/jhu-saw/sawSensablePhantom/blob/master/drivers.md <---  I followed this to get the Phantom OMNI GUI to show up?
## https://github.com/jhu-cisst-external/phantom-omni-1394-drivers <--- followed this to get the drivers installed? 

If the Phantom Omni device was not recognised during the initialization.
Please try the following command again.

```bash
chmod a+rwx /dev/fw*
```

## Head Mount Display
We are using VIVE PRO 2 for this project. 
Please refer to the follwing website: https://github.com/OpenHMD/OpenHMD/wiki/Xorg .

[Warning] If you create the 99-HMD.config, the laptop screen will be disabled. Please be careful and be sure to have external monitor.

```bash
cd /usr/share/X11/xorg.conf.d/
sudo mv 99-HMD.conf 99-HMD.conf.bak # rename the file to enable your laptop screen
```
