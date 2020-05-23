## Project Topic:
### Dialogflow Fulfillment Cross-Border Driver Monitoring Software 
### Using Interactive Chatbot as Part of a Multipronged Approach to 
### Fight the COVID-19 Pandemic

## Introduction: 
The COVID-19 outbreak and the resulting social distancing recommendations and related restrictions have led to numerous short-term changes in economic and social activity around the world. According to the ILO as reported on the UN news site, the risks of food insecurity are now emerging because of containment measures, including border closures implemented by governments. While it is important for governments to ensure a reduction in the risks of inter-border infections, it is equally critical to ensure that the food supply chain is not disrupted.

I have come up with a solution that implements cross-border driver monitoring to address the issue of food supply-chain disruption. The success of our solution is, however, dependent on the collaboration between governments at all levels, and the private sector as part of a multi-pronged approach to fight COVID-19. 

Ensuring that the movement of food and other important materials can move across state borders safely, would require public health departments and the transport unions to:

1. Test, Register and approve all inter-state truck drivers and their staff for each trip. This will require rapid testing methods for covid-19.
2. Conduct periodic tests on all interstate drivers and update the records database.
3. Educate all drivers on COVID-19 and how to conduct themselves while in transit.
4. Use our software to monitor interstate drivers at state borders to verify from the digital travel records if the drivers have been approved for the ongoing trip.

Cross-border driver monitoring helps governments reduce transmission and ensure the food supply chain is not disrupted. This will mitigate the collateral impacts on children, women, and vulnerable populations.

That’s why I recommend that adopting and deploying cross-border driver monitoring system is a key milestone to reopen economies.

## Technology Components used:
1.	Python
    1.	  Flask Framework
2.	Google Dialogflow.
3.	Google App engine.
4.	Redis Data Store.


## Setup Instructions

### Redis DB Setup
 1. You can set this up on localhost or any server of your choice

### Dialogflow Setup
 1. Create an account on Dialogflow
 1. Create a new Dialogflow agent
 1. Restore the `dialogflow-agent.zip` ZIP file in the root of this repo
   1. Go to your agent's settings and then the *Export and Import* tab
   1. Click the *Restore from ZIP* button
   1. Select the `dialogflow-agent.zip` ZIP file in the root of this repo
   1. Type *RESTORE* and and click the *Restore* button

### Fulfillment Setup
 1. Deploy fulfillment to App Engine
   1. [Download and authenticate the Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstart-macos)
   1. Run `gcloud app deploy`, make a note of the service URL, which will be used in the next step
 1. Set the fulfillment URL in Dialogflow to your App Engine service URL
   1. Go to your [agent's fulfillment page](https://console.dialogflow.com/api-client/#/agent//fulfillment)
   1. Click the switch to enable webhook for your agent
   1. Enter you App Engine service URL (e.g. `https://webhook-10929.appspot.com/`) to the URL field
   1. Click *Save* at the bottom of the page

## How to report bugs
* If you find any issues, please open a bug here on GitHub

## How to make contributions?
Please read and follow the steps in the CONTRIBUTING.md

## License
See LICENSE.md

## Terms
Your use of this sample is subject to, and by using or downloading the sample files you agree to comply with, the [Google APIs Terms of Service](https://developers.google.com/terms/) and the [Dialogflow's Terms of Use and Privacy Policy](https://dialogflow.com/terms/).