---
layout: post
title: PM Lessons I - Shape Up
---

This is the first blog of a series on lessons from the best books on building software products.

### Backdrop

Allow me to share a bit of a backdrop - Having a technical background and 5 years of experience in the tech industry has helped me in gaining some insights into how a product comes to life. My curiosity about the non-technical aspects of the lifecycle of a product pushed me to explore more about the field. There were multiple resources like MOOCs, blogs, and books to start with. Though blogs are great for getting a peripheral understanding, I found courses and books to be delving much deeper into the subject. I had fun doing [University of Alberta's course](https://www.coursera.org/specializations/product-management) on Software Product Management [last year](https://drive.google.com/file/d/1-P766V8iLysZk6jSX_ULQTJtu1tRxF4j/view?usp=sharing) - highly recommended if you want to get into the nitty-gritty of product management (PM).

### Books on PM
The next step is to explore the best books on building great software products. There are numerous blogs about must-read-books on PM & building great products in general. I feel sharing a short-summary or lessons from these books will be useful for the industry and help in pushing product managers into reading them.

### PM Lessons: Shape Up
I am starting with a book titled __Shape Up__ by _Ryan Singer_ (Head of Strategy, Basecamp). It is an excellent take on the process of product development. This book is available for free in [here](https://basecamp.com/shapeup/webbook).

Without further ado, let me share the PM lessons from Shape Up:


* __Shape the work__ before giving it to a team. Focus on __appetite__. Instead of asking _how much time it will take to do some work_, ask: _How much time do we want to spend? How much is this idea worth?_

* __Principles of Shaping__:
  - Wireframes are too concrete . Words are too abstract.
  - Properties of shaped work:
    - __Rough__: Enough flexibility for designers & programmers to think and apply their expertise
    - __Solved__: All main elements of solution are there at the macro level and they connect together
    - __Bounded__: Absolute clarity on what not to do

&nbsp;
* __Steps to shaping__:
  - __Set boundaries__: Figure out how much time the raw idea is worth and how to define the problem. Default response to any idea that comes up should be: “_Interesting. Maybe someday_.” In other words, a very soft “no”.
  - __Rough out the elements__: Sketch a solution at a higher level of abstraction than wireframes in order to move fast and explore widely (Breadboarding / Fat-sketches).
  - __Address risks and rabbit holes__: Find holes or unanswered questions that could trip up the team. Solve them by cutting things out, or specifying details at tricky spots. Well-shaped work looks like a thin-tailed probability distribution. There’s a slight chance it could take an extra week but, no reason to go beyond that. Beware the simple question: “_Is this possible_?”. In software, everything is possible but nothing is free. Rather than asking “_Is it possible to do X_?” ask “_Is X possible in 6-weeks_?”
  - __Write the pitch__: The pitch summarizes the problem, constraints, solution, rabbit holes, and limitations (_No-gos_). The pitch goes to the betting table for consideration.

* __Bets, Not backlogs__: A pitch is not tracked if it’s rejected for the current cycle.  Anyone who wants to advocate for it again simply tracks it independently—their own way—and then lobbies for it six weeks later.

* __Betting Six Weeks__
  - Six weeks is long enough to finish something meaningful and still short enough to see the end from the beginning. Think like: “_If this project ships after six weeks, we’ll be really happy. We’ll feel our time was well spent_.”
  - __Uninterrupted time__: When you make a bet, you honor it. Do not allow the team to be interrupted or pulled away to do other things.
  - __The circuit breaker__: Teams have to ship the work within the amount of time that has been bet. If they don’t finish, by default the project doesn’t get an extension.
  - __Fixing bugs__: If it's a crisis, drop everything and work on it. But crises are rare. The vast majority of bugs can wait six weeks or longer.
  - __Think of screen space in terms of real estate__: If we give that space to that button up now, we won’t be able to use it in the future. Are we selling it too cheaply to solve this particular problem?

* __Hand Over responsibility__: Don’t assign tasks to anyone. Trust the team to take on the entire project and work within the boundaries of the pitch. Give full responsibility to a small integrated team of designers and programmers.

* __Get One Piece Done__: Instead of building lots of disconnected parts and hoping they’ll fit together in the 11th hour,  build one meaningful piece of the work end-to-end early on and then repeat. Work vertically on one small piece of the project instead of chipping away at the horizontal layers. Have something tangible and demo-able in the first week.

![](https://basecamp.com/assets/books/shapeup/3.2/back-end_only-e8b9580807d4b4b50a31627b20d37c1dcf90c55b1f0cc20d5ab88f25888b6bf6.png)
![](https://basecamp.com/assets/books/shapeup/3.2/one_slice-4cbcdda1a5cdc1b2bdc9bf7bd023cc0c5af666c5857c6e7d32650d9229a81cf0.png)

* __Which piece to work on first? Core, small & Novel__: Choose the feature which solves the core issue first, is small enough to demonstrate. In case of collision, chose the one which is more novel (the one which offers more learning for the team/ eliminates uncertainty)

* __Map the Scopes__: Organize work by structure, not by person. Segregate work by tasks that fit together (scopes). Scopes reflect the meaningful parts of the problem that can be completed independently and in a short period of time—a few days or less. _They are bigger than tasks but much smaller than the overall project_. Well-made scopes show the anatomy of the project.
![](https://basecamp.com/assets/books/shapeup/3.3/drafts_6-a511456472dd9b348e6fc314781a8e6c91e7ae942eed0779036539bf27bbb530.png)

* __Use Hill Charts to show progress__: Each dot represents a piece of work. Every piece of work has two phases. First there’s the uphill phase of figuring out what our approach is and what we’re going to do. Then, once we can see all the work involved, there’s the downhill phase of execution. _Easy to execute once all unknowns are resolved_.
![](https://basecamp.com/assets/books/shapeup/3.4/snapshots-acc8efc1f87284428ed51816961e7f6f40141ff29cf1103c3d0002e73b0da497.png)

* __Decide When to Stop__: Don't aim for the ideal design/Code, compare down to baseline—the current reality for customers. How do customers solve this problem today, without this feature? Move from _“never good enough”_ to _“better than what they have now”_.
![](https://basecamp.com/assets/books/shapeup/3.5/compare_to_baseline-ff521686dc8ea60cb9587d072409f5ee8bba79ca269e0fb04963b930699fb62d.jpg)

* __Scope Hammering__: Divide features into __Must-haves__ vs __Nice-to-haves__. Be brutal in this differentiation & its execution.

* __On Testing__:
  - Programmers write their own tests and ship features.
  - _Think of QA as a level-up, not a gate or a check-point that all work must go through_. Things are better off with QA than without it but don’t depend on QA to ship quality features that work as they should.

* __Code review__: Same as testing. _The team can ship without waiting for a code review. There’s no formal check-point_. But code review makes things better, so if there’s time and it makes sense, someone senior may look at the code and give feedback.

* __Move On__: Stay debt free after shipping features post a six-week betting cycle. _A flood of new requests will come in - say a polite No and let the requests compete with everything else on the next betting table/ release cycle_.
