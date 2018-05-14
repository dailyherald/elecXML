# XML election files

In which I'm striving to learn how to parse xml with Python with election data files using the Hart InterCivic Tally source.

Tree

|  EDX  |  Count  |  Description  |
|  ---  |  ---:  |  ---  |
|  StateDefinedCodes  |  1  |    |
|  ->VotingMethodDefinitions  |  1  |    |
|  -->VotingMethodCode  |  3  |    |
|  County  |  1  |    |
|  ->Election  |  1  |    |
|  -->DataSources  |  1  |    |
|  --->DataSource  |  1  |    |
|  ---->SourceDescription  |  1  |    |
|  -->Parties  |  1  |    |
|  --->Party  |  3  |    |
|  -->Contests  |  1  |    |
|  --->Contest  |  564  |    |
|  ---->Choice  |  357  |    |
|  -->BallotStyles  |  1  |    |
|  --->BallotStyle  |  751  |    |
|  -->Precincts  |  1  |    |
|  --->Precinct  |  228  |    |
|  ---->Splits  |  228  |    |
|  ----->Split  |  1348  |    |
|  ------>Voters  |  4044  |    |
|  -->PollingPlaces  |  1  |    |
|  --->PollingPlace  |  115  |    |
|  -->PrecinctSplitContests  |  1  |    |
|  --->PrecinctSplitContest  |  12446  |    |
|  -->ElectionTally  |  3  |    |
|  --->PrecinctTally  |  684  |    |
|  ---->SplitTally  |  4044  |    |
|  ----->ContestTally  |  37338  |    |
|  ------>CastVoteTally  |  67545  |    |
|  ----->ReportingSummaryList  |  4044  |    |
|  ------>ReportingSummary  |  4044  |    |
