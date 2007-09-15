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

%define base_name jaxme
%define gcj_support 1

Name:           ws-jaxme
Version:        0.5.1
Release:        %mkrel 2.1.3
Epoch:          0
Summary:        Open source implementation of JAXB

Group:          Development/Java
License:        Apache License
URL:            http://ws.apache.org/jaxme/
# svn export http://svn.apache.org/repos/asf/webservices/jaxme/tags/R0_5_1/ ws-jaxme-0.5.1
# tar czf ws-jaxme-0.5.1-src.tar.gz ws-jaxme
Source0:        ws-jaxme-0.5.1-src.tar.gz
Source1:        ws-jaxme-0.5-docs.tar.gz
# generated docs with forrest-0.5.1
Patch0:         ws-jaxme-ant-scripts.patch
Patch1:         ws-jaxme-0.5.1-create_sql.patch
Patch2:         ws-jaxme-use-commons-codec.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-trax >= 0:1.6
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
mkdir -p build/docs/build/site
pushd build/docs/build/site
tar xzf %{SOURCE1}
popd

%patch0 -b .sav
%patch1 -b .sav
%patch2 -b .sav

%build
build-jar-repository -s -p prerequisites \
ant \
antlr \
commons-codec \
junit \
log4j \
servletapi5 \
xerces-j2 \
xml-commons-jaxp-1.3-apis \
xmldb-api \
xmldb-api-sdk \
hsqldb \

%{ant} all javadoc

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
rm -rf build/docs/build/site/apidocs

#manual
install -dm 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr build/docs/build/site/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -pm 644 LICENSE $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/LICENSE
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
