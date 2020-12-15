# Bitcoin Emissions Calculator
# Huan Wang & Tsee Lee, 2020
import pandas as pd
import datetime
import locale
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'

#CSV inputs that can be updated as new data arises (eventually can be automated)

#The power data was extrapolated from two sources: https://www.eia.gov/energyexplained/energy-and-the-environment/where-greenhouse-gases-come-from.php and https://www.eenews.net/assets/2019/03/26/document_cw_01.pdf)
power = pd.read_csv("power.csv")
power.set_index("Energy Source", inplace=True)

#Bitcoin data was originally taken from https://www.blockchain.com/charts/n-transactions on 12/3/20
bitcoin = pd.read_csv("bitcoin.csv")

#More relatable equivalencies were derived from this source: https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references
equivalencies = pd.read_csv("equivalencies.csv")

#Was used for testing specific cell reference; left here as reference for later
#print(power.at["Petroleum","# of Homes' Yearly Energy Use per Bitcoin-Transaction"])

#Converts the String types in the Timestamp column to datetime objects that can be filtered by start/end dates.
bitcoin.Timestamp = pd.to_datetime(bitcoin["Timestamp"])

#Sets start/end dates and stores filtered dataframe to bitcoinFiltered; we can consider making this a user input?
startTime = pd.to_datetime("1/1/2020")
endTime = pd.to_datetime("12/31/2020")
bitcoinFiltered = bitcoin.loc[(bitcoin.Timestamp >= startTime) & (bitcoin.Timestamp <= endTime)]

#Finds the average daily transactions in 2020, then extrapolates to yearly total by multiplying it by number of days in year, and stores it to numTrans variable
numTrans = round(bitcoinFiltered["n-transactions"].mean() * 365)

'''
#Originally read in CSV data on power and emissions and converted bitcoin transactions to more relatable equivalency of number of homes' yearly energy expenditure. Deprecated in favor of for loop that does this for multiple equivalencies 

power["homeYearlyEnergyUse"] = numTrans * power["# of Homes' Yearly Energy Use per Bitcoin-Transaction"]

sumHomeYearlyEnergyUse = round(power["homeYearlyEnergyUse"].sum())
'''

#Takes equivalency ratios and creates new columns in the power dataframe that converts bitcoin emissions contribution data to given equivalency (e.g. number of smartphones charged)  
def convertEmissions(transactions):
  for equivalency in equivalencies["Equivalency Type"]:
    power[equivalency] = transactions * power["Emission Contribution/Bitcoin-Transaction"] / equivalencies.at[equivalencies.loc[equivalencies["Equivalency Type"] == equivalency].index[0],"Ratio (Million Metric Tons Co2E/x)"]

  #Not sure if this is necessary in Python but declaring an empty list to append to later
  sumList = []

  #Creates a list of sums of each of the equivalency columns added previously in the for loop to calculate the total equivalency from all power sources.
  for equivalency in equivalencies["Equivalency Type"]:
    currentSum = round(power[equivalency].sum())
    sumList.append(currentSum)

  #Adds the sumList data as a "Totals" column in the equivalencies dataframe
  equivalencies["Totals"] = sumList

#Hard-coding in estimated global credit card transactions in 2018 worldwide, based on 2020 Nilson Report (https://nilsonreport.com/research_featured_chart.php or here to avoid paywall https://www.cardrates.com/advice/number-of-credit-card-transactions-per-day-year) 
numCCTrans = round(368.92 * 10**9)

#The ratio of 94 kWh/transaction for bitcoin was taken from https://www.vice.com/en/article/ypkp3y/bitcoin-is-still-unsustainable&sa=D&ust=1607274752180000&usg=AFQjCNGL0Ay292Jo7Iu4VgEM_bJzA_Zt3A. It has been reported as high as 741 (https://www.statista.com/statistics/881541/bitcoin-energy-consumption-transaction-comparison-visa/%23statisticContainer&sa=D&ust=1607274752175000&usg=AFQjCNE_NcBxSKtqMM3JdAo0GjXwtsoybA), but the first source described the methodology, while the second had a paywall.
bitEnergy = 94

#The ratio of .00149 kWh/credit-card-transaction was taken from https://www.statista.com/statistics/881541/bitcoin-energy-consumption-transaction-comparison-visa/%23statisticContainer&sa=D&ust=1607274752179000&usg=AFQjCNFwPHFrYWYNnmrlEFX6aJTIbelVQA.
#Other report the Bitcoin 
ccEnergy = .00149 

#This variable can be used to show the equivalent number of credit card transactions that can be made from one bitcoin transaction from an energy/emissions perspective.
ccToBitRatio = (bitEnergy / ccEnergy)
ccEquivalent = round(ccToBitRatio * numTrans) 

#Prints out all the equivalencies. We can consider making this a user input instead, giving them a selection of equivalencies, and conditionally outputting the value based on their equivalency selection. 
def printEquivalencies():
  for x in range(len(equivalencies["Equivalency Type"])):
    print("That's the carbon equivalent of", f'{equivalencies.iloc[x,2]:n}', equivalencies.iloc[x,0] + ".")

#---------------UX Print Statements---------------
print("Approximately", f'{numTrans:n}', "transactions were done globally on Bitcoin from", startTime.strftime('%b %d, %Y'), "to", endTime.strftime('%b %d, %Y') + ".")
print("\n")

convertEmissions(numTrans)
printEquivalencies()
print("That's also equivalent to the carbon emissions generated from", f'{ccEquivalent:n}', "credit card transactions, a", round(ccEquivalent / numTrans), "times difference.")
print("\n")

print("Approximately", f'{numCCTrans:n}', "transactions were processed by credit cards globally in 2018.")
print("\n")
#I separated the print and the input statements because for whatever reason the input text would get cut off when trying to wrap around the line in the terminal.
#Doesn't seem to be a problem anymore.
print("What percentage of those transactions do you think could be replaced by Bitcoin transactions in the future?")
predictedTrans = float(input(""))

print("\n")

#Assumes entire percentage of those credit card transactions turn into Bitcoin transactions and then subtracts the approximate emissions impact of the now-disappeared credit card transactions by converting the deducted credit card transactions to equivalent Bitcoin transactions and then deducts that converted value from the new Bitcoin transactions for a "net increase in Bitcoin transactions"
convertBitcoinTrans = round((predictedTrans/100 * numCCTrans) * (1 - 1 / ccToBitRatio))

print("That would mean", f'{convertBitcoinTrans:n}', "more net bitcoin transactions yearly.")
print("\n")
convertEmissions(convertBitcoinTrans)
printEquivalencies()
