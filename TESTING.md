MEMBERS:
Eugene Ho
Ryan Davis
Kenneth Ford
Luke Nguyen

TEAM: FOUNDIT

VISION:
Analyzing the front page of the internet to identify and discover what interesting ideas people believe are worth discussing.

Automated Tests:
We tested which possible inputs for our site would be valid enough to pass through to our results page, which inputs would create errors and not be able to pass, and which inputs were valid, but perhaps would be impractical/inefficient to pass through. Negative values and all 0 values would pass these tests, but would obviously display nothing int he case of the 0s. We can decide not to do any data-dathering or displaying given certain 0/negative values to save efficiency.

Such tests included different numerical values including negative ints, inputs that started with a 0, and very large values.
Our website prohibits the passing of non-int values for all of our numerical inputs, but we have a string input in which any charcter is currently valid. Inputting special characters in this field would result in errors. Inputting strings of subreddits that did not exist or were restricted would result in error.

Leaving any field blank would result in error.

We believed that because of the single dyno we only have access to (Django) that large values would result in a timeout error, however with an input of 1 million, the application continued to run. The results may not finish in a timely manner, but they will eventually finish given proper inputs of any size.

![alt tag](https://raw.githubusercontent.com/LogicianJones/CSCI3308_Foundit/master/Screenshot_2017-04-06_06-39-53.png)
![alt tag](https://github.com/LogicianJones/CSCI3308_Foundit/blob/master/Screenshot_2017-04-06_06-40-42.png)

User Acceptance Test Plans:

1.
Use case name
	Enter a subreddit to analyze
Description
	Test the validity of the inputted string
Pre-Conditions
	User has an existing and non-restricted subreddit in mind
Test steps
	1.Go to site
	2.Enter subreddit name
	3.Make sure it is spelled right with no special characters
	4.Enter other values
Expected result
	User should be able to see analyzed data of subreddit
Actual result
	User is directed to results page
Status (Pass/Fail)
	Pass
Notes
	User must input all fields validly
	
2.
Use case name
	Enter numerical paramters for analysis
Desription
	Test validity of inputted int values
Pre-Conditions
	User uses html forms, as opposed to inputting values in URL
Test steps
	1.Go to site
	2.Enter numerical values
Expected result
	User should be able to see analyzed data relative to int values
Actual result
	User is directed to results page
Status (Pass/Fail)
	Pass
Notes
	User can bypass input requirements by entering them into the URL 		instead, if other characters are used in these fields, an error will occur

3.
Use case name
	User enters some 0 values
Description
	In case User does not wish to see certain details
Pre-conditions
	User must understand how site works, what each field means
Test steps
    1. Go to site
    2. User cannot enter 0 for all numerical fields
    3. Posts to seach much be greater than 0
    4. User must enter a non-0 value for at least 1 remaining field
Expected result
    User should see deminished quality of data
Actual result
    User is shown less data than usual, as opposed to values in all fields
Status (Pass/Fail)
    Pass
Notes
    Currently, User can enter 0 in all fields, even negative numbers, but there is no point in doing so. If User wishes to use our site to display no data, is it wrong for us as developers to deny him this right? If mass amounts of Users all enter trash values, we would lose processing power and time.
Post-conditions
	User stares at a blank screen for a few seconds
