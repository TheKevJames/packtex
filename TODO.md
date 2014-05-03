TODO
====

* Add tests
* Clean up code
* Features
	* Explicit error handling (pip --exists-action [...])
	* Handle user- and system-installed packages (kpsewhich)
	* Install custom packages (i.e. not from CTAN)
	* Install from requirements file (pip install -r requirements.txt)
		* Dependency extraction from tex and sty files
	* Mark dependencies with exact or fuzzy versions (pip freeze)
		* Default: package>=installed,package<next_major_version?
	* Search CTAN (pip search). Must be able to `packtex search algorithm` -> `algorithms`
	* Operation logging
* Fix
	* Filenames like `bst` are picked up as extensions (see `packtex install biblatex`)
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
