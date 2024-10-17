%define modname tdb
%define soname %{modname}.so
%define inifile A77_%{modname}.ini

Summary:	Trivial DB bindings
Name:		php-%{modname}
Version:	1.0.0
Release:	22
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/tdb/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Patch0:		tdb-1.0.0-php54x.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	file
BuildRequires:	tdb-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This extension provides bindings for Trivial DB.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%patch0 -p0

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# lib64 fix
perl -p -i -e "s|/lib\b|/%{_lib}|g" *.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_libdir}/php/extensions

install -m0755 modules/%{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}

[%{modname}]
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml CREDITS README tests
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-21mdv2012.0
+ Revision: 796993
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-20
+ Revision: 761335
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-19
+ Revision: 696480
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-18
+ Revision: 695475
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-17
+ Revision: 646694
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-16mdv2011.0
+ Revision: 629885
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-15mdv2011.0
+ Revision: 628199
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-14mdv2011.0
+ Revision: 600540
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-13mdv2011.0
+ Revision: 588877
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-12mdv2010.1
+ Revision: 514680
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-11mdv2010.1
+ Revision: 485492
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-10mdv2010.1
+ Revision: 468263
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-9mdv2010.0
+ Revision: 451365
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1.0.0-8mdv2010.0
+ Revision: 397619
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-7mdv2010.0
+ Revision: 377035
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-6mdv2009.1
+ Revision: 346665
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-5mdv2009.1
+ Revision: 341829
- rebuilt against php-5.2.9RC2

* Sun Jan 04 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-4mdv2009.1
+ Revision: 324858
- rebuild
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2mdv2009.0
+ Revision: 238440
- rebuild

* Sun Apr 20 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1mdv2009.0
+ Revision: 195868
- import php-tdb


* Sun Apr 20 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1mdv2009.0
- initial Mandriva package
