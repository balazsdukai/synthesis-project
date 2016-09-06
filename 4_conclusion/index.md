---
layout: page
title: 4_Conclusion and Recommendations
permalink: /4_conclusion/
---

# Conclusion and Recommendations

To understand human motion behaviour for better decision making, many
studies have been conducted based on location data collection. Wi-Fi
tracking technology is increasingly used due its cost effectiveness and
ability to track people at a large scale. For this study, we used the
eduroam network of the TU Delft Campus to identify movement patterns.
Firstly, states are extracted from the raw Wi-Fi logs. Subsequently, the
event of going from one state to another can be detected as movement.
Finally, by counting the number of movement for an observation period,
movement patterns can be identified. This paper tried to illustrate to
what extend movement patterns in and between buildings can be identified
from anonymised Wi-Fi logs. We successfully identified movement patterns
at two spatial levels.

At building level, the rhythm of the campus is illustrated by time
profiles showing the amount of movement for different observation
periods. We found that movement at the campus was related to the lecture
hours. Flow and direction of aggregated movement can be visualized on a
map as edges. At building-part level, similar movement patterns can be
identified. An indoor network graph was created of the underlying
building floorplan. This successfully illustrates the occupied space for
movement. However, the range of APs can extent between building-parts
and floors and limits the accuracy of the analysis.

It is possible to identify movement patterns in and between buildings
using the eduroam network. The presented method automatically mines
movement patterns of large crowds from a dataset with anonymised Wi-Fi
logs. However, we also encountered limitations from which several
recommendations can be provided for future implementations.

The movement trajectory between two building-part states is computed
with a shortest path algorithm, using the constructed network graph.
Better models need to be implemented for a more accurate path
estimation. No data from APs on the way between two states is used to
estimate the path, because the system stores logs at a 5-minute
interval. With a shorter log interval, this can be considered. The
Faculty of Architecture and the Built Environment has a building lay-out
with separate building wings and only three floor levels. It is
important to mention that this building lay-out makes it easier to
distinguish between building parts. Considering the range of APs,
different methods need to be investigated for buildings with more floor
levels. This also means that for the identification of movement at room
level, other techniques, e.g. including Received Signal Strength (RSS),
need to be implemented. In this paper, the road network is not used to
estimate a detailed path of outdoor movement between building states.
Due to the spacious character of the TU Delft campus and limited
constrained space for pedestrians, it is challenging to analyse the
usage of the infrastructure. With several strategically placed APs
outdoor and logging with a higher frequency, this can be considered.
Detailed information about the usage of the infrastructure on the campus
can provide valuable knowledge, such as the identification of hotspots
at specific time periods.

