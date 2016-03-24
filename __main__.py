#!/usr/bin/python
#TODO: Fix the arbitrage calculator function in exchange trader...
#TODO: Add blacklist for Whitecoin coinse
'''
Goal: to automate all arbitrage trading.
This will be done in several steps:
Planning Phase(2step trade max so far):
  Need to have option for ignore coins-e
  1. Prompt for max allowed investment(bitcoin)
  2. Read market data from markets(Need to refresh periodically in later phases)
  3. Filter out all markets that are under maintence or are non-cryptocurrency markets on one side or are only present on one site.
  4. Read in current trade rates, transaction fees and withdrawal fees:
  5. Perform calculations for all markets, for all site pairs, buying at market high and selling at market low, ignoring withdrawal fee. Filter out all cases with no profit(majority) or less than threshold.
  6. Print all cases to log file(if wanted).
  7. With remaining markets, find max of allowed investment, and trade volumes, and calculate results, including withdrawal fee. Sort by profit.
  8. Print all cases to file(if wanted).
  9. Check if profit is below threshold or 0(remember to show next step if case)
  10. For the five most profitable cases, calculate approximate processing time, refresh data and recalculate above, and display all info. display recommended course of action to user and ask for confirmation.(ALso warn about needing user to manually do coins-e withdrawals.
Action Phase:
  If coins-e based: need to tell user to transfer himself and check every minute if completed.
  Log all trade data, including time for trade to complete.
  1. Display action screen and display time and constantly update progress...
  2. Check if needed funds are in first account and transfer from wallet if needed. (generate if haven't already)(Check if transfered every minute).
  3. Create trade on first market at price determined.(Check if completed every 30 seconds)
  4. Once compelte, withdraw to address of second market(generate if haven't already).(Check if transfered every minute).
  5. Create trade on second market at price determined.(Check if completed every 30 seconds)
  6. Once complete, withdraw to origin account.(Optional).(Check if transfered every minute).
  7. Perform sanity check to determine if ending amount is greater than starting amount. If not, apologize profusely, log error, and quit.
  8. Say "Congratulations! You earned _____ BTC/LTC!."
  9. Return to Planning phase and loop until user is sick of money.
  


'''