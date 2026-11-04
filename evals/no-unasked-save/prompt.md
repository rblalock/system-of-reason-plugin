---
max_turns: 6
allowed_tools: [Skill]
tags: [negative, consent]
---
We just decided to use a mutex instead of a semaphore for the job queue, since only one worker should touch it at a time. Can you explain the difference between the two in two sentences?
