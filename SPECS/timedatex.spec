%global _hardened_build 1

Name:		timedatex
Version:	0.5
Release:	3%{?dist}
Summary:	D-Bus service for system clock and RTC settings

Group:		System Environment/Daemons
License:	GPLv2+
URL:		https://github.com/mlichvar/timedatex
Source0:	https://github.com/mlichvar/timedatex/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	glib2-devel libselinux-devel systemd
Requires:	polkit systemd util-linux

Patch1:		timedatex-timeout.patch

%description
timedatex is a D-Bus service that implements the org.freedesktop.timedate1
interface. It can be used to read and set the system clock, the real-time clock
(RTC), the system timezone, and enable or disable an NTP client installed on
the system. It is a replacement for the systemd-timedated service.

%prep
%setup -q
%patch1 -p1 -b .timeout

%build
make %{?_smp_mflags} \
	CFLAGS="$RPM_OPT_FLAGS" \
	EXTRA_LDFLAGS="%{__global_ldflags}"

%install
%makeinstall unitdir=%{?buildroot:%{buildroot}}%{_unitdir}

# mask systemd-timedated service (#1244023)
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system
ln -s /dev/null %{buildroot}%{_sysconfdir}/systemd/system/systemd-timedated.service

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc COPYING NEWS README
%{_sysconfdir}/systemd/system/systemd-timedated.service
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8*
%{_unitdir}/%{name}.service
%dir %{_prefix}/lib/systemd/ntp-units.d

%changelog
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 10 2018 Miroslav Lichvar <mlichvar@redhat.com> 0.5-2
- avoid getting stuck in infinite loop with new glib2 (#1450628)

* Tue Nov 07 2017 Miroslav Lichvar <mlichvar@redhat.com> 0.5-1
- update to 0.5

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Miroslav Lichvar <mlichvar@redhat.com> 0.4-1
- update to 0.4 (#1279760)

* Fri Jul 24 2015 Miroslav Lichvar <mlichvar@redhat.com> 0.3-3
- mask systemd-timedated service (#1244023)
- rely on systemd preset in post scriptlet

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Miroslav Lichvar <mlichvar@redhat.com> 0.3-1
- update to 0.3 (#1190377)

* Wed Jan 21 2015 Miroslav Lichvar <mlichvar@redhat.com> 0.2-1
- update to 0.2

* Wed Nov 19 2014 Miroslav Lichvar <mlichvar@redhat.com> 0.1-1
- initial release
