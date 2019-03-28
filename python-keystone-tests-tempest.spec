# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%global service keystone
%global plugin keystone-tempest-plugin
%global module keystone_tempest_plugin
%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
This package contains Tempest plugin for functional testing of keystone \
LDAP and federation features. Additionally it provides a plugin to \
automatically load these tests into Tempest.

Name:       python-%{service}-tests-tempest
Version:    0.2.0
Release:    1%{?dist}
Summary:    Tempest plugin for the keystone project.
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/

Source0:    http://tarballs.openstack.org/%{plugin}/%{module}-%{upstream_version}.tar.gz

BuildArch:  noarch
BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python%{pyver}-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python%{pyver}-%{service}-tests-tempest}
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools

Obsoletes: python-keystone-tests < 1:13.0.0

Requires:   python%{pyver}-tempest >= 1:18.0.0
Requires:   python%{pyver}-oslo-config >= 2:5.2.0
Requires:   python%{pyver}-six => 1.10.0
Requires:   python%{pyver}-testtools
Requires:   python%{pyver}-requests >= 2.14.2

# Handle python2 exception
%if %{pyver} == 2
Requires:   python-lxml
%else
Requires:   python%{pyver}-lxml
%endif

%description -n python%{pyver}-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python%{pyver}-%{service}-tests-tempest-doc
Summary:        python-%{service}-tests-tempest documentation
%{?python_provide:%python_provide python%{pyver}-%{service}-tests-tempest-doc}

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme

%description -n python%{pyver}-%{service}-tests-tempest-doc
It contains the documentation for the Keystone tempest tests.
%endif

%prep
%autosetup -n %{module}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-ingo
rm -rf %{module}.egg-info

%build
%{pyver_build}

# Generate Docs
%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%files -n python%{pyver}-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python%{pyver}-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Thu Mar 28 2019 RDO <dev@lists.rdoproject.org> 0.2.0-1
- Update to 0.2.0

