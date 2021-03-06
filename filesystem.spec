%define		_enable_debug_packages	0
%define		__spec_clean_body	%{nil}

Summary:	Common directories
Name:		filesystem
Version:	201408
Release:	0.1
License:	GPL
Group:		Base
BuildRequires:	automake
Requires:	FHS
Requires:	setup
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# directory for "privilege separation" chroot
%define		_privsepdir	/usr/share/empty
# directory for *.idl files (for CORBA implementations)
%define		_idldir		/usr/share/idl

%define		no_install_post_strip	1
%define		_enable_debug_packages	0

%description
This package contains common directories for packages that extend
some programs functionality, but don't require them themselves.

%package debuginfo
Summary:	Common directories for debug information
Group:		Development/Debug
Requires:	%{name} = %{version}-%{release}

%description debuginfo
This package provides common directories for debug information.

%prep

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT/{run,sys} \
	$RPM_BUILD_ROOT/etc/{X11/xinit/xinitrc.d,X11/xorg.conf.d,certs,default,logrotate.d,pam.d,security,skel/tmp,sound,sysconfig/wmstyle,xdg/{autostart,menus}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{cron.d,cron.{hourly,daily,weekly,monthly},cron} \
	$RPM_BUILD_ROOT/home/{users,services} \
	$RPM_BUILD_ROOT/usr/lib/{firmware,security} \
	$RPM_BUILD_ROOT/usr/include/security \
	$RPM_BUILD_ROOT/usr/lib/{cgi-bin,debug,pkgconfig} \
	$RPM_BUILD_ROOT/var/lib/color/icc \
	$RPM_BUILD_ROOT/usr/share/{backgrounds,desktop-directories,{gnome,mate}/help,color/{icc,targets},man/man{n,l},man/pl/mann,pkgconfig,sounds/sf2,themes/Default,thumbnailers,wallpapers,{gnome,mate}/wm-properties,xsessions} \
	$RPM_BUILD_ROOT/usr/src/{debug,examples} \
	$RPM_BUILD_ROOT/var/lock/subsys \
	$RPM_BUILD_ROOT/var/log/archive \
	$RPM_BUILD_ROOT{%{_aclocaldir},%{_desktopdir}/{docklets,screensavers},%{_iconsdir},%{_pixmapsdir}/backgrounds,%{_datadir}/gtk-engines} \
	$RPM_BUILD_ROOT%{_fontsdir}/{{100,75}dpi,OTF,Speedo,Type1/{afm,pfm},TTF,cyrillic,local,misc} \
	$RPM_BUILD_ROOT{%{_idldir},%{_privsepdir}} \
	$RPM_BUILD_ROOT%{_libdir}/browser-plugins \
	$RPM_BUILD_ROOT%{_datadir}/gnome-2.0/ui

> %{name}.lang
install -d $RPM_BUILD_ROOT/usr/share/help/C

for lang in ar as ast bg bn_IN ca ca@valencia cs da de el en_GB es eu fa fi fr gl gu he hi hr hu id it ja kn ko lt lv mk ml mr nb nds nl oc pa pl ps pt pt_BR ro ru sl sr sr@latin sv ta te th tr uk vi zh_CN zh_HK zh_TW; do
	install -d $RPM_BUILD_ROOT/usr/share/help/${lang}
	echo "%%lang($lang) %dir /usr/share/help/${lang}" >> %{name}.lang
done

%if "%{_lib}" == "lib64"
install -d \
	$RPM_BUILD_ROOT/usr/lib64/{browser-plugins,cmake,mozilla/extensions,pkgconfig,security}
%endif

install -d \
	$RPM_BUILD_ROOT/usr/lib/debug/%{_lib} \
	$RPM_BUILD_ROOT/usr/lib/debug%{_libdir} \
	$RPM_BUILD_ROOT/usr/lib/debug/{bin,sbin} \
	$RPM_BUILD_ROOT/usr/lib/debug/usr/{bin,sbin} \
	$RPM_BUILD_ROOT/usr/lib/debug/lib/security \
	$RPM_BUILD_ROOT/usr/src/debug

%if "%{_lib}" == "lib64"
install -d \
	$RPM_BUILD_ROOT/usr/lib/debug/lib64/security
%endif

# create this for %clean
tar -cf checkfiles.tar -C $RPM_BUILD_ROOT .

%clean
mkdir -p $RPM_BUILD_ROOT
tar -xf checkfiles.tar -C $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT

check_filesystem_dirs() {
	RPMFILE=%{_rpmdir}/%{name}-%{version}-%{release}.%{_target_cpu}.rpm
	RPMFILE2=%{?with_debuginfo:%{_rpmdir}/%{name}-debuginfo-%{version}-%{release}.%{_target_cpu}.rpm}
	TMPFILE=$(mktemp)
	# note: we must exclude from check all existing dirs belonging to FHS
	find | sed -e 's|^\.||g' -e 's|^$||g' | LC_ALL=C sort | grep -v $TMPFILE | grep -E -v '^/(etc|etc/X11|home|lib|lib64|usr|usr/include|usr/lib|usr/lib64|usr/share|usr/share/man|usr/share/man/pl|usr/src|var|var/lib|var/lock|var/log)$' > $TMPFILE

	# find finds also '.', so use option -B for diff
	rpm -qpl $RPMFILE $RPMFILE2 | grep -v '^/$' | LC_ALL=C sort | diff -uB - $TMPFILE || :

	rm -f $TMPFILE
}

check_filesystem_dirs

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir /etc/X11/xinit
%dir /etc/X11/xinit/xinitrc.d
%dir /etc/X11/xorg.conf.d
%attr(751,root,root) %dir /etc/certs
%attr(750,root,root) %dir %{_sysconfdir}/default
%attr(751,root,root) %dir /etc/security
%attr(755,root,root) /etc/pam.d
%dir /etc/logrotate.d
%dir /etc/skel
%dir /etc/skel/tmp
%dir /etc/sound
%dir /etc/sysconfig
%dir /etc/sysconfig/wmstyle
%dir /etc/xdg
%dir /etc/xdg/autostart
%dir /etc/xdg/menus
%dir /home/users
%attr(751,root,adm) %dir /home/services
%dir /run
%dir /usr/lib/firmware
%dir /usr/lib/security
%dir /sys
%dir /usr/include/security
%dir /usr/lib/cgi-bin
%dir /usr/lib/pkgconfig
%dir /usr/share/backgrounds
%dir /usr/share/desktop-directories
%dir /usr/share/gnome
%dir /usr/share/gnome/help
%dir /usr/share/mate
%dir /usr/share/mate/help
%dir /usr/share/help
%dir /usr/share/help/C
%dir /usr/share/color
%dir /usr/share/color/icc
%dir /usr/share/color/targets
%dir /usr/share/man/man[nl]
%lang(pl) %dir /usr/share/man/pl/mann
%dir /usr/share/pkgconfig
%dir /usr/share/sounds
%dir /usr/share/sounds/sf2
%dir /usr/share/themes
%dir /usr/share/themes/Default
%dir /usr/share/thumbnailers
%dir /usr/share/wallpapers
%dir /usr/share/gnome/wm-properties
%dir /usr/share/xsessions
%dir /usr/src/examples
%dir /var/lib/color
%dir /var/lib/color/icc
%attr(700,root,root) %dir /var/lock/subsys
%attr(755,root,root) %dir /var/log/archive
%dir %{_aclocaldir}
%dir %{_datadir}/gtk-engines
%dir %{_desktopdir}
%dir %{_desktopdir}/docklets
%dir %{_desktopdir}/screensavers
%dir %{_iconsdir}
%dir %{_idldir}
%dir %{_pixmapsdir}
%dir %{_pixmapsdir}/backgrounds
%dir %{_privsepdir}
%{_libdir}/browser-plugins
%{_fontsdir}

%if "%{_lib}" == "lib64"
%dir /usr/lib64/security
%dir /usr/lib64/browser-plugins
%dir /usr/lib64/cmake
%dir /usr/lib64/mozilla
%dir /usr/lib64/mozilla/extensions
%dir /usr/lib64/pkgconfig
%endif

%files debuginfo
%defattr(644,root,root,755)
%dir /usr/lib/debug
/usr/lib/debug/*
%dir /usr/src/debug


