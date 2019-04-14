# Makefile

# 此定义只支持GNU make
currentPath := $(shell pwd)/$(lastword $(MAKEFILE_LIST))
currentDir := $(shell dirname $(currentPath))
python = `which python`
pip = `which pip`
# Makefile不支持awk
pipInstallPath := $(shell $(pip) show pip | grep 'Location' | cut -d ' ' -f2)

# make all
# 	function: packageing app
#	command:  python setup.py sdist
#	usage: pip install dist/auto-solution-1.0.tar.gz
all:
	$(python) setup.py sdist

# make install
#	function: package and install
install:
	$(python) setup.py sdist
	$(pip) install dist/auto-solution-1.0.tar.gz

# make uninstall
#	function: delete useless file and uninstall app
uselessDirs = dist __pycache__ *.egg-info
uninstall:
	echo $(uselessDirs)
	for uselessDir in `echo $(uselessDirs)`; do \
		find $(currentDir) -type d -name $$uselessDir | xargs -i rm -rf {}; \
	done
	$(pip) uninstall auto-solution -y
	rm -rf $(pipInstallPath)/auto_solution

# make clean
#	function: delete useless file
clean:
	echo $(uselessDirs)
	for uselessDir in `echo $(uselessDirs)`; do \
		find $(currentDir) -type d -name $$uselessDir | xargs -i rm -rf {}; \
	done
