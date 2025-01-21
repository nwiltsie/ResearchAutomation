---
theme: eloc
background: https://cover.sli.dev
title: Accelerating Research with Automation
class: text-center
drawings:
  persist: false
mdc: true
colorSchema: light
highlighter: shiki
---

# Accelerating Research with Automation

Nick Wiltsie, January 2025

---

## About Me

- BS + MS in Mechanical Engineering from MIT
- 9 years at NASA's Jet Propulsion Laboratory
  - Rover planner for Curiosity and Perseverance
  - Lead developer for rover planner ground software
  - Received Early Career Public Achievement Medal for improving science return
- Now a software engineer in Dr. Paul Boutros's lab

---

## What is an Automation?

- A system, tool, or workflow <!-- .element: class="fragment" -->
- that performs tasks or processes automatically <!-- .element: class="fragment" -->
- with minimal or no human intervention <!-- .element: class="fragment" -->

---

## Why Automate?

I:

- Am **easily bored**
- Have a **short attention span**
- Have a **poor memory**

<!-- Quantum Leap, Memento -->

---

## Remove tedium

![Alt](/Monotony.svg)

---

## Increase vigilance

![Alt](/Vigilance.svg)

---

## Maintain capabilities

![Alt](/Time_Displacement.svg)

---

## Increase productivity

![Alt](/Productivity.svg)

---

![Alt](/What_is_an_automation.svg)

<!-- I understand this problem well enough that I can solve every similar problem in the future. -->

---

## Good Targets for Automation - VURVEN

(Expanded from [this](https://zapier.com/blog/automation-for-education/) Zapier blog post)

- **V**olume: Happens a lot
- **U**niform: Accomplished in a similar way each time
- **R**epetitive: Done multiple times in a row
- **V**aluable: Worth doing
- **E**rror: Easy to get wrong / problematic if done wrong
- u**N**enjoyable

---
zoom: 0.4
---

## Manual Nextflow Pipeline release steps

Updating metapipline-DNA from `6.1.0` to `6.2.0`:

<v-clicks>

1. Decide on the new version number
1. Create a new git branch
   1. Update `CHANGELOG.md`
      1. Move `Unreleased` changes under new `6.2.0` section, with current date
      1. Add link to GitHub changes since last release (link will not work yet)
   1. Update version number in `nextflow.config`
1. Create pull request with changes
   - Don't let anything else merge between opening and merging this PR
1. Get approval, merge pull request
1. Create GitHub release with tag `v6.2.0`
   - Note the leading `v`
   - Make sure you're creating the release from the correct commit
   - This is when the link added to `CHANGELOG.md` will start working
1. Attach tarball of pipeline, including all submodules, to the GitHub release
1. Deploy updated pipeline onto compute cluster
   1. Rename catch-all test output directory (`$RELEASE_DIR/development/unreleased`) to `6.2.0/`.
   1. Create new catch-all test output directory
   1. Download and unpack release tarball into `$RELEASE_DIR/release/6.2.0/`
1. Announce new release and major changes to lab via email

</v-clicks>

---
zoom: 0.6
---

## Automated Pipeline Release Steps

<v-clicks>

1. Determine if release includes breaking changes, behavioral changes, or patches
1. Run `Prepare Release` workflow on GitHub for chosen release type
   - Updates `CHANGELOG.md` and `nextflow.config`
   - Opens pull request with details of who triggered the release
1. Approve and merge PR
   - Creates GitHub release with auto-generated notes
   - Attaches tarball with submodules
1. Wait < 60 minutes
   - Deploys pipeline onto compute cluster
   - Updates test output directory
   - Announces deployment in Teams
1. Wait until Monday
   - Emails lab with all new deployments since last week

</v-clicks>

---
layout: image
backgroundSize: contain
image: /Enrollment.png
---

---

## Example 1

Generating emails

---

## Structure: If This Then That

![Alt](/IFTTT.svg) <!-- .element: class="fragment" -->

---

![Alt](/IFTTT_Expanded.svg)

---

## Example 2

BlinkyTape!

---
zoom: 0.7
---

## Rapid-Fire Data Types

_There are lots of simplifications here, don't @ me._

| Primitive Type | Description                                                                               |
| -------------- | ----------------------------------------------------------------------------------------- |
| String         | Text. A sequence or "string" of characters (which can include number characters).         |
| Integer        | A whole number, e.g `-1`, `7`, `0`.                                                       |
| Float          | A real number with a fractional part, e.g. `1.0`, `17.333333`.                            |
| Boolean        | True or False.                                                                            |
| Null           | A special value indicating the absence of a value (to differentiate from an empty value). |

![Alt](/Strings.svg)

---
zoom: 0.7
layout: two-cols-header-fixed
---

::header::

## Compound Data Types

::left::

| Compound Type | Similar Names                        | Description                                                                   |
| ------------- | ------------------------------------ | ----------------------------------------------------------------------------- |
| Array         | List, vector, tuple                  | An ordered collection of items that can be accessed by index.                 |
| Map           | Dictionary, hash table, lookup table | A unordered collection that maps unique keys (generally primitives) to items. |

::right::
![Alt](/Data_Structures.svg)

<!-- .element: class="fragment" -->

---
zoom: 0.7
---

## Everything Else

| Special Type                           | Similar Names          | Description                                                                                |
| -------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------ |
| **B**inary **L**arge **Ob**ject (blob) | Raw/binary data, bytes | An opaque block of data - can be literally anything. _Generally_ useless without metadata. |

![Alt](/Raw_Bytes.svg)

<!-- .element: class="fragment" -->

---

## Example 3

Office documents

---

![Alt](/Good_Automations.svg)
