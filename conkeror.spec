Summary:	Conkeror Web Browser Conquers Small Screens
Name:		conkeror
Version:	0.9
Release:	0.2
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications
# http://repo.or.cz/w/conkeror.git?a=snapshot;h=master;sf=tgz
Source0:	%{name}.tgz
# Source0-md5:	9e00720680f9cbdd0a98bbd20b9a8d95
Requires:	xulrunner >= 1.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/%{name}

%description
Conkeror is a keyboard-oriented, highly-customizable,
highly-extensible web browser based on Mozilla XULRunner, written
mainly in JavaScript, and inspired by exceptional software such as
Emacs and vi.

Conkeror features a sophisticated keyboard system, allowing users to
run commands and interact with content in powerful and novel ways. It
is self-documenting, featuring a powerful interactive help system.

%prep
%setup -q -n %{name}

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_appdir},%{_desktopdir}}

install	conkeror-spawn-helper $RPM_BUILD_ROOT%{_bindir}
cp -a branding chrome components content contrib defaults  \
   locale modules search-engines help style         \
$RPM_BUILD_ROOT%{_appdir}

# Add generated Build ID and PLD Linux to version output
sed -e 's/BuildID=git/BuildID=${BUILDID}/;s/^Version=\(.*\)$$/Version=\1 (PLD Linux)/' application.ini \
> $RPM_BUILD_ROOT%{_appdir}/application.ini
# Use PLD Linux version for M-x version output
sed -e 's/\$$CONKEROR_VERSION\$$/${UPSTREAM_VERSION} (Debian-${DEBIAN_VERSION})/' components/application.js \
> $RPM_BUILD_ROOT%{_appdir}/components/application.js
cat <<'EOF' > $RPM_BUILD_ROOT%{_bindir}/%{name}
#!/bin/sh
exec %{_bindir}/xulrunner %{_appdir}/application.ini
EOF
cp -a debian/conkeror.desktop $RPM_BUILD_ROOT%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/conkeror-spawn-helper
%dir %{_appdir}
%{_appdir}/application.ini
%{_appdir}/branding
%{_appdir}/chrome
%{_appdir}/components
%{_appdir}/content
%{_appdir}/contrib
%{_appdir}/defaults
%{_appdir}/help
%{_appdir}/modules
%{_appdir}/search-engines
%{_appdir}/style
%{_desktopdir}/conkeror.desktop

%dir %{_appdir}/locale
%{_appdir}/locale/en-US
%lang(sv) %{_appdir}/locale/sv-SE
