TODO
====

* Add tests
* Clean up code
* Features
	* Explicit error handling (pip --exists-action [...])
	* Handle user- and system-installed packages (kpsewhich)
	* Install custom packages (i.e. not from CTAN)
	* Install from requirements file (pip install -r requirements.txt)
	* Search CTAN (pip search)
	* Operation logging
* Standardize error handling with rollbacks
* Support alternate set ups
	* OS
		* Mac
		* Unix
		* Windows
			* texmf: figure out where to look for this
			* OTF: configure font_dir stuff
	* *TeX
		* BibTeX
		* LaTeX
		* LuaTeX
		* TeX
		* XeTeX
	* Managers
		* MacTex
		* MikTex
		* TeXLive
		* ...
