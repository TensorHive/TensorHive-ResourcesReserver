# TensorHive-ResourcesReserver

## About
We're developing a lightweight computing resource reservation system that will work with [roscisz/TensorHive](https://github.com/roscisz/TensorHive).

## Example use case (why you should consider using our system)
You own/administrate some computing resources (like 8 NVIDIA TITAN X GPUs) and you must allow other users using it (e.g. workmates).

After some time you realize they interrupt each other, simply because there are more users than resources. 

A simple solution is to create a mailing system/chatroom as a place to resolve conflicts and allow declaring their needs: 
> I need 2 GPUs tommorow, from 2pm to 8pm

**Unfortunately that doesn't work very often...** They declare using a GPU for 8 hours but in reality it takes 2 days or simply they say:
> Oh sorry man, I haven't seen this message. Did I interrupt someone?

## Core features (release planned for December 2018)
- [ ] Users can make reservations using calendar
- [ ] Priviliged users can view resource utilization on charts (CPU, GPU, mem, disk)
- [ ] During the reservation period users can freely access declared resources
- [ ] When reservation time expires (or before it starts), user processes are stopped
- [ ] Admin dashboard (ban users, edit/reject reservations)

## Goal
We want it to be small and lightweight, so that anyone can set it up **within minutes**.

**Small companies, universities are our targeted "customers"**.

If you are interested, just give us a star or post an issue. We'd love to notify you when the project is completed (v1.0.0)
