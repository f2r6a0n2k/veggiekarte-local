[![GitHub issues](https://img.shields.io/github/issues/KristjanESPERANTO/veggiekarte-local)](https://github.com/KristjanESPERANTO/veggiekarte-local/issues)
[![GitHub forks](https://img.shields.io/github/forks/KristjanESPERANTO/veggiekarte-local)](https://github.com/KristjanESPERANTO/veggiekarte-local/network)
[![GitHub stars](https://img.shields.io/github/stars/KristjanESPERANTO/veggiekarte-local)](https://github.com/KristjanESPERANTO/veggiekarte-local/stargazers)
[![GitHub license](https://img.shields.io/github/license/KristjanESPERANTO/veggiekarte-local?style=plastic)](https://github.com/KristjanESPERANTO/veggiekarte-local/blob/master/LICENSE)

# Veggiekarte local

This is a fork of the world wide map [veggiekarte from piratenpanda](https://github.com/piratenpanda/veggiekarte). This map is for local use. Improvements will be added to the upstream project.

## Description

A OpenStreetMap based map to easily find places, like restaurants and cafes, with vegetarian and vegan options.

## Usage

You can use it in any modern browser or install it as an app (as an [PWA](https://en.wikipedia.org/wiki/Progressive_web_application)).

## Get involved

There are several ways to get involved:

1. Improve the data on OpenStreetMap
   1. Add missing places
   2. Add and correct information (like opening hours) of places
2. Report issues
3. Help to translate (take [locales/en.json](locales/en.json) as template)
4. Participate in development
5. Write reviews for places on [https://lib.reviews/](lib.reviews)

## Keys

The most important keys for us are [diet: vegan](https://wiki.openstreetmap.org/wiki/DE:Key:diet:vegan) and [diet: vegetarian](https://wiki.openstreetmap.org/wiki/DE:Key:diet:vegetarian). These keys are used to determine whether a place is shown on the Veggiekarte or not.

You can find an overview of which other keys we use at [Taginfo](https://taginfo.openstreetmap.org/projects/veggiekarte#tags).

## Website

- www.veggiekarte.de

## Third-party software and data

This is an overview of the third-party software and data we use. Many thanks to the open source community, especially to the authors of the following projects! ❤️ 🍻

| software                                                                                   | license                                                                                                          | version   | purpose                                                                               |
| ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------- |
| [chart.js](https://github.com/chartjs/Chart.js)                                            | MIT [\*](https://github.com/chartjs/Chart.js/blob/master/LICENSE.md)                                             | 3.5.1     | JavaScript library to creat charts. We use this in the `data_chart.html`.             |
| [i18next](https://github.com/i18next/i18next)                                              | MIT [\*](https://github.com/i18next/i18next/blob/master/LICENSE)                                                 | 21.3.3    | JavaScript internationalization framework.                                            |
| [leaflet](https://github.com/Leaflet/Leaflet/)                                             | BSD-2-Clause [\*](https://github.com/Leaflet/Leaflet/blob/master/LICENSE)                                        | 1.7.1     | JavaScript library to create interactive maps.                                        |
| [leaflet.control.geocoder](https://github.com/perliedman/leaflet-control-geocoder/)        | BSD-2-Clause [\*](https://github.com/perliedman/leaflet-control-geocoder/blob/master/LICENSE)                    | 2.2.0     | A control to locate places. The button with the magnifier 🔍.                         |
| [leaflet.easybutton](https://github.com/CliffCloud/Leaflet.EasyButton)                     | MIT [\*](https://github.com/CliffCloud/Leaflet.EasyButton/blob/master/LICENSE)                                   | 2.4.0     | Adding buttons. We are using it for the info button.                                  |
| [leaflet.featuregroup.subgroup](https://github.com/ghybs/Leaflet.FeatureGroup.SubGroup)    | BSD-2-Clause [\*](https://github.com/ghybs/Leaflet.FeatureGroup.SubGroup/blob/master/LICENSE)                    | 1.0.2     | Dynamically add/remove groups of markers.                                             |
| [leaflet.fullscreen](https://github.com/runette/Leaflet.fullscreen)                        | ISC [\*](https://github.com/runette/Leaflet.fullscreen/blob/gh-pages/LICENSE)                                    | 1.0.5     | Add a fullscreen button.                                                              |
| [leaflet.hash](https://github.com/siimots/leaflet-hash)                                    | MIT [\*](https://github.com/siimots/leaflet-hash/blob/master/LICENSE.md)                                         | 1.0.1     | Add coordinate hashes to the URL in the browser adress field.                         |
| [leaflet.languageselector](https://github.com/KristjanESPERANTO/Leaflet.LanguageSelector/) | CC0 [\*](https://github.com/KristjanESPERANTO/Leaflet.LanguageSelector/blob/master/LICENSE)                      | 1.2.0     | A control to switch between languages.                                                |
| [leaflet.locatecontrol](https://github.com/domoritz/leaflet-locatecontrol/)                | MIT [\*](https://github.com/domoritz/leaflet-locatecontrol/blob/gh-pages/LICENSE)                                | 0.74.0    | A control to locate the position of the user.                                         |
| [leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster/)                 | MIT [\*](https://github.com/Leaflet/Leaflet.markercluster/blob/master/MIT-LICENCE.txt)                           | 1.5.3     | Marker Clustering plugin.                                                             |
| [opening_hours.js](https://github.com/opening-hours/opening_hours.js)                      | LGPL-3.0-only [\*](https://github.com/opening-hours/opening_hours.js/blob/master/LICENSES/LGPL-3.0-or-later.txt) | 3.8.0-dev | Library to parse and process the opening_hours tag from OpenStreetMap data.           |
| [OpenStreeMap](https://www.openstreetmap.org)                                              | CC BY-SA [\*](https://www.openstreetmap.org/copyright)                                                           |           | There we get the data of the places. We also show the markers on an OpenStreeMap map. |
| icons from [OpenStreetMap Carto](https://github.com/gravitystorm/openstreetmap-carto)      | CC0 [\*](https://github.com/gravitystorm/openstreetmap-carto/blob/master/LICENSE.txt)                            |           | Default marker icons                                                                  |
| icons from [Maki](https://labs.mapbox.com/maki-icons/)                                     | CC0                                                                                                              |           | Fallback marker icons                                                                 |
| [veggiepenguin](https://openclipart.org/detail/189178/veggiepenguin)                       | CC0 [\*](https://openclipart.org/share)                                                                          |           | Favicon                                                                               |
