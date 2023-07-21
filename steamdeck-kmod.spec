%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

Name:     steamdeck-kmod
Version:  {{{ git_dir_version }}}
Release:  1%{?dist}
Summary:  Driver exposing various bits and pieces of functionality provided by Steam Deck specific VLV0100 device
License:  GPLv2
URL:      https://github.com/KyleGospo/steamdeck-kmod

Source:   %{url}/archive/refs/heads/main.tar.gz
Source1:  https://gitlab.com/evlaV/linux-integration/-/raw/6.1.29-valve8/drivers/mfd/steamdeck.c
Source2:  https://gitlab.com/evlaV/linux-integration/-/raw/6.1.29-valve8/drivers/extcon/extcon-steamdeck.c
Source3:  https://gitlab.com/evlaV/linux-integration/-/raw/6.1.29-valve8/drivers/hwmon/steamdeck-hwmon.c
Source4:  https://gitlab.com/evlaV/linux-integration/-/raw/6.1.29-valve8/drivers/leds/leds-steamdeck.c

BuildRequires: kmodtool

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Driver exposing various bits and pieces of functionality provided by Steam Deck specific VLV0100 device presented by EC firmware.
This includes but not limited to:
- CPU/device's fan control
- Read-only access to DDIC registers
- Battery tempreature measurements
- Various display related control knobs
- USB Type-C connector event notification

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c steamdeck-kmod-main
cp %{SOURCE1} steamdeck-kmod-main/steamdeck.c
cp %{SOURCE2} steamdeck-kmod-main/extcon-steamdeck.c
cp %{SOURCE3} steamdeck-kmod-main/steamdeck-hwmon.c
cp %{SOURCE4} steamdeck-kmod-main/leds-steamdeck.c

find . -type f -name '*.c' -exec sed -i "s/#VERSION#/%{version}/" {} \+

for kernel_version  in %{?kernel_versions} ; do
  cp -a steamdeck-kmod-main _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 _kmod_build_${kernel_version%%___*}/steamdeck.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/steamdeck.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/extcon-steamdeck.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/extcon-steamdeck.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/steamdeck-hwmon.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/steamdeck-hwmon.ko
 install -D -m 755 _kmod_build_${kernel_version%%___*}/leds-steamdeck.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/leds-steamdeck.ko
done
%{?akmod_install}

%changelog
{{{ git_dir_changelog }}}
