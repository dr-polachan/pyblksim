# PyBlkSim
An Open-Source Model-Based Simulator for Discrete-Time Simulations

- **Source Code**
  - Refer to `./pyblksim`

- **Installation**
  - PyBlkSim is available on the Python Package Index (PyPI).
  - Install using the following command:
    ```bash
    $ pip install pyblksim
    ```

## Examples

For examples, refer to the `./examples` directory. For more details on these example scripts, see:

> Kurian Polachan and Bijeet Basak, "PyBlkSim: An Open-Source Block-Based Discrete-Time Simulator," in *Proceedings of the 17th International Conference on Communication Systems & Networks (COMSNETS 2025)*, Bangalore, India.

### Steps to Run the Example, `example-sources-n-scopes`

1. Open a terminal and execute the script using the following command:
    ```bash
    $ python ./example_sources_scope_file.py
    ```
   This will pop up three windows displaying sinusoidal, noise, and ramp signals. The script will also save these signals in CSV format.

2. To view these signals in a single window, run the post-processing script:
    ```bash
    $ python example_fig_generation
    ```
   The generated figure will be saved in `./examples/example-sources-n-scopes`.

## Citation
If you are using PyBlkSim for your work, please cite:

> Kurian Polachan and Bijeet Basak, "PyBlkSim: An Open-Source Block-Based Discrete-Time Simulator," in *Proceedings of the 17th International Conference on Communication Systems & Networks (COMSNETS 2025)*, Bangalore, India.

## Contact
For questions on using the simulator, please reach out to Kurian Polachan at [kurian.polachan@iiitb.ac.in](mailto:kurian.polachan@iiitb.ac.in) or visit [https://iiitb.ac.in/faculty/kurian-polachan](https://iiitb.ac.in/faculty/kurian-polachan).
