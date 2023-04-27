# JDM_Scraper

# A Python web-scraping script which extracts the data from https://www.beforward.jp, a japanese used car exporter site.

## Extracted parameters:

Vehicle ID - internal beforward reference number <br />
Model <br />
Mileage (km) <br />
Engine (cc) <br />
Year <br />
Auction Grade - 2 / 3 / 3.5 / 4 / 4.5 / 5 / 6 / R (accident repaired) / RA (light accident repaired) <br />
Steering - Right / Left / Center
Transmission Automatic / Manual / CVT / Semi AT / Unspecified
Total Price USD
Original Price USD
Current Price USD
Discount %
Shipping Price USD
Location - Japanese Region / Korea / Singapore
Model Code
Fuel - Petrol / Diesel / LPG / Electric / Hybrid
Seats
Engine Code
Color
Drive - 2WD / 4WD
Number of Doors
Auction URL


# The data is then saved into an excel file in format JDM_Data_{date} in the script folder.
![image](https://user-images.githubusercontent.com/96234810/234986258-97b7fea3-4976-4d16-82fd-a7d84d16663d.png)

# Example dataset:
![image](https://user-images.githubusercontent.com/96234810/234986347-eaa25df8-0a6e-49d9-9fe4-df42d6633a1a.png)

# The shipping costs should be localized by the requests library.

# In the future I would love to add some additional sheets to create some funky graphs.

Hope someone will find this useful,
Thanks,
Krystian 

## Required libraries:
# requests, bs4 (beautiful soup), pandas
