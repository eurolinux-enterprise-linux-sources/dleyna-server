%global api 1.0

Name:           dleyna-server
Version:        0.5.0
Release:        2%{?dist}
Summary:        Service for interacting with Digital Media Servers

License:        LGPLv2
URL:            https://01.org/dleyna/
Source0:        https://01.org/dleyna/sites/default/files/downloads/%{name}-%{version}.tar.gz

BuildRequires:  autoconf automake libtool
BuildRequires:  pkgconfig(dleyna-core-1.0) >= 0.5.0
BuildRequires:  pkgconfig(gio-2.0) >= 2.28
BuildRequires:  pkgconfig(glib-2.0) >= 2.28
BuildRequires:  pkgconfig(gobject-2.0) >= 2.28
BuildRequires:  pkgconfig(gssdp-1.0) >= 0.13.2
BuildRequires:  pkgconfig(gupnp-1.0) >= 0.20.3
BuildRequires:  pkgconfig(gupnp-av-1.0) >= 0.11.5
BuildRequires:  pkgconfig(gupnp-dlna-2.0) >= 0.9.4
BuildRequires:  pkgconfig(libsoup-2.4) >= 2.28.2
Requires:       dbus
Requires:       dleyna-connector-dbus%{?_isa}

# https://github.com/01org/dleyna-server/issues/145
Patch0:         0001-Device-Fix-ChildCount-property-type.patch
# https://github.com/01org/dleyna-server/pull/151
Patch1:         0001-Fix-possible-use-after-free-on-exit.patch
# https://github.com/01org/dleyna-server/pull/159
Patch2:         0001-Include-libgupnp-gupnp-context-manager.h.patch

%description
D-Bus service for clients to discover and manipulate DLNA Digital Media
Servers (DMSes).


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
autoreconf -fiv
%configure \
  --disable-silent-rules \
  --disable-static

# Omit unused direct shared library dependencies.
sed --in-place --expression 's! -shared ! -Wl,--as-needed\0!g' libtool

%make_build


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -delete -print

# We don't need a -devel package because only the daemon is supposed to be
# using the library.
rm -rf $RPM_BUILD_ROOT/%{_includedir}
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/libdleyna-server-%{api}.so
rm -rf $RPM_BUILD_ROOT/%{_libdir}/pkgconfig


%files
%doc AUTHORS
%doc COPYING
%doc ChangeLog
%doc README
%{_datadir}/dbus-1/services/com.intel.%{name}.service

%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libdleyna-server-%{api}.so.*

%{_libexecdir}/%{name}-service
%config(noreplace) %{_sysconfdir}/%{name}-service.conf


%changelog
* Thu Oct 05 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.5.0-2
- Use arch-specific Requires on dleyna-connector-dbus
Resolves: #1479486

* Fri Mar 03 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0
Resolves: #1386847

* Tue Jun 02 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.4.0-1
- Initial RHEL import
Resolves: #1219532
