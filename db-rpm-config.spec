# https://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_of_Additional_RPM_Macros
%global macrosdir       %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

%global rrcdir          /usr/lib/rpm

%{!?namespace:%global namespace db}
%global macro_ns        %{?namespace:%{namespace}_}
%global script_ns       %{?namespace:%{namespace}-}
%global macrofn_ns      %{?namespace:%{namespace}-}
%global macrofn()       macros.%{?macrofn_ns}%1

Summary: More or less DB related rpm configuration files
Name: %{?script_ns}rpm-config
Version: 1
Release: 1%{?dist}
License: GPL+
Group: Development/System
URL: https://github.com/devexp-db/db-rpm-config

Source0: multilib-fix
Source1: macros.ml

BuildArch: noarch

# Most probably we want to have everything moved to this package!
Provides: redhat-rpm-config = %{version}-%{release}

%description
RPM configuration files used by DB team (but others might be interested too).

%prep
%setup -c -T

%build
%global ml_fix %rrcdir/%{?script_ns}multilib-fix
sed \
    -e 's|@ML_MACRO_PFX@|%{?macro_ns}|g' \
    -e 's|@ML_FIX@|%ml_fix|g' \
    %{SOURCE1} > %{macrofn ml}

%install
mkdir -p %{buildroot}%{rrcdir}
mkdir -p %{buildroot}%{macrosdir}
# Multi-lib kludge.
install -m 644 -p macros.%{?macrofn_ns}ml %{buildroot}/%{macrosdir}
install -m 755 -p %{SOURCE0} %{buildroot}/%{ml_fix}

%files
%{rrcdir}
%{macrosdir}

%changelog
* Wed Nov 18 2015 Pavel Raiskup <praiskup@redhat.com> - 1-1
- initial packaging
