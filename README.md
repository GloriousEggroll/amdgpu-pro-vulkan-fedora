This downloads the proprietary amdgpu-pro Vulkan component debian packages, converts them to Fedora RPMs, and installs them on the system


1. Just run the install script and it should create and install the packages:

```
./install.sh
```

2. Install the amdgpu-vulkan-switcher from copr:
```
sudo dnf copr enable gloriouseggroll/amdgpu-vulkan-switcher 
sudo dnf install -y amdgpu-vulkan-switcher
```

3. Usage:

Mesa RADV:
```
$ vk_radv command
```

amdgpu-pro:
```
$ vk_pro command
```
