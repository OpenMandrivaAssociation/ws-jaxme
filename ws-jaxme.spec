%{?_javapackages_macros:%_javapackages_macros}
# Copyright (c) 2000-2005, JPackage Project
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

%global base_name jaxme

Name:           ws-jaxme
Version:        0.5.2
Release:        12.4
Epoch:          0
Summary:        Open source implementation of JAXB
Group:          Development/Java
License:        ASL 2.0
URL:            http://ws.apache.org/
# svn export http://svn.apache.org/repos/asf/webservices/archive/jaxme/tags/R0_5_2/ ws-jaxme-0.5.2
# tar czf ws-jaxme-0.5.2-src.tar.gz ws-jaxme-0.5.2
Source0:        ws-jaxme-0.5.2-src.tar.gz
Source1:        ws-jaxme-bind-MANIFEST.MF

Source2:        http://repo1.maven.org/maven2/org/apache/ws/jaxme/jaxme2/%{version}/jaxme2-%{version}.pom
Source3:        http://repo1.maven.org/maven2/org/apache/ws/jaxme/jaxme2-rt/%{version}/jaxme2-rt-%{version}.pom
Source4:        http://repo1.maven.org/maven2/org/apache/ws/jaxme/jaxmeapi/%{version}/jaxmeapi-%{version}.pom
Source5:        http://repo1.maven.org/maven2/org/apache/ws/jaxme/jaxmejs/%{version}/jaxmejs-%{version}.pom
Source6:        http://repo1.maven.org/maven2/org/apache/ws/jaxme/jaxmepm/%{version}/jaxmepm-%{version}.pom
Source7:        http://repo1.maven.org/maven2/org/apache/ws/jaxme/jaxmexs/%{version}/jaxmexs-%{version}.pom

Source100:	ws-jaxme.rpmlintrc

# generated docs with forrest-0.5.1
Patch0:         ws-jaxme-docs_xml.patch
Patch1:         ws-jaxme-catalog.patch
Patch2:         ws-jaxme-system-dtd.patch
Patch3:         ws-jaxme-jdk16.patch
Patch4:         ws-jaxme-ant-scripts.patch
Patch5:         ws-jaxme-use-commons-codec.patch
# Remove xmldb-api, deprecated since f17
Patch6:         ws-jaxme-remove-xmldb.patch
Patch7:         ws-jaxme-0.5.2-class-version15.patch
BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  java-devel >= 1.6.0
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-apache-resolver
BuildRequires:  antlr
BuildRequires:  apache-commons-codec
BuildRequires:  junit
BuildRequires:  hsqldb1
BuildRequires:  log4j12
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
BuildRequires:  docbook-style-xsl
BuildRequires:  docbook-dtds
BuildRequires:  zip
Requires:       antlr
Requires:       apache-commons-codec
Requires:       junit
Requires:       hsqldb1
Requires:       log4j12
Requires:       xalan-j2
Requires:       xerces-j2
Requires:       jpackage-utils

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

%description    javadoc
%{summary}.

%package        manual
Summary:        Documents for %{name}

%description    manual
%{summary}.

%prep
%setup -q
find . -name "*.jar" -print -delete

%patch0 -p0
%patch1 -p0
%patch2 -p1
DOCBOOKX_DTD=`%{_bindir}/xmlcatalog %{_datadir}/sgml/docbook/xmlcatalog "-//OASIS//DTD DocBook XML V4.5//EN" 2>/dev/null`
%{__perl} -pi -e 's|@DOCBOOKX_DTD@|$DOCBOOKX_DTD|' src/documentation/manual/jaxme2.xml
%patch3 -p1
%patch4 -p0 -b .sav
%patch5 -p0 -b .sav
%patch6 -p1
%patch7 -p1

sed -i 's/\r//' NOTICE

sed -i "s|log4j.jar|log4j12-1.2.17.jar|" ant/js.xml
sed -i "s|hsqldb.jar|hsqldb1-1.jar|" ant/js.xml ant/pm.xml

%build
export CLASSPATH=$(build-classpath antlr hsqldb1-1 commons-codec junit log4j12-1.2.17 xerces-j2 xalan-j2 xalan-j2-serializer)
ant all Docs.all \
-Dbuild.sysclasspath=first \
-Ddocbook.home=%{_datadir}/sgml/docbook \
-Ddocbookxsl.home=%{_datadir}/sgml/docbook/xsl-stylesheets

