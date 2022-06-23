#!/bin/sh

sudo dnf -y install mock pykickstart fedpkg libvirt

# download AMD's AMDF libraries
if [ ! -f "vulkan-amdgpu-pro_21.50.2-1384495_amd64.deb" ]; then
wget --referer https://www.amd.com/en/support/kb/release-notes/rn-amdgpu-unified-linux-21-50 -N http://repo.radeon.com/amdgpu/21.50.2/ubuntu/pool/proprietary/v/vulkan-amdgpu-pro/vulkan-amdgpu-pro_21.50.2-1384495_amd64.deb
fi
if [ ! -f "vulkan-amdgpu-pro_21.50.2-1384495_i386.deb" ]; then
wget --referer https://www.amd.com/en/support/kb/release-notes/rn-amdgpu-unified-linux-21-50 -N http://repo.radeon.com/amdgpu/21.50.2/ubuntu/pool/proprietary/v/vulkan-amdgpu-pro/vulkan-amdgpu-pro_21.50.2-1384495_i386.deb
fi

# create a fedora srpm from the spec sheet
fedpkg --release f36 srpm

# add current user to 'mock' build group
sudo usermod -a -G mock $USER

# turn selinux off if it's enabled
sudo setenforce 0

# build the package
# x86_64
mock -r /etc/mock/fedora-36-x86_64.cfg --rebuild amdgpu-pro-vulkan*.src.rpm
sudo mv /var/lib/mock/fedora-36-x86_64/result/* .
# i386
mock -r /etc/mock/fedora-36-i386.cfg --rebuild amdgpu-pro-vulkan*.src.rpm
sudo mv /var/lib/mock/fedora-36-i686/result/* .

# re-enable selinux if needed
sudo setenforce 1

# install the package
sudo dnf -y --nogpgcheck install amdgpu-pro-vulkan*.x86_64.rpm amdgpu-pro-vulkan*.i686.rpm

# cleanup
rm *.log
mock -r /etc/mock/fedora-36-x86_64.cfg --scrub=all
mock -r /etc/mock/fedora-36-i386.cfg --scrub=all
