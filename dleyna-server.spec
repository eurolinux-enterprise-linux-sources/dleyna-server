%global api 1.0
%global commit 3fcae066b44195c187b5611acfd511b9a87850d0
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           dleyna-server
Version:        0.4.0
Release:        1%{?dist}
Summary:        Service for interacting with Digital Media Servers

License:        LGPLv2
URL:            https://01.org/dleyna/

Source0:        https://github.com/01org/%{name}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

BuildRequires:  autoconf automake libtool
BuildRequires:  dleyna-core-devel
BuildRequires:  glib2-devel >= 2.28
BuildRequires:  gssdp-devel >= 0.13.2
BuildRequires:  gupnp-devel >= 0.20.3
BuildRequires:  gupnp-av-devel >= 0.11.5
BuildRequires:  gupnp-dlna-devel >= 0.9.4
BuildRequires:  libsoup-devel
BuildRequires:  pkgconfig
Requires:       dbus
Requires:       dleyna-connector-dbus

# https://github.com/01org/dleyna-server/issues/145
Patch0:         0001-Device-Fix-ChildCount-property-type.patch

%description
D-Bus service for clients to discover and manipulate DLNA Digital Media
Servers (DMSes).


%prep
%setup -qn %{name}-%{commit}
%patch0 -p1

%build
autoreconf -fiv
%configure \
  --disable-silent-rules \
  --disable-static

# Omit unused direct shared library dependencies.
sed --in-place --expression 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
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
* Tue Jun 02 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.4.0-1
- Initial RHEL import
Resolves: #1219532
