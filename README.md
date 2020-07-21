# CloudedBats - Sound

**Note: Work in progress. For test only.**

## sound4bats

The software library sound4bats will be used to extract and handle the sound parts that are produced by bats. The library dsp4bats takes care of the basic and more generic sound processing steps both in the time and the frequency domains. The goal is to separate pulses from harmonics and noise to extract the more precise shape of each pulse. Sequences of pulses is also of interrest since that can be used for statistical analysis.

## Installation for desktop application

    git clone https://github.com/cloudedbats/cloudedbats_sound.git
    cd cloudedbats_sound/
    python3 -m venv venv
    source venv/bin/activate
    sudo apt-get install python3-pyqt5
    pip install -r requirements.txt 
    pip install git+https://github.com/cloudedbats/cloudedbats_dsp
    # Run.
    python desktop_test_app_main.py 

## Contact

Arnold Andreasson, Sweden.

info@cloudedbats.org
