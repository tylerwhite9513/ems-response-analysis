# Exploratory Data Analysis Summary

Dataset: 368,065 dispatch records, 2018-01-01 to 2024-12-31

## Response Time Overview

- Mean: 15.06 min
- Median: 15.01 min
- 90th percentile: 21.43 min
- 95th percentile: 23.26 min
- Std dev: 4.89 min

## Response Time by Region

| Region_Type   |   count |   mean |   median |
|:--------------|--------:|-------:|---------:|
| Suburban      |   73811 |  15.06 |    15.01 |
| Urban         |  257605 |  15.05 |    15.01 |
| Rural         |   36649 |  15.09 |    15.03 |

## Response Time: AI vs Human Dispatch Coordinator

| Dispatch_Coordinator   |   count |   mean |   median |
|:-----------------------|--------:|-------:|---------:|
| AI                     |   73478 |  15.08 |    15.03 |
| Human                  |  294587 |  15.05 |    15    |
