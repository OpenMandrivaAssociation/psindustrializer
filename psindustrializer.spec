%define name	psindustrializer
%define version	0.2.5
%define release 7

%define major	0
%define libname %mklibname psphymod %major

Name: 	 	%{name}
Summary: 	Percussion Sample Generator (Discrete Mass Physical Modelling)
Version: 	%{version}
Release: 	%{release}

Source0:	%{name}-%{version}.tar.bz2
Source1: 	%{name}48.png
Source2: 	%{name}32.png
Source3: 	%{name}16.png
URL:		https://uts.cc.utexas.edu/~foxx/industrializer/
License:	GPL
Group:		Sound
#BuildRequires:	libgnome-devel gtk+2-devel gettext
#BuildRequires:	gtkglarea2-devel mesaglu-devel desktop-file-utils
BuildRequires:	pkgconfig(gtkgl-2.0)
BuildRequires:	pkgconfig(audiofile)
BuildRequires:	pkgconfig(glu)
BuildRequires:	desktop-file-utils

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
sed -i 's/if test "$AUDIOFILE_CONFIG" = "no" ; then/if false; then/' configure
export CFLAGS="%{optflags} -laudiofile"
%configure2_5x --disable-audiofiletest
%make

%install
%makeinstall_std

#fix desktop file location
mkdir -p %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=psindustrializer
GenericName=Sound Editor
Comment=Power Station Industrializer
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=AudioVideo;Audio;Video;Player;
EOF


#mv %{buildroot}%{_datadir}/gnome/apps/Multimedia/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
rm -f %{buildroot}%{_datadir}/gnome/apps/Multimedia/%{name}.desktop

#menu

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="Sequencer" \
  --add-category="X-MandrivaLinux-Multimedia-Sound" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

#icons
mkdir -p %{buildroot}/%_liconsdir
cat %SOURCE1 > %{buildroot}/%_liconsdir/%name.png
mkdir -p %{buildroot}/%_iconsdir
cat %SOURCE2 > %{buildroot}/%_iconsdir/%name.png
mkdir -p %{buildroot}/%_miconsdir
cat %SOURCE3 > %{buildroot}/%_miconsdir/%name.png

%find_lang %name

%files -f %{name}.lang
%doc README
%{_bindir}/%name
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*
%{_datadir}/%{name}/*.xpm
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png

%files -n %{libname}
%{_libdir}/*.so.*

%files -n %{libname}-devel
%{_includedir}/psphymod
%{_libdir}/*.so
%{_libdir}/*.a
