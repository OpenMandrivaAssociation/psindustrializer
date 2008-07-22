%define name	psindustrializer
%define version	0.2.5
%define release %mkrel 5

%define major	0
%define libname %mklibname psphymod %major

Name: 	 	%{name}
Summary: 	Percussion Sample Generator (Discrete Mass Physical Modelling)
Version: 	%{version}
Release: 	%{release}

Source:		%{name}-%{version}.tar.bz2
Source1: 	%{name}48.png
Source2: 	%{name}32.png
Source3: 	%{name}16.png
URL:		http://uts.cc.utexas.edu/~foxx/industrializer/
License:	GPL
Group:		Sound
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	libgnome-devel gtk+2-devel gettext
BuildRequires:	gtkglarea2-devel mesaglu-devel desktop-file-utils

%description
Industrializer is a program for generating percussion sounds for musical
purposes. Try using the sounds in your favorite tracker, or the upcoming
Beast / BSE tracker and modular synthesizer.

This program is great for generating new techno sounds, industrial sounds
in particular. But it's not limited to industrial crashes, it can produce
chimes, bubbles, gongs, hammer hits on different materials, and a variety
of other sounds. 

%package -n 	%{libname}
Summary:        Dynamic libraries from %name
Group:          System/Libraries
#Provides:	%name
#Obsoletes:	%name = %version-%release

%description -n %{libname}
Dynamic libraries from %name.

%package -n 	%{libname}-devel
Summary: 	Header files and static libraries from %name
Group: 		Development/C
Requires: 	%{libname} >= %{version}
Provides: 	libpsphymod-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes: 	%name-devel

%description -n %{libname}-devel
Libraries and includes files for developing programs based on %name.

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

#fix desktop file location
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
mv $RPM_BUILD_ROOT%{_datadir}/gnome/apps/Multimedia/%{name}.desktop $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

#menu

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="Sequencer" \
  --add-category="X-MandrivaLinux-Multimedia-Sound;AudioVideo" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
cat %SOURCE1 > $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
cat %SOURCE2 > $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
cat %SOURCE3 > $RPM_BUILD_ROOT/%_miconsdir/%name.png

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%endif
		
%if %mdkversion < 200900
%postun
%clean_menus
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc README
%{_bindir}/%name
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*
%{_datadir}/%{name}/*.xpm
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/psphymod
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la

