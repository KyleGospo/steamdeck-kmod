%if 0%{?fedora}
%global debug_package %{nil}
%endif

Name:     steamdeck
Version:  {{{ git_dir_version }}}
Release:  1%{?dist}
Summary:  Driver exposing various bits and pieces of functionality provided by Steam Deck specific VLV0100 device
License:  GPLv2
URL:      https://github.com/KyleGospo/steamdeck-kmod

Source:   %{url}/archive/refs/heads/main.tar.gz

Provides: %{name}-kmod-common = %{version}
Requires: %{name}-kmod >= %{version}

BuildRequires: systemd-rpm-macros

%description
Driver exposing various bits and pieces of functionality provided by Steam Deck specific VLV0100 device presented by EC firmware.
This includes but not limited to:
- CPU/device's fan control
- Read-only access to DDIC registers
- Battery tempreature measurements
- Various display related control knobs
- USB Type-C connector event notification

%prep
%setup -q -c %{name}-kmod-main

%build
install -D -m 0644 %{name}-kmod-main/%{name}.conf %{buildroot}%{_modulesloaddir}/%{name}.conf

%files
%doc %{name}-kmod-main/README.md
%license %{name}-kmod-main/LICENSE
%{_modulesloaddir}/%{name}.conf

%changelog
{{{ git_dir_changelog }}}
