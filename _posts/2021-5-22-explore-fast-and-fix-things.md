---
layout: post
title: Explore Fast & Fix Things&#58;
categories: Technology
---
### because "Move Fast & Break Things" doesn't work in Healthcare

Building Health Tech has its nuances & challenges. You can't build it like other software. You certainly can't build fast & break things in healthcare.

This philosophy is unique to Software engineering. You would rarely see it applied in other engineering disciplines. But with healthcare, you can't follow it even while building software. Why is it so? This blog answers it.

Let's start with understanding what does "Move fast & Break Things" stands for?

### The philosophy behind MFBT (Move fast & Break Things)

MFBT is an ideology that backs speedy delivery of software and fast iteration of development. It means that even if you break things down, that’s okay - as long as you’re faster than your competitors in rebuilding it. The velocity of shipping code & features is paramount.

The mantra is to get it out there and see if it works. Learn from mistakes & keep iterating.

### The Bug Cost in software development

It's easy to see why MFBT works so well with software development. It’s because the bug cost (the monetary loss that the bug causes) is low in the virtual world.

Broke your library management system? No worries - engineers will night the bug out. That fancy feature of your new app is throwing tantrums? Bet on your engineering team to debug it within a week.

| ![]({{ site.url }}/images/explore_fast/software_bugs.jpeg) |
|:--:|
|*Software Bugs*|

Note that I am talking about start-ups here. Of course, if Twitter or Gmail goes down, the bug cost for these companies is humongous.

But when you're starting up, such bugs cost you a week of developer's payroll and a few affected customers & transactions.

### Bug cost in other engineering disciplines

Compare software development to building things in the real world.

Can a civil engineer afford to move fast & break things while building a bridge?

Can you follow *agile development* while building a skyscraper?

Nope. All the designs & planning have to be done beforehand. Meticulously.

Why? Because the bug cost is huge.

Unlike the virtual world, the real world doesn't have the option to *Edit*. You can edit a text message but not what you said face to face.

You can't *edit* pillars of the bridge if they have been misaligned.


| ![]({{ site.url }}/images/explore_fast/misaligned_bridge.jpeg) |
|:--:|
|*Bugs in real life!*|

The bug cost to go back and build it again is humongous. That's because a major chunk of costs to build software is comprised of man hours. While in the real world, the cost of land, raw materials & machinery counts for more.

### The Two Extremes

Building software at startups and building bridges lie at the two extremes of bug cost.

| ![]({{ site.url }}/images/explore_fast/graph/graph-1.png) |
|:--:|
|*Two extremes of bug cost*|

Does the bug cost for writing every new software lie at the bottom of this chart?

Can you think of examples where the software accompanied a very costly project thereby taking its bug cost higher?

##### The Apollo guidance computer

How about *The Apollo guidance computer* - the software in the spaceflight that first landed humans on the Moon? Imagine the bug-cost if the mission failed due to a software bug.

NASA recently released the codebase on [GitHub](https://github.com/chrislgarry/Apollo-11/). The detailing in design and maintenance of code is immaculate ([Link](https://history.nasa.gov/computers/Ch2-6.html?mod=article_inline)). Every change was minutely tracked. It mimics the kind of planning done for projects like bridges & skyscrapers. It's because the bug cost is enormous.

### Where does Healthcare lie in the bug cost chart?

Healthcare lies at an interesting point between the two extremes. You are building software but with a significant bug cost. And that cost is not all monetary. When systems break down in healthcare, it can lead to lifelong impairments.

Imagine a medical exam routing system that broke down because an update was shipped in haste! It can cause significant delays in getting the right diagnosis which in extreme cases can lead to loss of life.

Bad change is very costly in health tech. More than the immediate benefits of good change.

| ![]({{ site.url }}/images/explore_fast/graph/graph-2.png) |
|:--:|
|*Health Tech & Apollo Mission in the bug cost chart*|

And it explains why health tech has not caught up with the rest of the world. Using what’s already working provides a safety net. The risk of drastic change might not be worth the rewards for healthcare professionals. This fear is not wrongly placed. When you’re walking such a tight rope, it’s hard to adopt game-changing innovation.
