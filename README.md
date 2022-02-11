# Documentation of Lukas' Work

## I/O from WVTICs to SPH-EXA
* Updated `parse_gadget_format_two.py` to work in Python 3 TODO: (now gadget_two_parser.py)
* Created scripts to transform the Gadget2 binary to `.txt` file and SPH-EXA-compatible binaries/`.txt` files
* Modified SPH-EXA's Sedov test case:
	* Modified `sedov.cpp` to accept file input like Evrard TODO: include checkpoint inputs
	* Included a hybrid file reader/generator for Sedov `SedovInputFileReader.hpp`
* Created script to stack initial condition "boxes" to increase resolution
	NOTE: for constant densities only! 

### How to use: 
* Sedov file reader:
	1. REPLACE your `sedov.cpp` and add the `SedovInputFileReader.hpp` to the sedov directory
	2. recompile
	3. specify a input file with the argument `--input <PATH>` where PATH leads to your binary input file
		NOTES: the number of particles in your file MUST be identical with your `-n` argument ^3
				if no input is specified, SPH-EXA will default to the built-in generator
* Converting WVTICs outputs:
	1. to `.txt`: run ```python outputwriter.py <PATH>``` where PATH points to the WVTICs binary output
	2. to SPH-EXA format: run ```python outputwriter_sphexa.py <PATH>```
		NOTE: currently the smoothing length is hardcoded to be divided by three to adjust to SPH-EXA's aim of ~100 neighbours
	3. upscaling your initial conditions: run ```python box_scaler.py <PATH> <NPART> <N> ``` where PATH points to a SPH-EXA compatible binary, 
		NPART is the number of particles in the input file and N is the scaling factor (you will end up with N^3 particles in your output)