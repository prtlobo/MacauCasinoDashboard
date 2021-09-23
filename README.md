# Macau Casino Financial Dashboard
### This is a dashboard comparing and displaying the financials of Macao top casino hotels. Casinos included are Galaxy Entertainment Group (GEG), Wynn Resorts (WYNN), Sociedade de Jogos de Macau (SJM), MGM China Holdings (MGM), and Sands China (SANDS)*.
##### * Melco Resorts & Entertainment Limited (MELCO) will be added at a later update as it is a NASDAQ listed stock (will need to convert USD to HKD)
### Dashboard is python coded, designed and configured using [Plotly's Dash](https://plotly.com/dash/) app platform and then hosted on [pythonanywhere](https://www.pythonanywhere.com/). You can visit my dashboard at [here](prtlobo.pythonanywhere.com).
### Data is queried using the [Financial Modeling Prep ](https://financialmodelingprep.com/) API using the companies HKEX listed tickers. As the financials are based on the HKEX, all prices shown are in HKD. This is a demo but it can be easily configured to allow any number of companies listed in HKEX. 

### TO DO:
* Add Melco by converting USD financials to HKD
* Tweak Visuals/ design
* Gather all financials of companies in same sector/industry to obtain average values.
* Add better error handling in API call file
* add vertical annotations to dates with major events (COVID, crackdowns,etc)
* Add Graham's number charts
* Add trend lines to data (LOWESS, Moving average)
