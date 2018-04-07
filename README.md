# stockpredict [![Build Status](https://travis-ci.org/thedataincubator/stockpredict.svg?branch=master)](https://travis-ci.org/thedataincubator/stockpredict)

## Overview: 
 
This repository contains a stock price predict app that is based on stock market data from Quandl. The goal of this repository is to work as a team to make some changes to the app and get experience on working on production codes. 

## Repository Organization:  

- _static_: contains static resources, stock price file in this case.   
- _stockpredict_: contains stockticker.py that reads in the stock price data and requests the prediction (done using Facebook prophet). templates folder contains the html template.   
- _tests_: test.py tests the app.  
- _.travis.yml_: specifies the programming language and testing environment. When new commits are made or pull request is submitted, Travis CI will run the tests specified in this file automatically.   
- _app.py_: entry point to the application, set up the environment variables, and call the codes that create the app.   
 
## Tasks:
1. Clone repo locally, ask Zach to get permissions to push branches
2. Choose an issue to work on and comment that you want to work on it.  Or create your own issue and comment that you want to work on that.
3. Make a branch (or two or three or ...) and open up a PR with a change you like.
4. Ask for a review from a peer.
5. Ask for a review from Zach or Dylan.
6. Once both reviews are passed, MERGE AWAY!

## Some useful commands:
- Checkout new branch `git checkout -b branch_name`
- Push new branch `git push --set-upstream origin branch_name`
- Switch branches `git checkout branch_name`
- Rebase on master `git rebase master`
