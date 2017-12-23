#
# Conditional build:
%bcond_without	cryptopp	# selective encryption using crypto++

Summary:	Kvazaar - open-source HEVC encoder
Summary(pl.UTF-8):	Kvazaar - koder HEVC o otwartych źródłach
Name:		kvazaar
Version:	1.2.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/ultravideo/kvazaar/releases
Source0:	https://github.com/ultravideo/kvazaar/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	829c4d94517047e09110f341c29603cb
Patch0:		x32.patch
Patch1:		%{name}-link.patch
URL:		https://github.com/ultravideo/kvazaar
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
%{?with_cryptopp:BuildRequires:	cryptopp-devel}
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%ifarch %{ix86} %{x8664} x32
BuildRequires:	yasm
%endif
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kvazaar is an open-source HEVC encoder licensed under LGPL v2.1.

%description -l pl.UTF-8
Kvazaar to mający otwarte źródła koder HEVC, wydany na licencji LGPL
v2.1.

%package libs
Summary:	Kvazaar library
Summary(pl.UTF-8):	Biblioteka Kvazaar
Group:		Libraries
Conflicts:	kvazaar < 0.8.2-3

%description libs
Kvazaar library.

%description libs -l pl.UTF-8
Biblioteka Kvazaar.

%package devel
Summary:	Header files for Kvazaar library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Kvazaar
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

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
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_cryptopp:--with-cryptopp}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libkvazaar.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/kvazaar

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING CREDITS README.md doc/syntax_elements.txt
%attr(755,root,root) %{_bindir}/kvazaar
%{_mandir}/man1/kvazaar.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkvazaar.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkvazaar.so.4

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkvazaar.so
%{_includedir}/kvazaar.h
%{_pkgconfigdir}/kvazaar.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libkvazaar.a
