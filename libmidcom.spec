Summary:	The MIDCOM SIMCO protocol and Timer library
Summary(pl):	Biblioteka protoko³u i zegara MIDCOM SIMCO
Name:		libmidcom
Version:	0.2.0
Release:	1
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.digium.com/pub/asterisk/releases/%{name}-%{version}.tar.gz
# Source0-md5:	dd3b1f4188dd17bc843f1e2d2dc3e1a9
URL:		http://www.ranchnetworks.com/
BuildRequires:	asterisk-devel
BuildRequires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The MIDCOM SIMCO protocol and Timer library.

%description -l pl
Biblioteka protoko³u i zegara MIDCOM SIMCO.

%package devel
Summary:	Header files for MIDCOM library
Summary(pl):	Pliki nag³ówkowe biblioteki MIDCOM
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for MIDCOM library.

%description devel -l pl
Pliki nag³ówkowe biblioteki MIDCOM.

%package static
Summary:	Static MIDCOM library
Summary(pl):	Statyczna biblioteka MIDCOM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MIDCOM library.

%description static -l pl
Statyczna biblioteka MIDCOM.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC -D_GNU_SOURCE=1"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_includedir}/midcom
install -d $RPM_BUILD_ROOT%{_includedir}/timer

install midcom/libmidcom.so.%{major}.0 $RPM_BUILD_ROOT%{_libdir}
ln -s libmidcom.so.%{major}.0 $RPM_BUILD_ROOT%{_libdir}/libmidcom.so.%{major}
ln -s libmidcom.so.%{major}.0 $RPM_BUILD_ROOT%{_libdir}/libmidcom.so
install midcom/libmidcom.a $RPM_BUILD_ROOT%{_libdir}
install midcom/simco_client.h $RPM_BUILD_ROOT%{_includedir}/midcom

install timer/libtimer.so.%{major}.0 $RPM_BUILD_ROOT%{_libdir}
ln -s libtimer.so.%{major}.0 $RPM_BUILD_ROOT%{_libdir}/libtimer.so.%{major}
ln -s libtimer.so.%{major}.0 $RPM_BUILD_ROOT%{_libdir}/libtimer.so
install timer/libtimer.a $RPM_BUILD_ROOT%{_libdir}
install timer/*.h $RPM_BUILD_ROOT%{_includedir}/timer

# fix headers
cd $RPM_BUILD_ROOT%{_includedir}/timer
for h in *.h; do
	%{__perl} -pi -e "s|\"$h\"|\<timer/$h\>|g" *.h
done
cd -

cd $RPM_BUILD_ROOT%{_includedir}/midcom
for h in *.h; do
	%{__perl} -pi -e "s|\"$h\"|\<midcom/$h\>|g" *.h
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmidcom.so.*.*
%attr(755,root,root) %{_libdir}/libtimer.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmidcom.so
%attr(755,root,root) %{_libdir}/libtimer.so
%{_includedir}/midcom
%{_includedir}/timer

%files static
%defattr(644,root,root,755)
%{_libdir}/libmidcom.a
%{_libdir}/libtimer.a
