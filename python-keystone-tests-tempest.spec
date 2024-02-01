%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x01527a34f0d0080f8a5db8d6eb6c5df21b4b6363
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
Version:    0.9.0
Release:    1%{?dist}
Summary:    Tempest plugin for the keystone project.
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/

Source0:    http://tarballs.openstack.org/%{plugin}/%{module}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{plugin}/%{module}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif
BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python3-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python3-%{service}-tests-tempest}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Obsoletes: python-keystone-tests < 1:13.0.0

Requires:   python3-tempest >= 1:18.0.0
Requires:   python3-oslo-config >= 2:5.2.0
Requires:   python3-six => 1.10.0
Requires:   python3-testtools
Requires:   python3-requests >= 2.14.2

Requires:   python3-lxml

%description -n python3-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python3-%{service}-tests-tempest-doc
Summary:        python-%{service}-tests-tempest documentation
%{?python_provide:%python_provide python3-%{service}-tests-tempest-doc}

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme

%description -n python3-%{service}-tests-tempest-doc
It contains the documentation for the Keystone tempest tests.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{module}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-ingo
rm -rf %{module}.egg-info

%build
%{py3_build}

# Generate Docs
%if 0%{?with_doc}
sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%files -n python3-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python3-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Fri Apr 01 2022 RDO <dev@lists.rdoproject.org> 0.9.0-1
- Update to 0.9.0


