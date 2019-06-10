

copy contents of this folder to parent folder

sphinx-apidoc -f -P -o tmp/source lkmltools
sphinx-apidoc -f -P -o tmp/source lkmltools/linter
sphinx-apidoc -f -P -o tmp/source lkmltools/linter/rules/
sphinx-apidoc -f -P -o tmp/source lkmltools/linter/rules/filerules
sphinx-apidoc -f -P -o tmp/source lkmltools/linter/rules/fieldrules
sphinx-apidoc -f -P -o tmp/source lkmltools/linter/rules/otherrules
sphinx-apidoc -f -P -o tmp/source lkmltools/updater
sphinx-apidoc -f -P -o tmp/source lkmltools/grapher

make clean

make html

#mkdir docs

rm -rf docs

mv _build/html docs/

git add docs/

git commit

git push
