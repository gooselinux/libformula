# Use rpmbuild --without gcj to disable native bits
%define with_gcj %{!?_without_gcj:1}%{?_without_gcj:0}

Name: libformula
Version: 0.2.0
Release: 3.OOo31.1%{?dist}
Summary: Formula Parser
License: LGPLv2+
Group: System Environment/Libraries
Source: http://downloads.sourceforge.net/jfreereport/%{name}-%{version}-OOo31.zip
URL: http://reporting.pentaho.org/
BuildRequires: ant, java-devel, jpackage-utils, libbase >= 1.0.0
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: java, jpackage-utils, jakarta-commons-logging, libbase >= 1.0.0
%if %{with_gcj}
BuildRequires: java-gcj-compat-devel >= 1.0.31
Requires(post): java-gcj-compat >= 1.0.31
Requires(postun): java-gcj-compat >= 1.0.31
%else
BuildArch: noarch
%endif

%description
LibFormula provides Excel-Style-Expressions. The implementation provided
here is very generic and can be used in any application that needs to
compute formulas.

%package javadoc
Summary: Javadoc for %{name}
Group: Development/Documentation
Requires: %{name} = %{version}-%{release}
Requires: jpackage-utils
%if %{with_gcj}
BuildArch: noarch
%endif

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -c
find . -name "*.jar" -exec rm -f {} \;
mkdir -p lib
build-jar-repository -s -p lib commons-logging-api libbase

%build
ant jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp build/api $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%if %{with_gcj}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %{with_gcj}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun
%if %{with_gcj}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%doc licence-LGPL.txt README.txt ChangeLog.txt
%{_javadir}/*.jar
%if %{with_gcj}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.2.0-3.OOo31.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Caolan McNamara <caolanm@redhat.com> 0.2.0-3.OOo31
- make javadoc no-arch when building as arch-dependant aot

* Mon Mar 16 2009 Caolan McNamara <caolanm@redhat.com> 0.2.0-2.OOo31
- post-release tuned for OpenOffice.org report-designer

* Mon Mar 09 2009 Caolan McNamara <caolanm@redhat.com> 0.2.0-1
- latest version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 07 2008 Caolan McNamara <caolanm@redhat.com> 0.1.18-1
- initial fedora import
