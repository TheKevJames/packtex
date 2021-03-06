TODO
====

* Add tests
* Features
	* Ability to install build systems (biblatex, etex, latex, luatex, pdflatex, xetex)
	* Add pre-installed packages (`packtex init`?)
	* Explicit error handling (`pip --exists-action [...]`)
		* Standardize error handling with rollbacks
	* Handle user- and system-installed packages (`kpsewhich`)
	* Install custom packages (i.e. not from CTAN)
	* Search CTAN (pip search). Must be able to `packtex search algorithm` -> `algorithms`
* Look into TeXHash
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
* Bugs
	* Does not run Makefiles
	* Dependency packages end up in wrong log
	* See `failed_dependency' <- should be solved by `packtex search'
	* expl3 installs twice (with l3docstrip)
