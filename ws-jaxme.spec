# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define base_name jaxme
%define gcj_support 0

Name:           ws-jaxme
Version:        0.5.2
Release:        1.0.8
Epoch:          0
Summary:        Open source implementation of JAXB

Group:          Development/Java
License:        Apache License
URL:            http://ws.apache.org/jaxme/
Source0:        ws-jaxme-0.5.2-src.tar.gz
# svn export https://svn.apache.org/repos/asf/webservices/jaxme/tags/R0_5_2/ ws-jaxme-0.5.2
Source1:        ws-jaxme-bind-MANIFEST.MF
Patch0:         ws-jaxme-docs_xml.patch
Patch1:         ws-jaxme-catalog.patch
Patch2:         ws-jaxme-system-dtd.patch
Patch3:         ws-jaxme-jdk16.patch
Patch4:         ws-jaxme-ant-scripts2.patch
Patch5:         ws-jaxme-use-commons-codec.patch
Patch6:         ws-jaxme-fix_docbook.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-trax >= 0:1.6
BuildRequires:  ant-apache-resolver
BuildRequires:  antlr
BuildRequires:  jaxp_transform_impl
BuildRequires:  jakarta-commons-codec
BuildRequires:  junit
BuildRequires:  hsqldb
BuildRequires:  log4j
BuildRequires:  xalan-j2
BuildRequires:  xmldb-api
BuildRequires:  xmldb-api-sdk
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-jaxp-1.3-apis
BuildRequires:  libxml2-utils
BuildRequires:  docbook-style-xsl
BuildRequires:  docbook-dtd45-xml
BuildRequires:  zip
Requires:       antlr
Requires:       jaxp_transform_impl
Requires:       jakarta-commons-codec
Requires:       junit
Requires:       hsqldb
Requires:       log4j
Requires:       xalan-j2
Requires:       xmldb-api
Requires:       xmldb-api-sdk
Requires:       xerces-j2
Requires:       xml-commons-jaxp-1.3-apis
Requires:       jpackage-utils
Requires(postun): jpackage-utils

%description
A Java/XML binding compiler takes as input a schema
description (in most cases an XML schema, but it may
be a DTD, a RelaxNG schema, a Java class inspected
via reflection, or a database schema). The output is
a set of Java classes:
* A Java bean class matching the schema description.
  (If the schema was obtained via Java reflection,
  the original Java bean class.)
* Read a conforming XML document and convert it into
  the equivalent Java bean.
* Vice versa, marshal the Java bean back into the
  original XML document.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       jpackage-utils
Requires(postun): jpackage-utils

%description    javadoc
%{summary}.

%package        manual
Summary:        Documents for %{name}
Group:          Development/Java

%description    manual
%{summary}.

%prep
%setup -q -n %{name}-%{version}
for j in $(find . -name "*.jar"); do
    mv $j $j.no
done

%patch0 -p0
%patch1 -p0
#%patch2 -p1
%patch3 -p1
%patch4 -p0 -b .sav
%patch5 -p0 -b .sav
%patch6 -p0 -b .docbook

%build
export OPT_JAR_LIST="xalan-j2 ant/ant-trax xalan-j2-serializer xml-commons-resolver ant/ant-apache-resolver"
export CLASSPATH=$(build-classpath antlr hsqldb commons-codec junit log4j xmldb-api xerces-j2 xml-commons-jaxp-1.3-apis)
%{ant} all Docs.all \
-Dbuild.sysclasspath=first \
-Ddocbook.home=%{_datadir}/sgml/docbook \
-Ddocbookxsl.home=%{_datadir}/sgml/docbook/xsl-stylesheets

mkdir -p META-INF
cp -p %{SOURCE1} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u dist/jaxmeapi-%{version}.jar META-INF/MANIFEST.MF

%install
rm -rf $RPM_BUILD_ROOT
install -dm 755 $RPM_BUILD_ROOT%{_javadir}/%{base_name}
for jar in dist/*.jar; do
   install -m 644 ${jar} $RPM_BUILD_ROOT%{_javadir}/%{base_name}/
done
(cd $RPM_BUILD_ROOT%{_javadir}/%{base_name} &&
    for jar in *-%{version}*;
        do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`;
    done
)

(cd $RPM_BUILD_ROOT%{_javadir}/%{base_name} &&
    for jar in *.jar;
        do ln -sf ${jar} ws-${jar};
    done
)

#javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/src/documentation/content/apidocs \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf build/docs/src/documentation/content/apidocs

#manual
install -dm 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr build/docs/src/documentation/content/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -pm 644 LICENSE $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%post
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/%{base_name}
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}


%changelog
* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0:0.5.2-1.0.6mdv2011.0
+ Revision: 608173
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:0.5.2-1.0.5mdv2010.1
+ Revision: 524356
- rebuilt for 2010.1

* Thu Jan 15 2009 Jérôme Soyer <saispo@mandriva.org> 0:0.5.2-1.0.4mdv2009.1
+ Revision: 329687
- Remove patch2 and add patch6 to fix dtd
- Add zip to BR
- Add BR
- Add BR
- Add libxml2-utils BR
- Bump Release
- Fix Build

* Mon Jan 05 2009 Jérôme Soyer <saispo@mandriva.org> 0:0.5.2-1.0.3mdv2009.1
+ Revision: 325046
- Add some patches and rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Wed Dec 12 2007 Alexander Kurtakov <akurtakov@mandriva.org> 0:0.5.2-1.0.1mdv2008.1
+ Revision: 117861
- new version 0.5.2 with maven poms (jpp sync)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:0.5.1-2.1.3mdv2008.0
+ Revision: 87265
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Wed Jul 18 2007 Anssi Hannula <anssi@mandriva.org> 0:0.5.1-2.1.2mdv2008.0
+ Revision: 53213
- use xml-commons-jaxp-1.3-apis explicitely instead of the generic
  xml-commons-apis which is provided by multiple packages (see bug #31473)

* Tue Jul 03 2007 David Walluck <walluck@mandriva.org> 0:0.5.1-2.1.1mdv2008.0
+ Revision: 47659
- Import ws-jaxme



* Mon Feb 12 2007 Deepak Bhole <dbhole@redhat.com> - 0:0.5.1-2jpp.1
- Update as per Fedora guidelines.

* Wed May 04 2006 Ralph Apel <r.apel at r-apel.de> - 0:0.5.1-1jpp
- First JPP-1.7 release

* Tue Dec 20 2005 Ralph Apel <r.apel at r-apel.de> - 0:0.5-1jpp
- Upgrade to 0.5

* Thu Sep 09 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.3.1-1jpp
- Fix version in changelog
- Upgrade to 0.3.1

* Fri Aug 30 2004 Ralph Apel <r.apel at r-apel.de> - 0:2.0-0.b1.4jpp
- Build with ant-1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:2.0-0.b1.3jpp
- Void change

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:2.0-0.b1.2jpp
- Upgrade to Ant 1.6.X

* Fri Mar 04 2004 Ralph Apel <r.apel at r-apel.de> - 0:2.0-0.b1.1jpp
- First JPackage release
