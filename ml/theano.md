## Theano Installation on Ubuntu 16.04

	sudo apt-get install python-numpy python-scipy python-dev python-pip python-nose g++ libopenblas-dev git
	sudo pip install Theano
	
	# cuda 7.5 don't support the default g++ version. Install an supported version and make it the default.
	sudo apt-get install g++-4.9
	
	sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 20
	sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 10
	
	sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.9 20
	sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 10
	
	sudo update-alternatives --install /usr/bin/cc cc /usr/bin/gcc 30
	sudo update-alternatives --set cc /usr/bin/gcc
	
	sudo update-alternatives --install /usr/bin/c++ c++ /usr/bin/g++ 30
	sudo update-alternatives --set c++ /usr/bin/g++
	
	# Work around a glibc bug
	echo -e "\n[nvcc]\nflags=-D_FORCE_INLINES\n" >> ~/.theanorc

.~/theanorc 配置文件
                                                                                              
	[nvcc]
	flags=-D_FORCE_INLINES
	[blas]
	ldflags=-L/usr/lib/ -lblas
	[global]
	floatX=float32
	device = gpu0
	[lib]
	cnmem = 0.8



reference:
http://deeplearning.net/software/theano/install_ubuntu.html#install-ubuntu