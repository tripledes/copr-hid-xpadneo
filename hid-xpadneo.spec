%define project_name xpadneo
%define real_name hid-%{project_name}
%define udev_scriptdir /lib/udev
%define modprobed_dir /etc/modprobe.d

Name:               dkms-%{real_name}
Version:            0.9.1
Release:            1%{?dist}
Summary:            Advanced Linux Driver for Xbox One Wireless Gamepad

License:            GPLv3
URL:                https://atar-axis.github.io/%{project_name}/
Source0:            https://github.com/atar-axis/%{project_name}/archive/refs/tags/v%{version}.tar.gz
Source1:            99-xpadneo-bluetooth.conf
# Remove post-{install,remove} dkms hooks
Patch0:             hid-xpadneo-dkms-conf-in.patch
Group:              System Environment/Kernel

BuildArch:          noarch
Requires:           gcc, make
Requires(post):     dkms
Requires(preun):    dkms

%description
Advanced Linux Driver for Xbox One Wireless Gamepad

%prep
%setup -q -n %{project_name}-%{version}
%patch0 -p1

%build

%install
%{__rm} -rf %{buildroot}

%define dkms_name %{real_name}
%define dkms_vers %{version}-%{release}
%define quiet -q

# Kernel module sources install for dkms
%{__mkdir_p} %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
%{__mkdir_p} %{buildroot}%{udev_scriptdir}/rules.d/
%{__mkdir_p} %{buildroot}%{modprobed_dir}/

sed 's/"@DO_NOT_CHANGE@"/"'"%{version}"'"/g' %{real_name}/dkms.conf.in > %{real_name}/dkms.conf
cp --recursive %{real_name}/{src,Makefile,dkms.conf} %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
rm %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/src/.editorconfig
install -m 0644 %{real_name}/etc-udev-rules.d/60-xpadneo.rules  %{buildroot}%{udev_scriptdir}/rules.d/
install -m 0644 %{real_name}/etc-modprobe.d/xpadneo.conf  %{buildroot}%{modprobed_dir}/
install -m 0644 %{SOURCE1} %{buildroot}%{modprobed_dir}/99-xpadneo-bluetooth.conf

%post
# Add to DKMS registry
dkms --rpm_safe_upgrade add -m %{dkms_name} -v %{version} %{quiet}
# Rebuild and make available for the currenty running kernel
dkms --rpm_safe_upgrade build -m %{dkms_name} -v %{version} %{quiet}
dkms --rpm_safe_upgrade install -m %{dkms_name} -v %{version} --force %{quiet}

%preun
# Remove all versions from DKMS registry
dkms --rpm_safe_upgrade remove -m %{dkms_name} -v %{version} --all %{quiet}

%files
%defattr(-, root, root, -)
%doc NEWS.md docs/{3P-BUGS.md,BT_DONGLES.md,CONFIGURATION.md,README.md,SDL.md,SECUREBOOT.md,TROUBLESHOOTING.md}
%license LICENSE
%{_usrsrc}/%{dkms_name}-%{version}/
%{udev_scriptdir}/rules.d/60-xpadneo.rules
%{modprobed_dir}/xpadneo.conf
%{modprobed_dir}/99-xpadneo-bluetooth.conf

%changelog
* Tue Jan 04 2022 Sergi Jimenez <tripledes@fedoraproject.org> - 0.9.1-1
- Initial build
