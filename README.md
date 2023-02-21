# RTL-SDR-Online-Radio-Broadcast

This program allows users to stream analog radio frequencies online using an RTL-SDR USB software-defined radio (SDR) and an Icecast streaming server.

## Requirements

-   Debian-based Linux distribution (tested on Ubuntu 20.04)
-   RTL-SDR USB SDR
-   Icecast server
-   GQRX, RTL-SDR, Sox, Lame, and Ezstream packages
-   Python 3

## Installation

1.  Install the required packages:

scssCopy code

`sudo apt install gqrx rtl-sdr sox lame ezstream python3` 

2.  Install the RTL-SDR USB SDR by following the instructions on the [official website](https://www.rtl-sdr.com/about-rtl-sdr/).
    
3.  Install and configure the Icecast server by following the instructions on the [official website](http://icecast.org/docs/icecast-2.4.1/config-file.html).
    
4.  Clone this repository to your local machine.
    

## Usage

1.  Open a terminal window and navigate to the directory where the repository was cloned.
    
2.  Run the program by executing the following command:
    

Copy code

`python3 broadcast.py` 

3.  Enter the frequency in MHz that you wish to stream. The program will prompt you to select a modulation based on the frequency range. If the frequency supports multiple modulations, the program will ask you to select one from a list.
    
4.  If a named pipe does not already exist, the program will create one in the local directory named `pipe`. If a named pipe already exists, the program will prompt you to confirm whether to delete it and create a new one.
    
5.  The program will tune to the desired frequency and output audio to the named pipe. If the modulation is FM, the program will use `rtl_fm` to output audio to the pipe. If the modulation is AM, SSB, or CW, the program will use `gqrx` to output audio to the pipe.
    
6.  The program will broadcast the audio from the named pipe to the Icecast server using `ezstream`.
    
7.  The program will read the audio from the named pipe and send it to the Icecast server using `curl`. The stream will be available at the URL `http://localhost:8000/frequency_modulation`, where `frequency` is the entered frequency in MHz and `modulation` is the selected modulation.
    
8.  To stop the program, enter `q` when prompted for the frequency. The program will terminate the processes and remove the named pipe.
    

## Troubleshooting

-   If the program cannot find the RTL-SDR USB SDR, make sure it is connected and the driver is loaded.
    
-   If the program cannot find the Icecast server, make sure it is running and the configuration file is correctly set up.
    
-   If the program prompts you to select a modulation that is not supported for the entered frequency, try a different modulation or frequency.
