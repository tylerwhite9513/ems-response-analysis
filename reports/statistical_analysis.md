# Statistical Analysis

All tests use alpha = 0.05. Response times are in minutes.

## 1. AI vs Human Dispatch Coordinator (Independent t-test)

- AI mean response time: 15.080 min (n=73,478)
- Human mean response time: 15.051 min (n=294,587)
- t-statistic: 1.433, p-value: 0.1518
- **Conclusion:** No statistically significant difference between AI and human dispatch coordinator response times.

## 2. Response Time Across Region Type (One-way ANOVA)

- F-statistic: 0.946, p-value: 0.3882
- **Conclusion:** No statistically significant difference in response time across Urban/Suburban/Rural regions in this dataset.

## 3. Response Time Across Incident Type (One-way ANOVA)

- F-statistic: 1.655, p-value: 0.1743
- **Conclusion:** No statistically significant difference in response time across incident types.

## 4. Distance to Incident vs Response Time (Pearson correlation)

- r = 0.001, p-value: 0.4817
- **Conclusion:** No statistically significant positive linear relationship (weak in strength).

## 5. Traffic Congestion vs Response Time (Pearson correlation, ordinal-encoded)

- r = 0.000, p-value: 0.9232
- **Conclusion:** No statistically significant positive relationship between traffic congestion level and response time.

## 6. Region Type vs Dispatch Mode (Chi-square test of independence)

- Chi-square statistic: 1.277, degrees of freedom: 4, p-value: 0.8652
- **Conclusion:** Dispatch mode selection appears independent of region type in this dataset.
