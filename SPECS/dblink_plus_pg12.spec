# SPEC file for dblink_plus
# Copyright(C) 2019 NIPPON TELEGRAPH AND TELEPHONE CORPORATION

%define _pgdir   /usr/pgsql-12
%define _bindir  %{_pgdir}/bin
%define _libdir  %{_pgdir}/lib
%define _datadir %{_pgdir}/share/extension
%define _bcdir %{_libdir}/bitcode/dblink_plus
%define _bc_ind_dir %{_libdir}/bitcode

## Set general information
Summary:    PostgreSQL module to connect PostgreSQL/Oracle
Name:       dblink_plus
Version:    1.0.5
Release:    1%{?dist}
License:    BSD
Group:      Applications/Databases
Source0:    %{name}-%{version}.tar.gz
URL:        https://github.com/ossc-db/dblink_plus
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Vendor:     NIPPON TELEGRAPH AND TELEPHONE CORPORATION
#Following is needed to remove auto-discovery of oci library files(not under RPM package management)
AutoReqProv: no

## We use postgresql-devel package
BuildRequires:  postgresql12-devel
Requires:  postgresql12-libs

## Description
%description
dblink_plus is a PostgreSQL module which supports connections to other databases.
It is similar to contrib/dblink except that it can connect to Oracle, MySQL and sqlite3. 

Note that this package is available for only PostgreSQL 12.

%package llvmjit
Requires: postgresql12-server, postgresql12-llvmjit
Requires: dblink_plus = 1.0.5
Summary:  Just-in-time compilation support for dblink_plus

%description llvmjit
Just-in-time compilation support for dblink_plus 1.0.5

## prework
%prep
%setup -q -n %{name}-%{version}

## Set variables for build environment
%build
USE_PGXS=1 make %{?_smp_mflags} MYSQL=0 SQLITE3=0 ORACLE=0

## Set variables for install
%install
rm -rf %{buildroot}
USE_PGXS=1 make install MYSQL=0 SQLITE3=0 ORACLE=0 DESTDIR=%{buildroot}
install -m 644 COPYRIGHT %{buildroot}%{_datadir}/COPYRIGHT_dblink_plus

%clean
rm -rf %{buildroot}

%files
%defattr(0755,root,root)
%{_libdir}/dblink_plus.so
%defattr(0644,root,root)
%{_datadir}/dblink_plus.sql
%{_datadir}/dblink_plus--1.0.5.sql
%{_datadir}/dblink_plus.control
%{_datadir}/uninstall_dblink_plus.sql
%{_datadir}/COPYRIGHT_dblink_plus

%files llvmjit
%defattr(0644,root,root,0755)
%{_bcdir}
%defattr(0644,root,root)
%{_bc_ind_dir}/dblink_plus.index.bc

# History.
%changelog
* Mon Nov 25 2019 - NTT OSS Center <keisuke.kuroda.3862@gmail.com> 1.0.5-1
Support PG12.
* Tue Jan 22 2019 - NTT OSS Center <tatsuro.yamada@lab.ntt.co.jp> 1.0.4-1
Support PG11.
