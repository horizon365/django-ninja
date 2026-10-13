# 996 Salary Calculator

Page: https://georgehuan1994.github.io/996-Salary-Calculator/

## Introduction

<br/>

> "What is your expected salary?"

<br/>

This is almost an unavoidable question.

Most people's expected salary is a broad range, and it varies significantly across different companies and departments.

For example: What are the working hours? Is there overtime pay? 14 months' salary? 16 months' salary? Housing provident fund? Base salary?

...

So the price quoted is often highly subjective and arbitrary.

And that's why this tool exists!

---

Click to jump to: [996 Salary Calculator](https://georgehuan1994.github.io/996-Salary-Calculator/)

![2021-10-15_115036](https://user-images.githubusercontent.com/49583943/137430292-c785dbb0-ea57-4989-862f-46cd2e860500.png)

## Explanation

### Expected Annual Salary

Based on the standard of "965 schedule, 12 months' salary, full housing provident fund", enter your expected annual salary to get the standard hourly rate and standard monthly salary.

### Daily Working Hours

Presets: 965, 995, 995.5, 996. Custom working hours are supported, such as Tencent's Wednesday Health Day.

Calculates the full year (50 weeks) of regular working hours, overtime hours, and rest-day hours, then derives the entitled annual salary and entitled monthly salary.

- The first 9 hours on a workday are counted as **regular hours** at 1x the hourly rate;
- Any hours beyond 9 on a workday are counted as **overtime hours** at 1.5x the hourly rate;
- Any hours beyond 0 on a rest day are counted as **rest-day hours** at 2x the hourly rate.

### Annual Payout

Enter the number of months over which salary is paid. 12 months? 13.5 months? 14 months? 16 months? ...

### Housing Provident Fund Contribution Rate (Company)

Lower bound: 5%, upper bound: 12%

Many people have a misconception about the company's housing provident fund contribution rate, namely: "Whatever I contribute, the company contributes the same."

But this value is unrelated to the individual's chosen rate. Companies generally pick a fixed rate and do not follow the individual's contribution rate.

### Housing Provident Fund Contribution Base (Company)

Lower bound: 2100, upper bound: 33786. There are some differences across regions.

Many companies not only have a low contribution rate, but also a low contribution base.

**Important note: This value is typically consistent with the "base salary" in the labor contract. Compensation related to disputes, layoffs, or non-compete agreements may be constrained by it!**

### Adjusted Monthly Salary

Based on the housing provident fund contribution rate and base, adjust the entitled monthly salary.

---

    If this project helps you, click the star button in the upper right corner and give me a Star ⭐️ to cheer me on~