mkdir -p META-INF
cp -p %{SOURCE1} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u dist/jaxmeapi-%{version}.jar META-INF/MANIFEST.MF

%install

install -dm 755 $RPM_BUILD_ROOT%{_javadir}/%{base_name} $RPM_BUILD_ROOT%{_mavenpomdir}
for jar in jaxme2 jaxme2-rt jaxmeapi jaxmejs jaxmepm jaxmexs; do
   install -m 644 dist/${jar}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{base_name}/${jar}.jar
   install -pm 644 %{_sourcedir}/${jar}-%{version}.pom $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{base_name}-${jar}.pom
   %add_maven_depmap JPP.%{base_name}-${jar}.pom %{base_name}/${jar}.jar
  (
    cd $RPM_BUILD_ROOT%{_javadir}/%{base_name} &&
    ln -sf ${jar}.jar ws-${jar}.jar
  )
done

#javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/docs/src/documentation/content/apidocs \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf build/docs/src/documentation/content/apidocs

%files -f .mfiles
%doc LICENSE NOTICE
%{_javadir}/%{base_name}

%files javadoc
%doc LICENSE NOTICE
%doc %{_javadocdir}/%{name}

%files manual
%doc LICENSE NOTICE
%doc build/docs/src/documentation/content/manual

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.5.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:0.5.2-11
- Use .mfiles generated during build

* Thu Sep 05 2013 gil cattaneo <puntogil@libero.it> - 0:0.5.2-10
- minor changes to update to current packaging guidelines
- added maven poms (rhbz#903694)
- stop hardcoding docdir (rhbz#993889)
- fix some rpmlint problems

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.5.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar  5 2013 Hans de Goede <hdegoede@redhat.com> - 0:0.5.2-8
- Fix FTBFS (add xalan-j2-serializer to classpath) (rhbz#914580)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 23 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:0.5.2-6
- Add LICENSE and NOTICE files too all (sub)packages

* Fri Jul 27 2012 Hans de Goede <hdegoede@redhat.com> - 0:0.5.2-5
- Build all class files in 1.5 format (rhbz#842624)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 6 2012 Alexander Kurtakov <akurtako@redhat.com> 0:0.5.2-3
- Fix the dependencies.

* Fri Apr 6 2012 Alexander Kurtakov <akurtako@redhat.com> 0:0.5.2-2
- Guideline fixes.

* Wed Feb 8 2012 Roland Grunberg <rgrunber@redhat.com> 0:0.5.2-1
- Update to 0.5.2.
- Remove xmldb-api due to deprecation.
- Fix ws-jaxme-ant-scripts.patch to apply cleanly.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Alexander Kurtakov <akurtako@redhat.com> 0:0.5.1-6
- Fix ant-nodeps in the classpath.

* Tue Dec 21 2010 Alexander Kurtakov <akurtako@redhat.com> 0:0.5.1-5
- Fix FTBFS.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.5.1-4.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.5.1-3.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 22 2008 Alexander Kurtakov <akurtako@redhat.com> - 0:0.5.1-2.3
- BR docbook-style-xsl.
- BR ant-apache-resolver.

* Wed Oct 22 2008 Alexander Kurtakov <akurtako@redhat.com> - 0:0.5.1-2.3
- Partial sync with jpackage to get build fixes.
- Add osgi manifest to jaxmeapi.jar.

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:0.5.1-2.2
- drop repotag
- fix license tag

* Mon Feb 12 2007 Deepak Bhole <dbhole@redhat.com> - 0:0.5.1-2jpp.1
- Update as per Fedora guidelines.

* Thu May 04 2006 Ralph Apel <r.apel at r-apel.de> - 0:0.5.1-1jpp
- First JPP-1.7 release

* Tue Dec 20 2005 Ralph Apel <r.apel at r-apel.de> - 0:0.5-1jpp
- Upgrade to 0.5

* Thu Sep 09 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.3.1-1jpp
- Fix version in changelog
- Upgrade to 0.3.1

* Mon Aug 30 2004 Ralph Apel <r.apel at r-apel.de> - 0:2.0-0.b1.4jpp
- Build with ant-1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:2.0-0.b1.3jpp
- Void change

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:2.0-0.b1.2jpp
- Upgrade to Ant 1.6.X

* Thu Mar 04 2004 Ralph Apel <r.apel at r-apel.de> - 0:2.0-0.b1.1jpp
- First JPackage release
