# This package is inspired and partially based on the AUR package
# by Christopher Snowhill, ipha, johnnybash and grmat.
# https://aur.archlinux.org/packages/opencl-amd/

# Download the source pkg with this command:
# wget --referer https://support.amd.com/en-us/kb-articles/Pages/AMDGPU-PRO-Driver-for-Linux-Release-Notes.aspx https://drivers.amd.com/drivers/linux/amdgpu-pro-20.20-1089974-ubuntu-20.04.tar.xz

# This package creates a wrapper file "amdgporun" which is similar to "optirun"
# or "primusrun" from Bumblebee times. In short, it enables the proprietary
# amdgpu-pro OpenCL stack on demand. If you want to eg. run Blender with it, you
# launch it the following way:
#
# $ amdgporun blender

# Important:
# The AMDGPU-PRO EULA forbids you from redistributing the source package.
# Therefore it's illegal to distribute the .src.rpm or .rpm files to third
# parties.

%global major 21.40.2
%global minor 1350683

# RPM flags
%global debug_package %{nil}

Name:           amdgpu-pro-vulkan
Version:        %{major}.%{minor}
Release:        1%{?dist}
Summary:        AMD Vulkan driver for AMD graphic cards

License:        EULA NON-REDISTRIBUTABLE
URL:            https://www.amd.com/en/support/kb/release-notes/rn-amdgpu-unified-linux-21-50-2
Source0:        http://repo.radeon.com/amdgpu/%{major}/ubuntu/pool/proprietary/v/vulkan-amdgpu-pro/vulkan-amdgpu-pro_%{major}-%{minor}_i386.deb
Source1:        http://repo.radeon.com/amdgpu/%{major}/ubuntu/pool/proprietary/v/vulkan-amdgpu-pro/vulkan-amdgpu-pro_%{major}-%{minor}_amd64.deb

%description
AMD Vulkan encoder userspace driver as provided in the amdgpu-pro driver stack. This package
is intended to work along with the free amdgpu stack.


%prep
mkdir files
# AMF
%ifarch i686
cp %{SOURCE0} .
ar x vulkan-amdgpu-pro_%{major}-%{minor}_i386.deb
%else
cp %{SOURCE1} .
ar x vulkan-amdgpu-pro_%{major}-%{minor}_amd64.deb
%endif
tar -xJC files -f data.tar.xz

%build
# fix vulkan loader path
pushd files/opt/amdgpu-pro/etc/vulkan/icd.d/
%ifarch i686
sed -i 's/\/opt\/amdgpu-pro\/lib\/i386-linux-gnu\//\/usr\/lib64\/amdgpu-pro-vulkan\//g' amd_icd32.json
mv amd_icd32.json amd_pro_icd32.json
%else
sed -i 's/\/opt\/amdgpu-pro\/lib\/x86_64-linux-gnu\//\/usr\/lib64\/amdgpu-pro-vulkan\//g' amd_icd64.json
mv amd_icd64.json amd_pro_icd64.json
%endif
popd

%install
mkdir -p %{buildroot}%{_datadir}/vulkan/icd.d/
mkdir -p %{buildroot}%{_libdir}/amdgpu-pro-vulkan

%ifarch i686
install -p -m755 files/opt/amdgpu-pro/lib/i386-linux-gnu/* %{buildroot}%{_libdir}/amdgpu-pro-vulkan/
%else
install -p -m755 files/opt/amdgpu-pro/lib/x86_64-linux-gnu/* %{buildroot}%{_libdir}/amdgpu-pro-vulkan/
%endif

install -p -m755 files/opt/amdgpu-pro/etc/vulkan/icd.d/* %{buildroot}%{_datadir}/vulkan/icd.d/


%files
%dir %{_libdir}/amdgpu-pro-vulkan/
%dir %{_datadir}/vulkan/icd.d/
%{_libdir}/amdgpu-pro-vulkan/*
%{_datadir}/vulkan/icd.d/*

%changelog
* Sun Jun 26 2022 update - 22.10.3.1420323
- Update to 22.10.3

* Sun Mar 27 2022 initial commit - 21.50.2.1384495
- Update to 21.50
