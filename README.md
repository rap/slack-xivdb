# slack-xivdb

A tiny python marshaller for pulling XIVDB info into a slack chatroom, for annoying work colleagues with information about Frumenty. 

Built on top of the default Heroku Python marshaller; you'll need the [Heroku Toolbelt](https://toolbelt.heroku.com/), and a free tier account to deploy it. You can follow the [Python Deployment Steps](https://devcenter.heroku.com/articles/getting-started-with-python#deploy-the-app) to create a new Heroku instance to deploy it, and then configure a new Outgoing Webhook in Slack that points to https://[your heroku deployment].herokuapp.com/slacklookup/ . 

Text response is Qiqirn-like, so use an appropriate icon for maximal semantic sensemaking.

# Usage

In Slack, type (trigger) (seach string), and you'll get back a unique reference or a clump of five valid references. You can also use -exact at the front of the string to get back a precise match.

