# -*- coding: utf-8 -*-
"""Module H — New platforms: floats, gliders, BGC-Argo, animals (slides 85-120)."""
import math
from lib import *
from qcore import Bank
from ma import LS
V = VERIFIED

def build():
    B = Bank('mh', seed=18); A = B.add
    G = V['bgc_argo_may2025']; F = V['bgc_argo_fractions']
    A('What does Munk (2000), quoted on slide 85, say about the first century of modern oceanography?',
      'It was “a century of undersampling”', ['It was a century of overfishing', 'It was a century of perfect sampling', 'It was a century without ships'],
      'Slide 85: “The ocean is critically undersampled, as nicely summarized by Munk (2000): ‘if I were to choose a single phrase for the first century of modern oceanography, it would be a century of undersampling’.”', 1, 'Undersampling', src='Lecture, slide 85')
    A('What does slide 2 show?',
      'The time and space scales of ocean processes and which platforms (satellites, floats, gliders, moorings) cover them', ['The optical properties of pure water', 'The depth of the Secchi disk', 'The map of Argo floats'],
      'Slide 2: horizontal scale from 1 mm to 10 000 km against time scale from 1 second to 100 years, with ovals for processes (Langmuir cells, internal tides, phytoplankton blooms, eddies, ENSO…) and rectangles for platforms. No single platform covers all scales.', 1, 'Scales', src='Lecture, slide 2')
    A('Which platform does slide 91 present, and what is special about it?',
      'FLIP (Floating Instrument Platform, Scripps): a 355-foot non-propelled platform that flips to a vertical position', ['A satellite of 355 feet', 'A glider with wings', 'A sediment trap'],
      'Slide 91 caption: “Scripps Institution of Oceanography’s Floating Instrument Platform (FLIP) is a 355-foot long non-propelled research platform”.', 1, 'Platforms', src='Lecture, slide 91')
    A('How does the profiling float of slide 94 work?',
      'It sinks to depth (up to 2000 m), drifts, then rises measuring temperature and salinity, and transmits its data to a satellite at the surface', ['It stays at the surface and measures wind', 'It is towed by a ship at constant depth', 'It is anchored to the sea bottom'],
      'Slide 94 drawing: “Submersion, measures water temperature and salinity while floating up, data transmission”, layers marked at 1000 m and 2000 m (“Sinks down to 2000 m”).', 1, 'Float', src='Lecture, slide 94')
    A('Which sensors are listed on the bio-optical profiling float of slide 97?',
      'Radiometer (412, 490, 532 nm), transmissometer (660 nm), Chl a and CDOM fluorometers, backscattering meter (555 nm)', ['Only a thermometer', 'A sonar and a camera', 'A radar and a magnetometer'],
      'Slide 97 labels. The bio-optical glider of slide 98 carries backscatter (2 wavelengths), Chl and CDOM fluorescence, downwelling irradiance (4 wavelengths), upwelling radiance (4 wavelengths), CTD and oxygen.', 2, 'Sensors', src='Lecture, slides 97–98')
    A('Which sensors does the bio-optical glider of slide 98 carry in addition to a CTD?',
      'Backscatter and Chl/CDOM fluorescence, downwelling irradiance and upwelling radiance (4 wavelengths each), and oxygen', ['Only an altimeter', 'A radiometer for gamma rays', 'A seismometer'],
      'Slide 98 labels.', 2, 'Sensors', src='Lecture, slide 98')
    A('How many contributions of autonomous platforms are listed on slide 101?',
      'Seven, from extending the satellite signal to the interior to identifying interior processes missed by ocean colour', ['Two', 'Four', 'Twelve'],
      'Slide 101: (1) extension of the satellite signal to the interior, (2) validation of level 2 and 3 products, (3) validation of bio-optical primary-production models (Chl a or phytoplankton carbon), (4) validation of coupled circulation–biogeochemical models, (5) data assimilation, (6) statistical biogeochemical/bio-optical trends for climate applications, (7) identification of interior pattern processes missed by ocean colour.', 1, 'Contributions', src='Lecture, slide 101')
    A('Why can a profiling float add information that a satellite cannot (slides 102–103)?',
      'It works under clouds, in winter and below the surface; e.g. it saw a bloom in clouded spring 2005 that SeaWiFS and MODIS missed', ['It sees the surface only, like a satellite', 'It has a larger swath than a satellite', 'It measures atmospheric aerosols'],
      'Slide 102 (Taylor et al., Ocean Optics 2006): satellite data “were unable to detect the blooming event in this highly cloudy area”. Slide 103 (Claustre et al., 2011): winter mixing and surface Chl in the South Pacific Gyre.', 2, 'Contributions', src='Lecture, slides 102–103')
    A('What did Boss et al. (2008) report on slide 104 about backscattering at depth at the end of 2006?',
      'An increase in backscattering at depth associated with the float being trapped in an eddy, a signature not visible in surface data', ['A failure of the sensor with no physical meaning', 'A bloom visible from space', 'An earthquake'],
      'Slide 104 text.', 2, 'Float data', src='Lecture, slide 104')
    A('What is shown on slide 105 (“Obtaining POC from Beam-c (660)”)?',
      'A SOLO “Carbon Explorer” float whose beam-c signal gives POC; two North Pacific blooms after a dust deposition event (iron fertilisation?), with POC and SeaWiFS Chl covarying (Bishop et al., 2002)', ['A ship measuring wind', 'A satellite measuring salinity', 'A laboratory fluorometer'],
      'Slide 105 text. Slide 66 gives the relationship between c_p(660) and POC.', 2, 'Float data', src='Lecture, slides 66, 105')
    A('What did gliders show in the Mediterranean front of slides 107–109?',
      'Sections of currents, density, salinity, Chl and CDOM across the front (Ligurian Sea, Jan 2007), with MODIS Chl and SST maps for context', ['A hurricane', 'A coral reef survey', 'An oil spill'],
      'Slides 107–109: glider transect from Villefranche toward the Boussole/DYFAMED site, 28–31 Jan 2007; MF = marginal/frontal zone, FC = central zone.', 2, 'Gliders', src='Lecture, slides 107–109')
    A('What problem do Sackmann et al. (2008, slides 110–111) address with a Seaglider?',
      'Daytime fluorescence quenching of chlorophyll a: reduced near-surface fluorescence each day, with a mixed-layer depth and b_bp(700) shown alongside', ['Seaglider speed', 'Salinity drift', 'Ice thickness'],
      'Slide 111 caption: arrows mark reduced near-surface fluorescence resulting from daytime quenching; dashed lines at midnight; pink line = mixed layer depth.', 2, 'Gliders', src='Lecture, slides 110–111')
    A('How many Argo floats does slide 113 show, and for which date?',
      '4153 floats on 30 June 2025', ['415 floats on 30 June 1995', '41 530 floats in 2025', '153 floats in 2005'],
      'Slide 113 (read directly from the page).', 1, 'Argo', src='Lecture, slide 113')
    A('Slide 114 compares XBT and Argo profile locations for 2000 and 2007. What does it illustrate?',
      'The evolution of both networks: XBT profiles follow ship tracks, Argo gives an even global coverage', ['Argo is limited to ship tracks', 'XBTs cover the whole ocean evenly', 'The two networks are identical'],
      'Slide 114 caption: “XBT (red) and Argo (blue) profile locations for the years 2000 (top) and 2007 (bottom) illustrate the evolution of both networks.”', 1, 'Argo', src='Lecture, slide 114')
    A('Which sensors are most frequently found on operational BGC-Argo floats in May 2025 (slide 115)?',
      f'Oxygen ({G["oxygen"]}), then suspended particles/b_bp and chlorophyll a ({G["suspended_particles"]} each)', [f'Downwelling irradiance ({G["downwelling_irradiance"]})', f'Full BGC floats ({G["full_bgc"]})', f'pH ({G["ph"]}) before oxygen'],
      f'Slide 115 legend (read at 250 dpi): operational floats {G["operational"]}; suspended particles {G["suspended_particles"]}; downwelling irradiance {G["downwelling_irradiance"]}; pH {G["ph"]}; nitrate {G["nitrate"]}; chlorophyll a {G["chlorophyll_a"]}; oxygen {G["oxygen"]}; full BGC floats {G["full_bgc"]}. Fractions of the {G["operational"]}: oxygen {F["oxygen"]*100:.0f} %, b_bp {F["suspended_particles"]*100:.0f} %, irradiance {F["downwelling_irradiance"]*100:.0f} %.', 2, 'BGC-Argo', src='Lecture, slide 115')
    A('What share of operational BGC-Argo floats carry the full BGC sensor set in slide 115?',
      f'≈ {V["bgc_full_fraction"]*100:.0f} % ({G["full_bgc"]} of {G["operational"]})', [f'≈ {F["oxygen"]*100:.0f} %', '≈ 50 %', '≈ 100 %'],
      f'{G["full_bgc"]}/{G["operational"]} = {V["bgc_full_fraction"]:.3f} (Python). Counts read from the slide legend; “full BGC” definition is not on the slide.', 2, 'BGC-Argo', src='Lecture, slide 115')
    A('Why do slides 119–120 show an elephant seal?',
      'Animals carrying small sensors sample polar regions that floats and ships rarely reach, returning temperature and Chl profiles', ['To measure the weight of seals', 'To show a protected species list', 'To illustrate Case 2 waters'],
      'Slides 119–120: “Other biogeochemical/bio-optical platforms: elephant seal”; profiles of temperature and Chl over ≈ 100 days and tracks on globes.', 1, 'Animals', src='Lecture, slides 119–120')
    B.essay('List the seven contributions of autonomous platforms (slide 101) and illustrate three of them with examples from slides 102–112.',
            'List: slide 101 items 1–7. Examples: under clouds (slide 102: float saw the 2005 North Atlantic bloom that SeaWiFS/MODIS missed); winter mixing (slide 103: South Pacific Gyre Chl vs mixed-layer thickness); interior patterns missed by colour (slide 104: eddy with high b_bp at depth); POC from beam-c (slide 105); quenching correction (slides 110–111).',
            2, 'Contributions', src='Lecture, slides 101–112')
    B.essay('Compare the sensors of a bio-optical float and of a bio-optical glider (slides 97–98) and relate each sensor to an IOP or biogeochemical variable studied in modules D–F.',
            'Float: radiometer 412/490/532 nm (light field, K_d), transmissometer 660 nm (c_p → POC, slide 105), Chl fluorometer (Chl, quenching issue), CDOM fluorometer (a_cdom proxy), backscattering 555 nm (b_bp → particles). Glider: b_bp at 2 wavelengths, Chl/CDOM fluorescence, E_d and L_u at 4 wavelengths, CTD, oxygen.',
            2, 'Sensors', src='Lecture, slides 97–98')

    sl = [
        S('An under-sampled ocean', cols(LS(2, 430), dul(['Scales from mm to 10 000 km', 'Seconds to 100 years', 'No single platform covers all', 'Munk (2000): “a century of undersampling”']), flex=[3, 2])),
        S('Profiling float', cols(LS(94, 430), dul(['Sinks to 2000 m', 'Measures while rising', 'Data sent by satellite']), flex=[3, 2])),
        S('Bio-optical profiling float', cols(LS(97, 430), dul(['Radiometer 412/490/532', 'Transmissometer 660 nm', 'Chl and CDOM fluorometers', 'Backscatter 555 nm']), flex=[3, 2])),
        S('Bio-optical glider', cols(LS(98, 430), dul(['Backscatter, Chl and CDOM fluorescence', 'Downwelling irradiance and upwelling radiance, 4 wavelengths', 'CTD and oxygen']), flex=[3, 2])),
        S('Seven contributions of autonomous platforms', cols(LS(101, 430), dul(['Extend the satellite signal inward', 'Validate products and models', 'Assimilate into models', 'Trends; interior patterns']), flex=[3, 2])),
        S('Sampling under clouds and in winter', cols(LS(102, 430), dul(['Float versus SeaWiFS and MODIS', 'Spring 2005 bloom missed from space', 'Slide 103: winter mixing, South Pacific Gyre']), flex=[3, 2])),
        S('Gliders across a front', cols(LS(109, 430), dul(['Currents, density, salinity', 'Chl and CDOM sections', 'Ligurian Sea, Jan 2007']), flex=[3, 2])),
        S('Argo and BGC-Argo', cols(LS(115, 430, 'Lecture slide 115 (May 2025)'), dul(['Argo: 4153 floats (30 Jun 2025)', f'BGC-Argo operational: {G["operational"]}', f'Oxygen {G["oxygen"]}, particle backscatter {G["suspended_particles"]}', f'Full BGC floats: {G["full_bgc"]}']), flex=[3, 2])),
        S('BGC-Argo sensors', img('bgc_sensors', 1160, cap='Own plot of the counts read from lecture slide 115 (May 2025)')),
        S('Key points', dul(['Ocean undersampled in space and time', 'Floats and gliders add the vertical dimension', 'Seven contributions (slide 101)', 'BGC-Argo: oxygen on nearly all, optics on 550–790'], xl=True)),
    ]
    mod = dict(id='mh', slug='08-new-platforms', title='H · New platforms', en='Floats, gliders, BGC-Argo and other autonomous platforms (slides 85–120)',
               qtitle='Guiding question: why do we need autonomous platforms, and what do they measure?',
               question='<p>Ships give precise but sparse data, satellites see only the surface layer of clear skies. Profiling floats, gliders, BGC-Argo and even animals extend the observations in depth and time, and carry bio-optical sensors that measure the IOPs of modules D–F.</p>',
               sections=[
                ('Why new platforms', '<p>“The ocean is critically undersampled” (Munk 2000, slide 85). Slide 4 shows the extreme contrast: ≈ ½ million Secchi/Chl points in 100 years versus about ½ million SeaWiFS observations every ≈ 30 s, each with spatial bias and gaps. Slide 2 places every process and platform on a space–time diagram.</p>'),
                ('Floats, gliders and what they carry', '<p>Profiling floats sink to about 2000 m, drift and rise measuring (slide 94); bio-optical versions add a radiometer (412, 490, 532 nm), a 660 nm transmissometer, Chl and CDOM fluorometers and a 555 nm backscattering meter (slide 97). Gliders carry backscatter, fluorescence, E<sub>d</sub> and L<sub>u</sub> at four wavelengths, CTD and oxygen (slide 98). Slide 101 lists seven contributions to science and operations (see the quiz).</p>'),
                ('Argo and BGC-Argo today', f'<p>Slide 113: 4153 Argo floats on 30 June 2025. Slide 115 (BGC-Argo, May 2025): {G["operational"]} operational floats; oxygen {G["oxygen"]}, suspended particles {G["suspended_particles"]}, chlorophyll a {G["chlorophyll_a"]}, pH {G["ph"]}, nitrate {G["nitrate"]}, downwelling irradiance {G["downwelling_irradiance"]}, full BGC {G["full_bgc"]} (read from the legend). The two numbers 4153 and 788 come from different maps/dates and are not combined into a percentage.</p>'
                 '<div class="callout warn"><b class="t">Not verified</b>Slides 116–118 (web viewer, section plots) are too small to read numbers; slides 107–112 are used only as illustrations of what gliders show.</div>')],
               checklist=['Quote Munk (2000) and the slide-4 contrast.', 'List float and glider sensors (slides 97–98).', 'List the seven contributions (slide 101).', 'Give one example of a float or glider result (slides 102–112).', 'Give the Argo and BGC-Argo counts and their dates.'],
               summary=['Đại dương bị lấy mẫu thiếu; phao và glider thêm chiều sâu và hoạt động dưới mây.', 'Phao sinh-quang học: bức xạ kế, truyền qua 660 nm, huỳnh quang Chl/CDOM, tán xạ ngược 555 nm.', 'Slide 101: bảy đóng góp của nền tảng tự hành.'],
               calcs=[], quiz_n=10,
               v2=dict(we_title='Counts from slide 115', we=f'<p>{G["full_bgc"]} of {G["operational"]} operational BGC floats carry the full set ({V["bgc_full_fraction"]*100:.0f} %); oxygen is on {F["oxygen"]*100:.0f} % and the b<sub>bp</sub> sensor on {F["suspended_particles"]*100:.0f} %.</p>',
                       qa=[('Why not just use satellites?', 'They see the surface layer, only through clear skies (slide 102).'), ('What do bio-optical floats add?', 'Vertical profiles of Chl, b_bp, c_p and irradiance all year (slides 97, 103).')],
                       hooks=[('Satellites: wide and shallow. Floats: narrow and deep.', 'Vệ tinh: rộng, nông. Phao: hẹp, sâu.')]))
    return mod, sl, B
