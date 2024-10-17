#Module-Specific definitions
%define apache_version 2.2.8
%define mod_name mod_crowd
%define mod_conf B34_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache Basic Authentication Module written in c for Crowd
Name:		apache-%{mod_name}
Version:	1.0
Release:	%mkrel 9
Group:		System/Servers
License:	Public Domain
URL:		https://confluence.atlassian.com/display/CROWDEXT/Apache+Basic+Authentication+Module+written+in+c
Source0:	crowd_apache_module.zip
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	dos2unix
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
CROWD is a web-based single sign-on (SSO) tool for provisioning and identity
management developed by Atlassian. This module allows for Basic authentication
calls from apache over to CROWD SSO.

%prep

%setup -q -n crowd_apache_module

cp %{SOURCE1} %{mod_conf}

dos2unix README

%build
%{_sbindir}/apxs -c mod_crowd.c soapClient.c soapC.c stdsoap2.c

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

