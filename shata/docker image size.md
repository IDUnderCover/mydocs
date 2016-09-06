##docker tips

### docker image size

1. aufs, copy on write， deep layers，search，copy and write
2. A large image will be harder to distribute. Pulling large image from Registry concurently may causes network error 


###How to minimize image size？
1. chain your commands
2. use `docker export $cid |　docker import` instructions to flatten your images (the metadata of image will lost)




###References:
[Image Layers, CenturyLink](https://imagelayers.io/)
  
[Ten things to avoid in docker containers](http://developers.redhat.com/blog/2016/02/24/10-things-to-avoid-in-docker-containers/)  
[Optimizing docker images](https://www.ctl.io/developers/blog/post/optimizing-docker-images/)  
[Docker image base os size comparison](https://www.brianchristner.io/docker-image-base-os-size-comparison/)