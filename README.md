This project is still actively under development and is not intended to be used in production environment. It is highly inadvisable to execute this software on a live trading environment in its current state.

Please refer to the UML Class Diagram for an overview of the design of the software.
The TODO.txt file contains plans for upcoming work on the software, as well as a brief overview of the changes I am currently making the backtesting system.
The backtesting system is not included here as it is being completely rewritten, however an old test script has been kept so that the basic functionality of the 
  old system can still be seen.

REQUIRED LIBRARIES
Pandas
Numpy
Alpaca.py      - This will be removed in the next update in favour of a REST approach.
Backtesting-py - Required only for legacy backtesting test script
Bokeh          - Required only for legacy backtesting test script

Note that code is functional but is missing required files.

For the live environment, you must add a 'Constants.py' file which contains the following constants:
API_KEY           # Alpaca API key
API_SECRET    # Alpaca API Secret Key
VERSION_ID   # Currently 0.2
PAPER_MODE # Should the trader use real money or simulated trades? True = Simulated

To run the backtesting test script, data must be provided into the folder "Historical_Test_Data". The data currently used does not have a license to be redistributed and so cannot be published here.
