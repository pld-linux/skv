# TODO: use system *tex todonotes package (newer texlive?)
#
# Conditional build:
%bcond_without	apidocs		# LaTeX documentation
%bcond_with	ibverbs		# use ibverbs (OFED) instead of sockets for communication
%bcond_with	rocksdb		# use rocksdb as database backend
#
Summary:	Scalable Key/Value Store
Summary(pl.UTF-8):	Scalable Key/Value Store - skalowalna baza klucz-wartość
Name:		skv
Version:	0.1.0
%define	snap	20141120
%define	gitrev	14cbb85
Release:	0.%{snap}.1
License:	Eclipse Public License v1.0
Group:		Daemons
Source0:	https://github.com/Scalable-Key-Value/code/archive/%{gitrev}/%{name}-%{gitrev}.tar.gz
# Source0-md5:	0ea9908ad80ae270238b65eca95da019
Source1:	https://github.com/Eyescale/CMake/archive/c13f465/Eyescale-CMake-c13f465.tar.gz
# Source1-md5:	71df45dad1b0c62d6039655fe898ea26
# generated from ftp://ftp.ctan.org/pub/tex/macros/latex2e/contrib/todonotes/
Source2:	todonotes.sty
Patch0:		%{name}-link.patch
URL:		https://github.com/Scalable-Key-Value
%{?with_rocksdb:BuildRequires:	bzip2-devel}
BuildRequires:	cmake >= 2.8
%{?with_ibverbs:BuildRequires:	librdmacm-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	mpi-devel
%{?with_rocksdb:BuildRequires:	rocksdb-devel}
%{?with_apidocs:BuildRequires:	texlive-format-pdflatex}
%{?with_apidocs:BuildRequires:	texlive-latex-pgf}
%{?with_apidocs:BuildRequires:	texlive-tex-xkeyval}
%{?with_rocksdb:BuildRequires:	zlib-devel}
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SKV (Scalable Key-Value Store) is a parallel client, parallel server,
key-value database system with basic function similar to BDB. SKV
storage can be drawn from main memory of the node of the parallel
machine or from a single-node key/value store that serves as a storage
back-end for the distributed SKV.

%description -l pl.UTF-8
SKV (Scalable Key-Value Store - skalowalna baza klucz-wartość) to
system baz danych klucz-wartość z równoległym klientem i równoległym
serwerem o funkcjonalności zbliżonej do BDB. Dane SKV można pobierać z
pamięci głównej węzła maszyny równoległej lub z danych klucz-wartość
pojedynczego węzła, służących jako backend dla rozproszonego SKV.

%package libs
Summary:	Shared SKV libraries
Summary(pl.UTF-8):	Biblioteki współdzielone SKV
Group:		Libraries

%description libs
Shared SKV libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone SKV.

%package devel
Summary:	Header files for SKV library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SKV
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for SKV library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SKV.

%package apidocs
Summary:	SKV API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki SKV
Group:		Documentation

%description apidocs
API documentation for SKV library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki SKV.

%prep
%setup -q -a1 -n code-14cbb85f056ae8eecb6936f1613233940dbf7963
%patch0 -p1

%{__mv} CMake-* CMake/common
%{__rm} .gitexternals

cp -p %{SOURCE2} doc/todonotes.sty

%build
install -d build
cd build
%cmake .. \
	-DBUILDYARD_DISABLED=ON \
	-DCOMMON_LIBRARY_TYPE=SHARED \
	%{?with_ibverbs:-DSKV_COMM_API_TYPE=verbs} \
%ifarch %{ix86} %{x8664}
	-DSKV_ENV=x86 \
%endif
%ifarch ppc ppc64
	-DSKV_ENV=BGAS \
%endif
	%{?with_rocksdb:-DSKV_LOCAL_KV_BACKEND=rocksdb}

%{__make}
cd ..

%if %{with apidocs}
%{__make} -C doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_prefix}/etc $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE.txt README
%attr(755,root,root) %{_bindir}/SKVServer
%attr(755,root,root) %{_bindir}/skv_base_test
%attr(755,root,root) %{_bindir}/skv_bench
%attr(755,root,root) %{_bindir}/skv_test_bulk
%attr(755,root,root) %{_bindir}/skv_test_insert_retrieve_async
%attr(755,root,root) %{_bindir}/skv_test_insert_retrieve_sync
%attr(755,root,root) %{_bindir}/test_skv_insert_command
%attr(755,root,root) %{_bindir}/test_skv_remove_command
%attr(755,root,root) %{_libdir}/libfxlogger.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfxlogger.so.1
%attr(755,root,root) %{_libdir}/libit_api.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libit_api.so.1
%attr(755,root,root) %{_libdir}/libskv_client.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libskv_client.so.1
%attr(755,root,root) %{_libdir}/libskv_client_mpi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libskv_client_mpi.so.1
%attr(755,root,root) %{_libdir}/libskv_common.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libskv_common.so.1
%attr(755,root,root) %{_libdir}/libskvc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libskvc.so.1
%attr(755,root,root) %{_libdir}/libskvc_mpi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libskvc_mpi.so.1
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/skv_server.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfxlogger.so
%attr(755,root,root) %{_libdir}/libit_api.so
%attr(755,root,root) %{_libdir}/libskv_client.so
%attr(755,root,root) %{_libdir}/libskv_client_mpi.so
%attr(755,root,root) %{_libdir}/libskv_common.so
%attr(755,root,root) %{_libdir}/libskvc.so
%attr(755,root,root) %{_libdir}/libskvc_mpi.so
%{_includedir}/skv
%{_pkgconfigdir}/skv.pc
%dir %{_datadir}/skv
%{_datadir}/skv/CMake

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/skvdoc.pdf
%endif
