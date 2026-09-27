#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	python3		# Python 3 binding
%bcond_without	tests		# unit tests
#
Summary:	Library for managing RPM manifests
Summary(pl.UTF-8):	Biblioteka do zarządzania manifestami RPM
Name:		libpkgmanifest
Version:	0.6.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/rpm-software-management/libpkgmanifest/releases
Source0:	https://github.com/rpm-software-management/libpkgmanifest/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c9d4059966ca45836fea1459858170e1
URL:		https://github.com/rpm-software-management/libpkgmanifest
BuildRequires:	cmake >= 3.16
%if %{with tests}
BuildRequires:	gmock-devel
BuildRequires:	gtest-devel
%endif
BuildRequires:	libstdc++-devel >= 6:10.1
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	yaml-cpp-devel >= 0.7.0
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	swig-python >= 4.2.0
%endif
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	python3-breathe
BuildRequires:	python3-sphinx_autoapi
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library provides functionality for parsing and serializing RPM
package manifest files.

It is primarily designed for use by package managers like DNF which
populate information into manifest files. However, it can also be used
directly to interact with manifest objects in custom applications.

%description -l pl.UTF-8
Ta biblioteka udostępnia funkcjonalność analizy i serializacji plików
manifestów pakietów RPM.

Jest przeznaczona głównie do użycia w zarządcach plików, takich jak
DNF, wypełniających informacje w plikach manifestów. Może być jednak
używana także bezpośrednio przy obsłudze obiektów manifestów we
własnych aplikacjach.

%package devel
Summary:	Header files for libpkgmanifest library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libpkgmanifest
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	rpm-devel
Requires:	yaml-cpp-devel >= 0.7.0

%description devel
Header files for libpkgmanifest library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libpkgmanifest.

%package apidocs
Summary:	API documentation for libpkgmanifest library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libpkgmanifest
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libpkgmanifest library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libpkgmanifest.

%package -n python3-libpkgmanifest
Summary:	Python 3 bindings for libpkgmanifest library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki libpkgmanifest
Group:		Libraries/Python
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n python3-libpkgmanifest
Python 3 bindings for libpkgmanifest library.

%description -n python3-libpkgmanifest -l pl.UTF-8
Wiązania Pythona 3 do biblioteki libpkgmanifest.

%prep
%setup -q

# FIX: 0.6.0 release has broken VERSION.cmake
%{__sed} -i -e '/VERSION_MINOR/ s/5/6/' -e '/VERSION_PATCH/ s/10/0/' VERSION.cmake

%build
# .pc file generation requires relative CMAKE_INSTALL_LIBDIR
%cmake -B build \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	%{!?with_apidocs:-DWITH_DOCS=OFF} \
	%{!?with_python3:-DWITH_PYTHON=OFF} \
	%{!?with_tests:-DWITH_TESTS=OFF}

%{__make} -C build

%if %{with apidocs}
%{__make} -C build doc
%endif

%if %{with tests}
cd build
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python3}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.md README.md
%{_libdir}/libpkgmanifest.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libpkgmanifest.so
%{_includedir}/libpkgmanifest
%{_pkgconfigdir}/libpkgmanifest.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/docs/html/{_images,_static,api,design,*.html,*.js}
%endif

%if %{with python3}
%files -n python3-libpkgmanifest
%defattr(644,root,root,755)
%dir %{py3_sitedir}/libpkgmanifest
%{py3_sitedir}/libpkgmanifest/*.py
%{py3_sitedir}/libpkgmanifest/_*.so
%{py3_sitedir}/libpkgmanifest/__pycache__
%{py3_sitedir}/libpkgmanifest-%{version}.dist-info
%endif
