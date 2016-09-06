---
layout: page
title: 1_Introduction
permalink: /1_introduction/
---

# Contents
{:.no_toc}

* Contents
{:toc}

# Introduction


Location is a key element of many processes and activities, and the
understanding of human movement behaviour is becoming increasingly
important. Knowledge of people’s locations and related mobility patterns
are important for numerous activities, such as urban planning, transport
planning and facility management. How to efficiently use the available
space, is a common problem in many fields. In the educational sector,
universities are struggling to meet the higher expectations of
facilities for education and research by students and academic staff.
Managing the campus of a university has become a complex and challenging
task, including the involvement of many stakeholders. Campus managers
are in need for evidence-based information to support their decision
making[^1]. This includes better location data to detect
activities, occupancy and usage of the infrastructure.

To understand the human motion behaviour many studies are conducted
based on data collection of GPS receivers. The Global Navigation
Satellite System (GNSS) is commonly used to track people in large scale
environments. Speck (2008)[^2] studied the movement of pedestrians in
city centres, where potential participants were asked to carry a GPS
receiver. However, the distribution of GPS devices to participants
limits the possibilities to collect location data at a large scale.
Furthermore, due to poor quality of received signals from satellites in
indoor environments, GPS receivers are not suitable in these conditions.
Technological developments in the acquisition of location data by smart
phones and the use of Wi-Fi networks, enables new opportunities to track
users.

Wireless Local Area Networks (WLAN) are widely used for indoor
positioning of mobile devices within this network. The use of the Wi-Fi
network to estimate the location of people is an attractive approach,
since Wi-Fi access points (AP) are often available in indoor
environments. Furthermore, smart phones are becoming essential in daily
life, making it convincing to track mobile devices. This provides a
platform to track people by using WLAN as a sensor network, and study
the mobility of users inside buildings or groups of buildings.

At Delft University of Technology (TU Delft) a large scale Wi-Fi network
is deployed across all facilities covering the indoor space of the
campus. The network is known as an international roaming service for
users in educational environments and is called the eduroam network. It
allows students and staff members from the university to use the
infrastructure throughout the campus for free. This enables the
possibility to collect Wi-Fi logs, including individual scans of mobile
devices, at a large scale. A continuous collection of re-locations of
devices to access points for a long duration will return detailed
records of people’s movement. This ubiquitous and individual
georeferenced data derived from smart phones will present valuable
knowledge about the movement on the campus. Several work has been made
for studying human mobility patterns in a University’s campus.
Menses and Moreira (2012)[^3] used the eduroam network to study connectivity between
two places, by computing the number of movements between two places
within a given observation time period. Previous work has also been made
at TU Delft[^4], where several Wi-Fi monitors were placed
to detect occupation and movement between different faculties.

In this paper, we attempt to identify people’s movement patterns from
the eduroam network of TU Delft. Other than previous studies, this
research-driven project analysed data from more than 30.000 users, and
tries to detect movement patterns between buildings, and between large
indoor regions. The project is carried out in request of the
university’s department of Facility Management and Real Estate (FMRE).
With this project, we try to illustrate to what extend movement patterns
in and between buildings can be identified from anonymised Wi-Fi logs.
Firstly, individual states are extracted from the Wi-Fi logs, where
users stay for a longer time period. Secondly, movements are detected
between a sequence of states. Thirdly, movement patterns can be
identified by counting the amount of movement from, to or between
certain locations at different time intervals.

The aim of this paper is not to improve a Wi-Fi based positioning
technique, but to use the location data to conduct a mobility analysis
producing knowledge about the University’s campus. Based on the three
steps mentioned above, the aim of this project is to provide a method to
detect movement patterns from anonymised Wi-Fi logs. This includes the
separation of mobile devices (i.e. smart phones) and static devices
(e.g. laptops) from the Wi-Fi logs, and detecting movement to and from
beyond the spatial extent of the eduroam network by introducing the
concept of a ‘world’ state. Hereby, this paper attempts to contribute
with a method to automatically mine people’s movement patterns at two
spatial levels. First, movement at building level is analysed.
Subsequently, indoor movement at building-part level is studied, by
constructing a network graph of the underlying building floorplan. The
structure of this paper is as follows. Section *Case description*, describes the case study of TU
Delft, the tracking technique and the acquired data that is used in the
study. In section *Methodology* we present our methodology. Section *Results* discusses the obtained results.
Finally, in section *Conclusion and Recommendations*, we present our concluding remarks and recommendations.

## Case description

The project’s main area of interest is the campus of Delft University of
Technology (TU Delft), used by more than 30.000 students and staff
members. The eduroam network of the TU Delft campus consists of 1730
access points, distributed over more than 30 buildings, covering all
indoor space. Even large outdoor areas around the buildings have access
to the Wi-Fi network, because of the range of APs. Connection to the
Wi-Fi eduroam network is free of charge and requires only a NetID (i.e.
username and password), which all students and staff get upon
registration at the university. Every time a user accesses the network,
the connection is logged. When the connected device moves from one AP to
another, a new log is done. The location of the AP a mobile device is
connected to, will give an estimation of the mobile devices’ location,
and thus the person. This allows the tracking of devices in space and
time by relating buildings and building-parts to an aggregation of APs.

The data is collected for every single AP over a period of almost two
months. The logs are stored in a database on a virtual server at regular
intervals of 5 minutes. In order to ensure privacy, MAC addresses and
NetIDs (i.e. usernames) are hashed. Every log is stored with a start
time, session duration, AP name and a description of the AP’s location
(e.g. System Campus > 20-Aula > 2nd floor). The AP name always
contains the ID of the building it is located in. We can use this ID to
locate APs at building level. For the Faculty of Architecture and the
Built Environment, we also had information about the exact physical
position of each AP. This geo-referenced information is used to analyse
movement at building-part level.

[^1]:Heijer den, Alexandra (2012). “Managing the University Campus: Exploring models for the future and supporting today’s decisions”.
[^2]:Spek, SC van der (2008). “Mapping Pedestrian Movement: Using Tracking Technologies in Koblenz”. In: Lecture Notes in Geoinformation and Cartography, pp. 95–118.
[^3]:Meneses, Filipe and Alberto Moreira (2012). “Large scale movement analysis from WiFi based location data”. In: Indoor Positioning and Indoor Navigation (IPIN), 2012 International Conference on. IEEE, pp. 1–9.
[^4]:Kalogianni, E et al. (2015). “Passive WiFi Monitoring of the Rhythm of the Campus”. In: Proceedings of The 18th AGILE International Conference on Geographic Information Science. AGILE, pp. 1–4.

# References
