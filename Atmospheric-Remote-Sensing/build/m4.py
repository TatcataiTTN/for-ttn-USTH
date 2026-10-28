# -*- coding: utf-8 -*-
"""M4 — Pointing geometries of spaceborne sensors (study guide Ch.4)."""
from lib import *
from qcore import Bank
V = VERIFIED
two = lambda a, b: cards(a, b, cols=2)

def build():
    B = Bank('m4', seed=4)
    B.add('What are the three main pointing geometries of satellite sensors that sound atmospheric composition?',
          'Nadir (looking down), limb (looking tangentially through the edge), occultation', ['Nadir, zenith and polar', 'Limb, geostationary orbit and elliptical orbit', 'Nadir, off-nadir and whiskbroom scanning'],
          'Guide Ch.4: nadir (including off-nadir/cross-track scanning), limb (scattering or emission), occultation (Sun, Moon, stars, GNSS).', 1, 'Three geometries', origin='goc', src='Study guide Ch.4 (checklist)')
    B.add('How does the nadir mode work?',
          'The sensor looks down at the Earth (or scans across track) and measures backscattered sunlight or thermal emission', ['The sensor looks tangentially through the atmospheric edge and measures forward-scattered radiation', 'The sensor looks at the Sun at sunrise or sunset to measure transmission', 'The sensor emits a laser pulse and measures the return time'],
          'Guide 4.1: examples TROPOMI, OMI, GOME-2, IASI, MOPITT, OCO-2. The field of view crosses the atmosphere once, vertically.', 1, 'Nadir', src='Study guide 4.1')
    B.add('In limb mode, how does the sensor look and how does it scan in altitude?',
          'Tangentially, just above the horizon, scanning the line of sight vertically (tangent heights ~5 to 100 km)', ['Vertically down, deriving altitude from pulse delay', 'At the rising Sun, deriving altitude from the time of observation', 'At 45° from zenith, deriving altitude from temperature'],
          'Guide 4.2: it measures scattered sunlight (OSIRIS, OMPS-LP, SCIAMACHY limb) or thermal emission (MIPAS, MLS microwave).', 1, 'Limb', src='Study guide 4.2')
    B.add('How does occultation differ from limb sounding?',
          'It views a light source (Sun, Moon, star, GPS signals) through the edge of the atmosphere and measures the transmission I/I₀', ['It measures thermal emission of the atmosphere in the microwave', 'It looks straight down, so there is no line of sight through the edge', 'It carries its own light source and measures its backscatter'],
          'Guide 4.3: SAGE II/III, ACE-FTS (Sun), GOMOS (stars), GNSS radio occultation (temperature/humidity).', 1, 'Occultation', src='Study guide 4.3')
    B.add('What is the main advantage of nadir?',
          'Good horizontal resolution (a few km, TROPOMI 5.5×3.5 km²), daily global coverage, and sensitivity to the troposphere/boundary layer', ['1–3 km vertical resolution from geometry', 'Self-calibration through the ratio I/I₀', 'No influence of surface or clouds'],
          'Guide 4.4: nadir suits air quality and emissions. Drawbacks: poor vertical resolution (a column or 1–6 pieces of information), sensitivity to surface, clouds and aerosols.', 1, 'Comparison', src='Study guide 4.4')
    B.add('What is the main disadvantage of nadir?',
          'Poor vertical resolution, sensitivity to surface albedo/emissivity, clouds and aerosols; the path through the atmosphere is short so the signal per layer is weak', ['Only a few tens of profiles per day', 'It cannot see the troposphere', 'Very poor horizontal resolution (200–400 km)'],
          'Guide 4.4. Nadir is strong in horizontal resolution but weak in vertical resolution — the opposite of limb and occultation.', 2, 'Comparison', src='Study guide 4.4')
    B.add('What is the main advantage of limb sounding?',
          'Good vertical resolution (1–3 km), a long path so high sensitivity, and no surface background (dark space behind)', ['Horizontal resolution of a few km and daily global coverage', 'It sees the boundary layer', 'Simple retrieval without a complex radiative transfer model'],
          'Guide 4.4. Drawbacks: poor horizontal resolution along the line of sight (~200–400 km), cannot see below ~5–10 km, complex RT, pointing must be known precisely.', 1, 'Comparison', src='Study guide 4.4')
    B.add('What is the main disadvantage of limb sounding?',
          'Poor horizontal resolution (~200–400 km) and no view below ~5–10 km, so it is unsuited to the boundary layer; complex RT', ['Vertical resolution of only tens of km', 'Strong sensitivity to surface albedo', 'Only a few profiles per day because it depends on sunrise and sunset'],
          'Guide 4.4. The line of sight is hundreds of km long, so horizontal resolution is poor; clouds and path saturation block the view below the upper troposphere.', 2, 'Comparison', src='Study guide 4.4')
    B.add('Why is occultation called "self-calibrating"?',
          'Because the ratio I/I₀ (measured outside and through the atmosphere) cancels instrument drift, giving very accurate long-term trends', ['Because the instrument changes its wavelength to match the lines', 'Because it uses the Moon as an external calibration standard', 'Because it needs no radiative transfer model at all'],
          'Guide 4.4: strong solar signal, ~1 km vertical resolution, high S/N, simple RT (Beer–Lambert).', 2, 'Comparison', src='Study guide 4.4')
    B.add('What is the biggest disadvantage of solar occultation?',
          'Very poor coverage: only ~30 profiles per day (2 per orbit), depending on orbit and latitude', ['Accuracy many times worse than limb', 'It cannot see the stratosphere', 'It depends strongly on surface albedo'],
          '30 profiles/day ÷ 2 per orbit implies about 15 orbits/day — consistent with a low Earth orbit. Guide 4.4.', 1, 'Comparison', src='Study guide 4.4')
    B.add('Which geometry is best for monitoring long-term stratospheric ozone trends with the highest accuracy?',
          'Solar occultation: self-calibrating (I/I₀), high vertical resolution, good trend quality', ['Nadir: best global coverage and horizontal resolution', 'Emission limb: works day and night', 'Geostationary orbit: hourly observations'],
          'Answer key Q4(b-i). The poor coverage is accepted because the goal is an accurate trend.', 2, 'Choosing a geometry', origin='goc', src='Mock exam Q4(b)(i)')
    B.add('Which geometry is best for mapping NO₂ emissions of individual cities?',
          'Nadir: km-scale horizontal resolution, daily global coverage, sensitivity to the boundary layer', ['Occultation: highest accuracy', 'Limb: 1–3 km vertical resolution', 'Emission limb: measures day and night'],
          'Answer key Q4(b-ii): urban emissions need the horizontal resolution and boundary-layer sensitivity that limb and occultation lack.', 2, 'Choosing a geometry', origin='goc', src='Mock exam Q4(b)(ii)')
    B.add('What does a geostationary orbit add compared with a low-Earth sun-synchronous orbit for air-quality monitoring?',
          'Hourly observation of one continent, so the diurnal cycle (rush hours, photochemistry) is seen, plus more cloud-free scenes', ['Hourly global coverage including both poles', 'Better horizontal resolution than LEO because it is farther away', 'Global limb coverage'],
          'Answer key Q4(c). LEO passes once a day at a fixed local time but is global; GEO (GEMS, TEMPO, Sentinel-4) sees only one region.', 2, 'Orbits', origin='goc', src='Mock exam Q4(c)')
    B.add('How can the tropospheric column be obtained by combining nadir and limb (as in SCIAMACHY, OMPS)?',
          'Tropospheric column = total column (nadir) minus stratospheric column (limb)', ['Tropospheric column = limb column multiplied by the nadir AMF', 'Tropospheric column = total column plus stratospheric column', 'Tropospheric column = occultation column divided by the Ångström exponent'],
          'Guide, closing note of 4.4: nadir sees the whole column, limb sees the stratospheric part; the difference is the troposphere.', 2, 'Orbits', src='Study guide 4.4 (notes)')
    B.add('What characterises a sun-synchronous low-Earth orbit?',
          'Global coverage once per day at a fixed local time', ['Continuous observation of one continent every hour', 'Even global coverage every hour', 'Standing still above one point of the equator'],
          'Guide 4.4: sun-synchronous LEO (TROPOMI, OMI, GOME-2) passes each place at the same local time; a geostationary satellite is fixed relative to the ground.', 1, 'Orbits', src='Study guide 4.4 (notes)')
    B.add('Which pair describes typical horizontal and vertical resolution correctly?',
          'Nadir: horizontal a few km, vertical coarse; limb: horizontal ~200–400 km, vertical ~1–3 km', ['Nadir: horizontal ~200–400 km, vertical ~1 km; limb: horizontal a few km, vertical coarse', 'Both: horizontal a few km and vertical ~1 km', 'Nadir: horizontal ~1 000 km; limb: horizontal ~1 km'],
          'Guide Figure 14: there is a trade-off between horizontal and vertical resolution; occultation: vertical ~1 km but poor horizontal.', 2, 'Comparison', src='Study guide 4.4, Figure 14')
    B.add('Which method does NOT obtain altitude directly from geometry?',
          'Nadir: altitude is inferred from weighting functions, not from geometry', ['Limb: tangent height of each ray', 'Solar occultation: tangent height at sunrise/sunset', 'GNSS occultation: bending angle of the signal ray'],
          'Limb and occultation geometry give vertical resolution directly through tangent height; nadir needs weighting functions and an a priori.', 3, 'Comparison', src='Study guide 4.2–4.4')
    B.essay('(a) Sketch the nadir, limb and solar occultation geometries.\n(b) Which geometry would you choose to (i) monitor long-term trends of stratospheric ozone with the highest accuracy, (ii) map NO₂ emissions from individual cities? Justify.\n(c) What does a geostationary orbit add compared with a low-Earth sun-synchronous orbit?',
            '(a) Draw the Earth, the atmospheric shell and lines of sight: nadir goes straight down; limb is tangent to the edge; occultation goes from the Sun through the edge to the sensor (see Figure 13 of the guide).\n'
            '(b)(i) Solar occultation: self-calibrating I/I₀, ~1 km vertical resolution, high S/N → good trends. (b)(ii) Nadir: km-scale horizontal resolution, daily coverage, boundary-layer sensitivity.\n'
            '(c) Hourly observation of one continent → diurnal cycle, rush hours, photochemistry, more cloud-free scenes; LEO gives one fixed-local-time overpass per day but global coverage.', 3, 'Mock exam', origin='goc', src='Mock exam Q4 (2.5 points) + suggested answer')
    B.essay('Tabulate the advantages and disadvantages of nadir, limb and occultation.',
            'Nadir: + good horizontal resolution, global coverage, sees the troposphere, day (UV-vis) and day-night (TIR); − poor vertical resolution, sensitive to surface/clouds/aerosols, short path. '
            'Limb: + 1–3 km vertical resolution, long path so sensitive, no surface background, emission works day and night; − ~200–400 km horizontal, no view below 5–10 km, complex RT. '
            'Occultation: + self-calibrating, accurate, ~1 km vertical, high S/N, simple RT; − only ~30 profiles/day, poor horizontal, only upper troposphere and stratosphere.', 2, 'Comparison', origin='goc', src='Study guide Ch.4 (table 4.4)')
    sl = [
        cover('Pointing geometries of spaceborne sensors', 'Study guide chapter 4',
              '<b>Atmospheric Remote Sensing</b> · USTH<br>Nadir · limb · occultation · low and geostationary orbits'),
        S('Three viewing geometries', figfit('f3_geometries', 'Figure 13 (study guide): nadir, limb and occultation.', 360) + ulb(['<b>Nadir</b>: looking down — TROPOMI, OMI, GOME-2, IASI, OCO-2', '<b>Limb</b>: looking tangentially — OSIRIS, MIPAS, MLS', '<b>Occultation</b>: looking at the Sun through the edge — SAGE, ACE-FTS'], 27, 12)),
        S('Nadir: pros and cons', two(
            card('Advantages', '• Horizontal resolution of a few km (TROPOMI 5.5×3.5 km²)<br>• Daily global coverage<br>• Sees the troposphere/boundary layer<br>• Day (UV-vis), day and night (TIR)'),
            card('Disadvantages', '• Poor vertical resolution (a column or 1–6 pieces of information)<br>• Sensitive to albedo, emissivity, clouds, aerosols<br>• Short path → weak signal per layer'))),
        S('Limb: pros and cons', two(
            card('Advantages', '• Vertical resolution 1–3 km<br>• Long path → very sensitive<br>• No surface background<br>• Emission limb: day and night'),
            card('Disadvantages', '• Horizontal resolution ~200–400 km<br>• No view below ~5–10 km<br>• Complex RT (sphericity, multiple scattering)<br>• Pointing must be known precisely'))),
        S('Occultation: pros and cons', two(
            card('Advantages', '• Self-calibrating: I/I<sub>0</sub> cancels instrument drift<br>• Very accurate, good for long-term trends<br>• Strong signal, ~1 km vertical, high S/N<br>• Simple RT (Beer–Lambert)'),
            card('Disadvantages', '• Very poor coverage: ~30 profiles/day (2 per orbit)<br>• Latitude bands depend on the orbit<br>• Poor horizontal resolution along the path<br>• Only upper troposphere and stratosphere'))),
        S('Trade-off: horizontal vs vertical resolution', figfit('f15_tradeoff', 'Figure 14 (study guide): approximate horizontal and vertical resolution of typical instruments for each geometry.', 480) + '<p class="note">Nadir wins on horizontal resolution; limb and occultation win on vertical resolution.</p>'),
        S('Orbits: LEO and geostationary', cards(card('Sun-synchronous LEO', 'Global coverage once per day at a fixed local time.<br>TROPOMI, OMI, GOME-2'),
          card('Geostationary (GEO)', 'Hourly view of one continent → diurnal cycle of pollution.<br>GEMS, TEMPO, Sentinel-4'),
          card('Nadir + limb', 'Tropospheric column = total (nadir) − stratospheric (limb).<br>SCIAMACHY, OMPS'), cols=3)),
        S('Choosing a geometry by goal', dtable(tbl(['Goal', 'Geometry', 'Reason'], [
            ['Most accurate stratospheric ozone trend', 'Solar occultation', 'Self-calibrating, high S/N, ~1 km'],
            ['NO₂ emissions of individual cities', 'Nadir', 'Km-scale horizontal resolution, boundary-layer sensitivity'],
            ['Detailed stratospheric chemistry profiles', 'Limb', 'Vertical resolution 1–3 km, many species'],
            ['Diurnal cycle of pollution', 'Geostationary nadir', 'Hourly observation']]), 'xl')),
        S('Exam checklist — Chapter 4', chk(['Three geometries: nadir, limb (scattering/emission), occultation (Sun, stars, Moon, GNSS)', 'Trade-off: horizontal resolution and tropospheric sensitivity (nadir) ↔ vertical resolution and accuracy (limb/occultation)', 'Occultation = self-calibrating, most accurate, worst coverage', 'Draw the three geometries with the Earth, atmosphere shell and lines of sight'])),
        S('Key points', dul(['Nadir: good horizontal, poor vertical resolution', 'Limb: good vertical, poor horizontal, cannot see low', 'Occultation: self-calibrating and accurate, but few profiles', 'Geostationary: hourly diurnal cycle']))]
    mod = dict(id='m4', slug='04-pointing-geometries', title='M4 · Pointing geometries', en='Pointing geometries of spaceborne sensors',
               question='<ul><li>What are the possible pointing geometries of spaceborne sensors for sounding the atmospheric composition?</li><li>What are the advantages and disadvantages of each case?</li></ul>',
               calcs=[], checklist=['Three geometries: nadir, limb (scattering/emission), occultation (solar/stellar/lunar/GNSS).', 'Trade-off: horizontal resolution & tropospheric sensitivity (nadir) ↔ vertical resolution & accuracy (limb/occultation).',
                                    'Occultation = self-calibrating, best accuracy, worst coverage.', 'Draw the three geometries with Earth, atmosphere shell, lines of sight.'],
               summary=['Nadir: nhìn thẳng xuống → độ phân giải ngang tốt, phủ toàn cầu hằng ngày, nhìn thấy tầng đối lưu; nhưng độ phân giải thẳng đứng kém, nhạy với mây/bề mặt.',
                        'Limb: nhìn tiếp tuyến qua rìa khí quyển → độ phân giải thẳng đứng tốt (1–3 km), không có nền bề mặt; nhưng độ phân giải ngang kém, không xuống thấp dưới ~5–10 km.',
                        'Che khuất (occultation): nhìn Mặt Trời/sao qua rìa khí quyển → tự hiệu chuẩn, rất chính xác; nhưng số lượng phép đo rất ít.'],
               sections=[
        ('Three geometries, in plain words', '<p>The same atmosphere can be viewed in three ways: <b>looking straight down</b>, like a photo from an aircraft (nadir); <b>looking sideways across the edge</b>, like viewing a slice of cake from the side (limb); and <b>looking at the rising or setting Sun through the atmosphere</b> (occultation).</p>' +
         lfig('f3_geometries', 'Figure 13 (study guide): nadir, limb and occultation.') +
         hx_table(['Geometry', 'How it looks', 'Example instruments'], [['Nadir (and off-nadir/cross-track)', 'Looks down; measures backscattered sunlight (UV-vis-SWIR) or thermal emission (TIR)', 'TROPOMI, OMI, GOME-2, IASI, MOPITT, OCO-2'],
             ['Limb', 'Looks tangentially above the horizon, scanning tangent heights ~5 to 100 km; measures scattered light or thermal emission', 'OSIRIS, OMPS-LP, SCIAMACHY limb (scattering); MIPAS, MLS (emission)'],
             ['Occultation', 'Looks at the Sun, Moon, a star or GNSS signals through the edge at sunrise/sunset; measures I/I₀', 'SAGE II/III, ACE-FTS, GOMOS (stars), GNSS radio occultation']], 'left')),
        ('Advantages and disadvantages', hx_table(['Geometry', 'Advantages', 'Disadvantages'], [
            ['Nadir', '• Good horizontal resolution (a few km; TROPOMI 5.5×3.5 km²), daily global coverage<br>• Sees the troposphere and boundary layer → air quality, emissions<br>• Day (UV-vis) and day and night (TIR)', '• Poor vertical resolution (a column or 1–6 pieces of information)<br>• Sensitive to surface albedo/emissivity, clouds, aerosols<br>• Short path → weak signal per layer'],
            ['Limb', '• Good vertical resolution (1–3 km) from geometry<br>• Long path → very sensitive, many stratospheric species<br>• No surface background (dark space)<br>• Emission limb: day and night', '• Poor horizontal resolution along the line of sight (~200–400 km)<br>• No view below ~5–10 km (clouds, saturation) → not for the boundary layer<br>• Complex RT (sphericity, multiple scattering); pointing known very precisely'],
            ['Occultation', '• Self-calibrating: I/I₀ cancels drift → very accurate, good for trends<br>• Strong solar signal, ~1 km vertical, high S/N<br>• Simple RT (Beer–Lambert)', '• Very poor coverage: ~30 profiles/day (2 per orbit for the Sun)<br>• Latitude bands depend on the orbit; poor horizontal along the path<br>• Only upper troposphere and stratosphere']], 'left') +
         lfig('f15_tradeoff', 'Figure 14 (study guide): approximate horizontal and vertical resolution of each instrument type.')),
        ('Orbits matter too', '<p>Geometry is only half of the story; the <b>orbit</b> is the other half:</p><ul><li><b>Sun-synchronous LEO</b>: global coverage once per day at a fixed local time.</li><li><b>Geostationary</b> (GEMS, TEMPO, Sentinel-4): nadir observation of one continent every hour → the <b>diurnal cycle</b> of pollution (rush hours, photochemistry) and more cloud-free scenes.</li><li><b>Nadir + limb</b> (SCIAMACHY, OMPS): tropospheric column = total column (nadir) − stratospheric column (limb).</li></ul>' +
         callout('info', 'Choose by goal', 'Most accurate stratospheric ozone trend → solar occultation. NO₂ emissions of individual cities → nadir. Detailed stratospheric chemistry profiles → limb.'))])
    return mod, sl, B
