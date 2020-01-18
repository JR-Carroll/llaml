# llaml
_Lights, Lights, and More Lights_ is a pet project of mine (Justin Carroll) to automate _insert_random_doohikki_ around the house for the purposes of entertainment; the project started out as a Christmas-lights controller for the house, but has since grown in ambition for Halloween (which has motors and animatronics, etc).  As such, LLaML may have started small but has since grown to encompass anything that has a wireless signal and should be syncronized.

Main Features (most are still in development):
* Main Server (Qt-based application for designing routines/programs)
* Complimentary "client" (receiver) software that runs headless on an embedded/IoT device that has connectivity (think "RaspberryPi", Arduino support coming!).  GPIO pins are necessary...
* Audio support (currently WAV and MP3) for syncronizing music with lights
* "Fruity-loops"-like interface on widgets for "clicking-and-dragging" your duration of automation on, or off.
* PWM support (coming)
* Schedule songs/sycnronization programs
* Much more... 

## Requirements
It can be a little tricky to install LLaML in the beginnig because there is no `setup.py` or wheel at this time, but if you are handy with your distros package manager tools it shouldn't be too difficult!

* Linux distro (I build/develop on Debian)
* Python 2+ (but <3.0; port to 3 not yet planned, still finishing Python 2 implementation, maybe in 10+ years... =P)
* Matplotlib
* PySide (Qt4 bindings)
  To install PySide, one often needs the following as pre-reqs:
  * CMake (to compile PySide)
  * Qmake (qt4-qmake)
  * QT4-default
  * Alternatively, if you can find a wheel/pip of a binary of pyside, ultimately that's all you need.
  
  
