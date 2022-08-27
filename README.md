# Documentation of Lukas' Work

## I/O from WVTICs to SPH-EXA
* Updated `parse_gadget_format_two.py` (included with WVTICs) to work in Python 3 (now parser_working.py)
* Created scripts to transform the Gadget2 binary to `.txt` file and SPH-EXA-compatible binaries/`.txt` files
* updated scripts to handle HDF5 files
* Added script to generate Kelvin-Helmholtz ICs out of glass blocks
*outdated/no longer used: 
	* Modified SPH-EXA's Sedov test case:
		* Modified `sedov.cpp` to accept file input like Evrard TODO: include checkpoint inputs
		* Included a hybrid file reader/generator for Sedov `SedovInputFileReader.hpp`
	* Created script to stack initial condition "boxes" to increase resolution
		NOTE: for constant densities only! 
	* Added script to "cut" Evrard initial conditions out of a glass block

### How to use: 
* Converting WVTICs outputs:
	1. to `.txt`: run ```python outputwriter.py <PATH>``` where PATH points to the WVTICs binary output
	2. to SPH-EXA format: run ```python outputwriter_sphexa.py <PATH>```. Outputs a HDF5 file.
		NOTE: currently the smoothing length is hardcoded to be divided by three to adjust to SPH-EXA's aim of ~100 neighbours
	3. cutting Evrard ICs out of a glass configuration block: run ```python evrard_cutter.py <PATH>``` where PATH points to a SPH-EXA compatible HDF5 file.
		
	4. creating Kelvin-Helmholtz ICs out of glass configuration blocks: run ```python kelvin-helmholtz_squeezer.py <PATH1> <PATH2>```
		where PATH1 is the outer (low-density) glass block and PATH2 the inner (high-density) block
		NOTE: this will create ICs with 128x the added number of particles of your input blocks
			in a box with size [1, 1, 0.0625] 

	Outdated, now handled at runtime in SPH-EXA:

	* upscaling your initial conditions: run ```python box_scaler.py <PATH> <NPART> <N> ``` where PATH points to a SPH-EXA compatible binary file, 
		NPART is the number of particles in the input file and N is the scaling factor (you will end up with N^3 particles in your output)
	* Sedov file reader:
		1. REPLACE your `sedov.cpp` and add the `SedovInputFileReader.hpp` to the sedov directory
		2. recompile
		3. specify a input file with the argument `--input <PATH>` where PATH leads to your binary input file
		NOTES: the number of particles in your file MUST be identical with your `-n` argument ^3
				if no input is specified, SPH-EXA will default to the built-in generator
				
## Contributions in SPH-EXA:
* Added Observables Interface and KH growth rate calculations (see https://github.com/lks1248/SPH-EXA/tree/kelvin-helmholtz)
* Added Gravitational waves Observable (see https://github.com/lks1248/SPH-EXA/tree/grav-waves-observable)
* different approaches to fixed boundaries:
	- immovable layer of particles (https://github.com/lks1248/SPH-EXA/tree/fixed-boundaries) 
	- discrete correction of pressure (https://github.com/lks1248/SPH-EXA/tree/fixed-boundaries-discrete-correction) not merged or fully tested
* expanded on the wind shock test case: added observable and extended domain (https://github.com/unibas-dmi-hpc/SPH-EXA/pull/297)

