Summary:	Kvazaar - open-source HEVC encoder
Summary(pl.UTF-8):	Kvazaar - koder HEVC o otwartych źródłach
Name:		kvazaar
Version:	0.7.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://github.com/ultravideo/kvazaar/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8a77a9c30cd98e2aef01508bba55886d
Patch0:		%{name}-x32.patch
URL:		https://github.com/ultravideo/kvazaar
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
%patch0 -p1

%build
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} -C src \
	CC="%{__cc}" \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
%ifarch %{ix86} %{x8664} x32
	TARGET_CPU_ARCH=x86 \
%endif
%ifarch ppc ppc64
	TARGET_CPU_ARCH=ppc \
%endif
%ifarch arm
	TARGET_CPU_ARCH=ppc \
%endif
%ifarch %{ix86} ppc s390 sparc sparcv9
	TARGET_CPU_BITS=32 \
%endif
%ifarch %{x8664} s390x ppc64 sparc64
	TARGET_CPU_BITS=64 \
%endif
%ifarch x32
	TARGET_CPU_BITS=x32
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING CREDITS README.md doc/syntax_elements.txt
%attr(755,root,root) %{_bindir}/kvazaar
%attr(755,root,root) %{_libdir}/libkvazaar.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkvazaar.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkvazaar.so
%{_includedir}/kvazaar.h
%{_includedir}/kvazaar_version.h
%{_pkgconfigdir}/kvazaar.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libkvazaar.a
