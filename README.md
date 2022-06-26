# NS3-based Wi-Fi Test
> NS3-based Indoor WLAN test with various applications, developed with Python bindings front-end.

### Preparation

- Install NS3 and the dependencies via one step: `make install-ns3`.

- We currently use `ns-3.36.1` and the corresponding patches in the `src` folder.

- You can customize the installation in `scripts/install.sh` script.

### Development

1. Define your custom application, network, and etc. resembling the `$NS3_HOME/src` folder structure in `$PWD/src`;
  > Don't forget to also modify the CMakeLists.txt file.

2. Define the simulation process in the Python files, e.g. `main.py`;

3. Run the simulation always after running `make build`, or use `make run` without parameters given.
