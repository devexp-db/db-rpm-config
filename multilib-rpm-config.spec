# While we are in package playing with packaging principles, why about having
# this solved in redhat-rpm-config too?  (Also for RHELs which are alive, or
# EPELs otherwise).
%{!?_licensedir:%global license %doc}

# https://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_of_Additional_RPM_Macros
%global macrosdir       %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

%global rrcdir          %_libexecdir

%global macro_ns        multilib_
%global macrofn_ns      multilib-

Summary: Multilib packaging helpers
Name: multilib-rpm-config
Version: 1
Release: 3%{?dist}
License: GPLv2+
URL: https://fedoraproject.org/wiki/PackagingDrafts/MultilibTricks

Source0: multilib-fix
Source1: macros.ml
Source2: README
Source3: COPYING

BuildArch: noarch

# Most probably we want to move everything here?
Requires: redhat-rpm-config

%description
Set of tools (shell scripts, RPM macro files) to help with multilib packaging
issues.


%prep
%setup -c -T
install -m 644 %{SOURCE2} %{SOURCE3} .


%build
%global ml_fix %rrcdir/multilib-fix
sed -e 's|@ML_FIX@|%ml_fix|g' \
    %{SOURCE1} > macros.multilib


%install
mkdir -p %{buildroot}%{rrcdir}
mkdir -p %{buildroot}%{macrosdir}
install -m 644 -p macros.multilib %{buildroot}/%{macrosdir}
install -m 755 -p %{SOURCE0} %{buildroot}/%{ml_fix}


%files
%license COPYING
%doc README
%{rrcdir}/*
%{macrosdir}/*


%changelog
* Thu Jun 09 2016 Pavel Raiskup <praiskup@redhat.com> - 1-3
- package separately from redhat-rpm-config

* Fri Nov 27 2015 Pavel Raiskup <praiskup@redhat.com> - 1-2
- fix licensing in Sources
- allow undefined %%namespace

* Wed Nov 18 2015 Pavel Raiskup <praiskup@redhat.com> - 1-1
- initial packaging
