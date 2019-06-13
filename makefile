all: blocks.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py parseimg.py texture.py
	python3 main.py blocks.mdl

clean:
	rm *pyc *out parsetab.py

clear:
	rm *pyc *out parsetab.py *ppm
