---
layout: post
title: Explore Fast & Fix Things
categories: Technology
---
### because *Move Fast & Break Things* doesn't work in Healthcare

Building Health Tech has its nuances & challenges. You can't build it like other software. You certainly can't break things while building health tech.

This philosophy is unique to software engineering. You would rarely see it applied in other engineering disciplines. But with healthcare, you can't follow it even while doing software engineering. Why is it so? That's what this blog tries to answer.

Let's start with understanding what "Move fast & Break Things" stands for.

## 1. Move fast & Break Things (MFBT)

### Philosophy behind the mantra

MFBT is an ideology that backs speedy delivery of software and fast iteration of development. It means that even if you break things down, that’s okay - as long as you’re faster than your competitors in rebuilding it. The speed of shipping code & features is paramount. The idea is to fail fast & fail often.

This mantra advocates getting it out there and see if it works. Learn from mistakes & keep iterating.

### The Bug Cost in software development

It's easy to see why MFBT works so well with software development. It’s because the bug cost (the monetary loss that the bug causes) is low in the virtual world.

Broke your library management system? No worries - engineers will night the bug out.

Is the fancy feature of your new app throwing tantrums? Bet on your engineering team to debug it within a week.

<center>
<figure>
    <img src="{{ site.url }}/images/explore_fast/software_bugs.jpeg" width="400"/>
</figure>
</center>

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


<center>
<figure>
    <img src="{{ site.url }}/images/explore_fast/misaligned_bridge.jpeg"/>
    <figcaption><i>Bugs in real life!</i></figcaption>
</figure>
</center>

The bug cost to go back and build it again is humongous. That's because a major chunk of costs to build software is comprised of man hours. While in the real world, the cost of land, raw materials & machinery counts for more.

### The Two Extremes

Building software at startups and building bridges lie at the two extremes of bug cost.


<center>
<figure>
    <img src="{{ site.url }}/images/explore_fast/graph/graph-1.png"/>
    <figcaption><i>Two extremes of bug cost</i></figcaption>
</figure>
</center>

Does the bug cost for writing every new software lie at the bottom of this chart?

Can you think of examples where the software accompanied a very costly project thereby taking its bug cost higher?

..

..

..

I insist. Think of an example before scrolling down!

..

..

..
##### Apollo guidance computer

How about *The Apollo guidance computer* - the software in the spaceflight that first landed humans on the Moon? Imagine the bug-cost if the mission failed due to a software bug.

<center>
<figure>
    <img src="{{ site.url }}/images/explore_fast/Apollo11.jpeg" alt="apollo11" width="400"/>
</figure>
</center>

NASA recently released the codebase on [GitHub](https://github.com/chrislgarry/Apollo-11/). The detailing in design and maintenance of code is immaculate ([Link](https://history.nasa.gov/computers/Ch2-6.html?mod=article_inline)). Every change was minutely tracked. It mimics the kind of planning done for projects like bridges & skyscrapers. It's because the bug cost is enormous.

Having seen a counter example, let's jump to healthcare now.

## 2. *Primum non nocere* - First, do no harm!

### Philosophy behind the mantra

The principle of *"First, do no harm"* is central to clinical practice & medical education. There are debates about the origin of this axiom and its feasibility in practice. But in general, we can conclude that the element of recklessness arising due to speed of execution is a big no in healthcare.

This principle is at loggerheads with software engineering's *"Move fast & break things"*.

<center>
<figure>
    <img src="{{ site.url }}/images/explore_fast/meme.jpeg" width="600"/>
    <figcaption><i>Software Development vs Healthcare</i></figcaption>
</figure>
</center>


As a health tech start-up, how do you navigate through this dilemma?

What operating principle gives you a middle ground between these two conflicting beliefs?

To answer it, let's first understand the bug cost analysis for health tech.

### Health tech & the bug cost chart

Health tech lies at an interesting point between the two extremes of building software & bridges. Health tech too comprises of building software but with a significant bug cost. And that cost is not all monetary. When systems break down in healthcare, it can lead to lifelong impairments.

Imagine a medical exam routing system that broke down because an update was shipped in haste! It can cause delays in getting the right diagnosis which can lead to loss of life.


<center>
<figure>
    <img src="{{ site.url }}/images/explore_fast/graph/graph-2.png"/>
    <figcaption><i>Health Tech & Apollo Mission in the bug cost chart</i></figcaption>
</figure>
</center>


Bad change is very costly in health tech. More than the immediate benefits of good change.


And it explains why health tech has not caught up with the rest of the world. Using what’s already working provides a safety cushion. The risk of drastic change might not be worth the rewards for healthcare professionals. And this fear is not wrongly placed. When you’re walking such a tight rope, it’s hard to adopt game-changing innovation.

That brings us to the new operating principle to build health tech.


## 3. Explore Fast & Fix Things (EFFT)

### Philosophy behind the mantra

Let's take a health tech example to understand the philosophy. Suppose you have developed state-of-the-art speech-to-text AI and want to use it to automate radiology reporting for Chest X-rays (CXR).

Let's call this application *Reportify*. Its goal is to reduce the manual effort wasted in typing out CXR reports. Let's understand both parts of this principle through the lens of *Reportify*.


### Explore Fast
The challenge with healthcare is that something as simple as reporting is also non-standardized. There are multiple ways to report a CXR around the industry. For example:

- Typing the report on personal editors (MS Word, Google Docs, etc.)
- Dictating the report to assistants
- Editing pre-filled reports
- Using web-based tools to drag-n-drop common findings

This is where *Explore Fast* becomes vital. You have to explore multiple pathways that radiologists take to arrive at the perfect solution.

Here too, you've to build & iterate fast. But with a major difference. The build iterations are not happening on the same software or piece of code. You're building different software to plug your AI in these pathways to see what sticks. So instead of building fast, you've to prioritize exploring fast.


<center>
<figure>
    <img src="{{ site.url }}/images/explore_fast/graph/graph-3.png"/>
    <figcaption><i>Iterating on Build vs Explore</i></figcaption>
</figure>
</center>


### Fix Things

The next point to ponder over is whether you can prioritize the speed of shipping over building the right app? What happens if you build it fast, deploy at a clinic & things break down? Even a delay of a couple of days can cause catastrophe.

In such scenarios, you must prioritize the seamless integration of your solution into the existing workflow. And make sure that during the initial days of deployment, the status-quo (existing workflow) is not affected even if your application goes down.

There's another interesting reasoning behind it. Healthcare professionals are used to working in a certain way. And drastic changes bring an added overhead of re-training the medical staff. Minimal changes to the existing workflow are much appreciated.

Coming back to fixing things - we must build *Reportify* with utmost care & minutely track changes that are going into the application. That coupled with seamless integration will cover both bases.

1. There are fewer chances of bugs in the application as there's a balance between speed & caution.
2. If *Reportify* still breaks down, seamless integration makes sure that the previous workflow is still working.




### Summary

You've to ruthlessly prioritize fixing things in the two scenarios:
1. While exploring, if the feedback from a workflow is not positive, learn what's not working & fix it.
2. When the application breaks down, act fast on debugging & fixing it.

 Gather learnings from each pathway and evolve them by fixing modules that aren't working.

 Finally, when the application is stable and stakeholders are happy, you can think about revolutionizing reporting by bringing in more innovations and moving away from the previous workflow.

Till then,

 <center><h1><i>Explore Fast & Fix Things</i></h1></center>


 <br>
 <br>
