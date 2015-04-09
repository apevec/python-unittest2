# Created by pyp2rpm-1.1.1
%global pypi_name unittest2
%if 0%{?fedora}
%global with_python3 1
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           python-%{pypi_name}
Version:        1.0.1
Release:        1%{?dist}
Summary:        The new features in unittest backported to Python 2.4+

License:        BSD
URL:            http://pypi.python.org/pypi/unittest2
Source0:        https://pypi.python.org/packages/source/u/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Patch0:         unittest2-1.0.1-remove-argparse-from-requires.patch
BuildArch:      noarch

BuildRequires:  python2-devel
%if 0%{?rhel} == 6
BuildRequires:  python-argparse
Requires:       python-argparse
%endif
BuildRequires:  python-setuptools
BuildRequires:  python-six >= 1.4.0
BuildRequires:  python-traceback2
Requires:       python-setuptools
Requires:       python-six >= 1.4.0
Requires:       python-traceback2

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six >= 1.4.0
BuildRequires:  python3-traceback2
%endif # if with_python3


%description
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7 and onwards. It is tested to run on Python 2.6, 2.7,
3.2, 3.3, 3.4 and pypy.

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        The new features in unittest backported to Python 2.4+
Requires:       python3-setuptools
Requires:       python3-six >= 1.4.0
Requires:       python3-traceback2

%description -n python3-%{pypi_name}
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7 and onwards. It is tested to run on Python 2.6, 2.7,
3.2, 3.3, 3.4 and pypy.
%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%patch0 -p1

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3


%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/unit2 %{buildroot}/%{_bindir}/python3-unit2
popd
%endif # with_python3

%{__python2} setup.py install --skip-build --root %{buildroot}


%check
%{__python2} -m unittest2.__main__

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} -m unittest2
popd
%endif # with_python3


%files
%doc README.txt
%{_bindir}/unit2
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.txt
%{_bindir}/python3-unit2
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with_python3

%changelog
* Fri Nov 14 2014 Slavek Kabrda <bkabrda@redhat.com> - 0.8.0-2
- Bump to avoid collision with previously blocked 0.8.0-1

* Mon Nov 10 2014 Slavek Kabrda <bkabrda@redhat.com> - 0.8.0-1
- Unretire the package, create a fresh specfile
