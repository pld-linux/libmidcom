Summary:	The MIDCOM SIMCO protocol and Timer library
Name:		libmidcom
Version:	0.2.0
Release:	1
License:	GPL
Group:		Libraries
URL:		http://www.ranchnetworks.com/
Source0:	ftp://ftp.digium.com/pub/asterisk/releases/%{name}-%{version}.tar.gz
# Source0-md5:	dd3b1f4188dd17bc843f1e2d2dc3e1a9
BuildRequires:	asterisk-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The MIDCOM SIMCO protocol and Timer library

%package devel
Summary:	Static library and header files for the %{name} library
Group:		Development/Libraries
Provides:	%{name}-devel = %{version}

%description devel
The MIDCOM SIMCO protocol and Timer library

This package contains the static %{name} library and its header files.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{optflags} -fPIC -D_GNU_SOURCE=1"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_includedir}/midcom
install -d $RPM_BUILD_ROOT%{_includedir}/timer

install midcom/libmidcom.so.%{major}.0 $RPM_BUILD_ROOT%{_libdir}/
ln -s libmidcom.so.%{major}.0 $RPM_BUILD_ROOT%{_libdir}/libmidcom.so.%{major}
ln -s libmidcom.so.%{major} $RPM_BUILD_ROOT%{_libdir}/libmidcom.so
install midcom/libmidcom.a $RPM_BUILD_ROOT%{_libdir}/
install midcom/simco_client.h $RPM_BUILD_ROOT%{_includedir}/midcom/

install timer/libtimer.so.%{major}.0 $RPM_BUILD_ROOT%{_libdir}/
ln -s libtimer.so.%{major}.0 $RPM_BUILD_ROOT%{_libdir}/libtimer.so.%{major}
ln -s libtimer.so.%{major} $RPM_BUILD_ROOT%{_libdir}/libtimer.so
install timer/libtimer.a $RPM_BUILD_ROOT%{_libdir}/
install timer/*.h $RPM_BUILD_ROOT%{_includedir}/timer/

# fix headers
pushd $RPM_BUILD_ROOT%{_includedir}/timer
    for h in *.h; do
	perl -pi -e "s|\"$h\"|\<timer/$h\>|g" *.h
    done
popd

pushd $RPM_BUILD_ROOT%{_includedir}/midcom
    for h in *.h; do
	perl -pi -e "s|\"$h\"|\<midcom/$h\>|g" *.h
    done
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc gpl.txt
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/midcom/*
%{_includedir}/timer/*
%{_libdir}/*.so
%{_libdir}/*.a
