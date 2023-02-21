import os
import subprocess

# Define frequency ranges and their corresponding modulations
frequency_ranges = {
    (30, 520): 'FM',
    (0.3, 30): ['AM', 'SSB'],
    (3.5, 30): 'CW',
}

fifo_path = 'pipe'

while True:
    # Prompt user to enter frequency or quit
    user_input = input("Enter Frequency in MHz or 'q' to quit: ")
    if user_input == 'q':
        # Terminate existing processes
        ices_process.terminate()
        icecast_process.terminate()
        gqrx_process.terminate()
        # Remove named pipe if it exists
        if os.path.exists(fifo_path):
            user_confirm = input(f"Are you sure you want to delete existing named pipe at {fifo_path}? Enter 'y' to confirm, or any other key to cancel: ")
            if user_confirm == 'y':
                os.remove(fifo_path)
                print(f"Removed named pipe at {fifo_path}")
            else:
                print(f"Keeping existing named pipe at {fifo_path}")
        break
    else:
        # Format frequency to have 4 decimal places
        frequency = "{:.4f}".format(float(user_input))
        
        # Prompt user to select modulation
        modulation_choices = frequency_ranges[float(frequency)]
        if isinstance(modulation_choices, str):
            modulation = modulation_choices
        else:
            modulation_str = ', '.join(modulation_choices)
            modulation = input(f"Multiple modulations are permitted for frequency {frequency} MHz. Please select a modulation from the following options: {modulation_str}: ")
            if modulation not in modulation_choices:
                print(f"Error: modulation {modulation} not supported for frequency {frequency} MHz.")
                continue

        # Create named pipe if it doesn't exist, otherwise prompt for confirmation before deleting
        if os.path.exists(fifo_path):
            user_confirm = input(f"Named pipe at {fifo_path} already exists. Enter 'y' to delete and recreate, or any other key to cancel: ")
            if user_confirm == 'y':
                os.remove(fifo_path)
                print(f"Removed existing named pipe at {fifo_path}")
            else:
                print(f"Keeping existing named pipe at {fifo_path}")
        try:
            os.mkfifo(fifo_path)
            print(f"Created named pipe at {fifo_path}")
        except FileExistsError:
            print(f"Named pipe at {fifo_path} already exists")

        # Tune to desired frequency and output audio to named pipe
        if modulation == 'FM':
            # For FM, use rtl_fm
            rtl_fm_process = subprocess.Popen(['rtl_fm', '-f', frequency + 'M', '-s', '2400000', '-', '|', 'sox', '-t', 'raw', '-r', '2400000', '-e', 's', '-b', '16', '-c', '1', '-V1', '-', fifo_path])
        else:
            # For AM, SSB, and CW, use GQRX
            gqrx_process = subprocess.Popen(['gqrx', '-r', 'none', '-f', frequency + 'M', '-M', modulation, '-s', '2400000', '- | sox -t raw -r 2400000 -e s -b 16 -c 1 -V1 - -t wav - | lame - -b 128 -', fifo_path])
        
        # Broadcast audio to Icecast server using ezstream
        ices_process = subprocess.Popen(['ezstream', '-c', 'icecast.xml'])

        # Read audio from named pipe and send to Icecast server using curl
        icecast_process = subprocess.Popen(['curl', '--retry', '5', '-T', fifo_path, '-u', 'source:hackme', 'http://localhost:8000/' + frequency + '_' + modulation])
