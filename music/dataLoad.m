clear; close all; clc

[user,date,gendre,country,playcount,cao] = ...
    textread('userid-timestamp-artid-artname-traid-traname.tsv','%s%s%s%s%s%s','delimiter','\t','headerlines',0);