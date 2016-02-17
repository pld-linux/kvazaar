Summary:	Kvazaar - open-source HEVC encoder
Summary(pl.UTF-8):	Kvazaar - koder HEVC o otwartych źródłach
Name:		kvazaar
Version:	0.8.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://github.com/ultravideo/kvazaar/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9c614d753dc055dcbb343546d3cd4048
URL:		https://github.com/ultravideo/kvazaar
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%ifarch %{ix86} %{x8664} x32
BuildRequires:	yasm
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kvazaar is an open-source HEVC encoder licensed under LGPL v2.1.

%description -l pl.UTF-8
Kvazaar to mający otwarte źródła koder HEVC, wydany na licencji LGPL
v2.1.

%package devel
Summary:	Header files for Kvazaar library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Kvazaar
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Kvazaar library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Kvazaar.

%package static
Summary:	Static Kvazaar library
Summary(pl.UTF-8):	Statyczna biblioteka Kvazaar
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Kvazaar library.

%description static -l pl.UTF-8
Statyczna biblioteka Kvazaar.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING CREDITS README.md doc/syntax_elements.txt
%attr(755,root,root) %{_bindir}/kvazaar
%attr(755,root,root) %{_libdir}/libkvazaar.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkvazaar.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkvazaar.so
%{_includedir}/kvazaar.h
%{_includedir}/kvazaar_version.h
%{_pkgconfigdir}/kvazaar.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libkvazaar.a
