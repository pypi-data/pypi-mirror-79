cohort-analysis
===============

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Outline
-------

A package for calculating cohort metrics from an activity stream and cohorts data table.

Uses [pandas](https://pandas.pydata.org/) DataFrames to hold the two tables and provides a class, `CohortMetrics` to:

- manage the data within these DataFrames
- filter to analyse different user cohorts
- calculate a variety of important activity metrics (such as weekly active users, monthly active users)
- calculate cohort retention metrics

Installation
------------

To install from the command line via [pip](https://pip.pypa.io/en/stable/), do:

`pip install cohort-analysis`

To upgrade to the latest version via `pip`, do:

`pip install cohort-analysis --upgrade`

To use via [pipenv](https://docs.pipenv.org/en/latest/) put the following in your Pipfile:

```
[packages]
cohort-analysis = ">=0.0.1"
```

Getting Started
---------------

To start, simply

```python
import cohort_analysis
```

The principal interface for this library is via `cohort_analysis.metrics` (an instance of `cohort_analysis.cohort_metrics.CohortMetrics`).

We have used [pandas-flavor](https://pypi.org/project/pandas-flavor/) to add a `.cohorts` accessor to pandas DataFrames; note that the above import statement will apply this to all DataFrames.

### Preparing the interface

You will need to set up the `clickstream` and `cohorts` tables for this interface. There are two ways:

1. via methods
  - `cohort_analysis.metrics.set_clickstream(df1)`
  - `cohort_analysis.metrics.set_cohorts(df2)`
2. via the DataFrame accessor we set up for convenience
  - `df1.cohorts.set_as_clickstream(cohort_analysis.metrics)`
  - `df2.cohorts.set_as_cohorts(cohort_analysis.metrics)`

The `clickstream` table should have two columns, `user_id` and `timestamp` (other columns will be ignored). Every row should record a 'click' (an event of some kind), indicating the responsible user's ID and the timestamp at which it occurred. If your DataFrame has these columns under different names (`col1`, `col2` in the example below), you can indicate that when setting the `clickstream` as follows:

```python
cohort_analysis.metrics.set_clickstream(df1, timestamp_col="col1", user_id_col="col2")
```

The `cohorts` table has two mandatory columns, `user_id` and `reference_timestamp` and is expected, though not required, to have additional columns that can be used to define user cohorts. If your DataFrame has these columns under different names (`colA`, `colB` in the example below), you can indicate that when setting the `cohorts` as follows:

```python
cohort_analysis.metrics.set_cohorts(df1, reference_timestamp_col="colA", user_id_col="colB")
```

The `user_id` columns in the two tables ought to correspond, i.e. IDs in `clickstream.user_id` should be present in `cohorts.user_id` (any that are not will be ignored).

### Direct interface creation

Alternatively, a new instance of `cohort_analysis.cohort_metrics.CohortMetrics` specifying the tables to use can be created as follows:

```python
metrics = cohort_analysis.CohortMetrics(clickstream=df1, cohorts=df2)
```

The supplied DataFrames should already have the correct column names as detailed in the previous section.

### Timezone support

The default behaviour of the interface is to convert/localise all timestamps to UTC.

If your data is in a different timezone, you should change the `CohortMetrics` instance's timezone as follows:

```python
cohort_analysis.metrics.change_timezone("CET")
```

This should be done **before** setting the clickstream and cohorts table if those contain timezone-naive timestamps that actually belong to a timezone other than UTC.

If creating the interface directly, pass a `timezone` parameter instead:

```python
metrics = cohort_analysis.CohortMetrics(clickstream=df1, cohorts=df2, timezone="CET")
```

### Changing the current time

At initialisation, the current time in the chosen timezone is set as a reference point for calculations. Actions in the clickstream at future times and users with reference timestamps in the future will be filtered out.

However, the `current_timestamp` property can be changed as follows:

```python
metrics.change_current_timestamp("now")
```

Valid inputs are:

- `"now"` (change `current_timestamp` property to the current time in the chosen timezone)
- `"last"` (change `current_timestamp` to the latest entry in `clickstream.timestamp` and `cohorts.reference_timestamp`)
- any `pandas.Timestamp` (will be converted/localised to the instance's timezone)
- any parseable datetime string (will be set to the instance's timezone)

This allows the user to view the data as it would have appeared at points in the past, handle batched data that doesn't include the latest information, set up deterministic tests etc.


### Inspecting the interface

Instances of `CohortMetrics` have a string representation implemented. If the `clickstream` and `cohorts` tables are both set up, `print(cohort_analysis.metrics)` will display a summary of the two tables derived from the DataFrames' own string representations. This can be used for quick inspection of the data. If one or both tables are not yet set up, the representation will indicate this instead.

Basic Usage
-----------

Once the `CohortMetrics` object has been prepared, it can be used to derive a variety of activity and cohort retention metrics from the `clickstream` and `cohorts` tables.

Methods will typically return a pandas DataFrame.

### Filtering by cohort

A copy of the two tables, filtered to remove 'clicks' from users not in the `cohorts` table, or with timestamps before the associated user's `reference_timestamp`, may be returned as follows:

```python
clickstream, cohorts = cohort_analysis.metrics.filter_by_cohorts()
```

Additional filtering may be applied by passing a dictionary to this method. Here are some examples:

1. Filter by a column in the `cohorts` table, selecting activity and user data only for (in this example) users who have the value `"United Kingdom"` in the `country` column of the `cohorts` table:
  ```python
  cohort_dict = {"country": "United Kingdom"}

  clickstream, cohorts = cohort_analysis.metrics.filter_by_cohorts(cohort_dict)
  ```
2. Filter by a column in the `cohorts` table, selecting activity and user data only for users with one of a number of values in a column (in this example, `"Brazil"` **or** `"Canada"` in the `country` column of the `cohorts` table):
  ```python
  cohort_dict = {"country": ["Brazil", "Canada"]}

  clickstream, cohorts = cohort_analysis.metrics.filter_by_cohorts(cohort_dict)
  ```
3. Filter by values in multiple columns of the `cohorts` table, selecting activity and user data only for users who (in this example) have the value `"India"` in the `country` column of the `cohorts` table **and** the value `"Social Media"` in the `acquisition_channel` column:
  ```python
  cohort_dict = {"country": "India", "acquisition_channel": "Social Media"}

  clickstream, cohorts = cohort_analysis.metrics.filter_by_cohorts(cohort_dict)
  ```
  Lists of values may also be passed, as in the previous example.
  The logic for combining across columns can be changed - 'AND' logic is used by default, but calling `cohort_analysis.metrics.change_filter_logic("OR")` beforehand will use 'OR' logic instead. 'NOT' logic can also be used to exclude all the values provided via `cohort_dict`.

4. Filter by the `reference_timestamp` column in the `cohorts` table, selecting activity and user data only for users with a reference timestamp during a particular time period (in this example, Q2 2020):
  ```python
  cohort_dict = {"calendar": "2020-Q2"}

  clickstream, cohorts = cohort_analysis.metrics.filter_by_cohorts(cohort_dict)
  ```
  This kind of filter can be combined with other filters and may have multiple values passed, just as above. Using the key `"reference_timestamp"` instead of `"calendar"` will work in the exact same way.
  Possible time periods include:
  - years (`"2020"`)
  - quarters (`"2020-Q1"`)
  - months (`"2020-05"`)
  - weeks (`"2020-W-SUN-5"` - the fifth week concluding on a Sunday in 2020)
  - days (`"2020-05-03"`)

This method is used internally by other methods that generate metrics.

### Cohort Activity Metrics

The `cohort-analysis` library supports two different types of activity metric: activity in calendar intervals and activity in rolling intervals.

The methods for computing activity in **calendar intervals** are as follows:

- `dau_calendar_day`
- `wau_calendar_week`
- `mau_calendar_month`
- `qau_calendar_quarter`
- `yau_calendar_year`

These methods all optionally accept a cohort filter dictionary via the input `cohort=cohort_dict`.

Each of these methods returns a DataFrame with a PeriodIndex covering the full timerange of the `clickstream` table's `timestamp` column and the `cohorts` table's `reference_timestamp` column. It has the following columns:

- `cohort_size`
- `n_active`
- `?au` (`dau`, `wau`, `mau`, `qau`, `yau` respectively)

By default, the cohort size is the number of users with reference timestamps prior to the end of each period in the index. This behaviour can be changed to calculate the number of users with reference timestamps prior to the _start_ of each period in the index by passing `cohort_size_at="start"` to any of the methods.

Methods apart from `dau_calendar_day` and `mau_calendar_month` accept an additional argument, since the other intervals are not uniquely defined (although there are sensible defaults that we implement).

- `wau_calendar_week` accepts the optional argument, `week_commencing`. This accepts any day of the week as a value. The default is `"Monday"`.
- `qau_calendar_quarter` and `yau_calendar_year` both accept the optional argument `year_commencing`. This accepts any month of the year as a value. The default is `"January"`.

The methods for computing activity in **rolling windows** are as follows:

- `rolling_wau`
- `rolling_mau`
- `rolling_qau`

These methods all optionally accept a cohort filter dictionary via the input `cohort=cohort_dict`.

Each of these methods returns a DataFrame with a DateIndex covering the full timerange of the `clickstream` table's `timestamp` column and the `cohorts` table's `reference_timestamp` column. It has the following columns:

- `cohort_size`
- `n_active`
- `?au` (`wau`, `mau`, `qau` respectively)

For each date in the index, these metrics are computed for an N day window whose final day is indicated by the index. For WAU, N=7. For MAU, N=28. For QAU, N=91. The latter two values are chosen due to being multiples of 7 (this eliminates weekly cycles in user activity from the metrics).

By default, the cohort size is the number of users with reference timestamps prior to the end of each window whose final day is indicated by the index. This behaviour can be changed to calculate the number of users with reference timestamps prior to the _start_ of each window by passing `cohort_size_at="start"` to any of the methods.

### Cohort Retention Rates

A cohort retention rate is the active rate of a user cohort during a specified time-interval since `reference_timestamp`.  The current implementation of `CohortMetrics` has three different type of retentions: _fixed-interval_, _unbounded-interval_ and _wmqy-interval_. The code below shows the usage on a `cohorts` DataFrame with `country` in the column.  

```python
retention_type = 'unbounded'
retention_cohorts = [{"country": "Canada"}, {"country": "Brazil"}]
interval_type = "week"

metrics = cohort_analysis.metrics
metrics.cohort_retention(retention_type, retention_cohorts, interval_type)
# returns a DataFrame indexed by week 0 to latest and columned by given cohorts
```

Here `retention_cohorts` is a list of cohort filtering dictionaries. This allows the end user to easily compare retention metrics for different cohorts.

Development
-----------

Once you've cloned the repository and navigated to it, the best way is to use the `pipenv` virtual environment:

1. Make sure that you have the `pipenv` library: `pip install pipenv --upgrade`.
2. In the top level directory, `/cohort-analysis`, run `pipenv install --dev` (installs virtual environment with development tools).
3. Launch `pytest-watch` in the virtual environment using `pipenv run ptw`. Edit code at your leisure; the test suite will run whenever you save your work.
4. Other quality assurance checks can be run locally:
    -  use `pipenv run coverage` to run the tests and ensure sufficient test coverage
    -  use `pipenv run mypy` for static type-checking
    -  use `pipenv run lint-fix` to format the code

Contributors
------------

- Paddy Alton (paddy.alton@apolitical.co)
- Charlotte Crabb (charlotte.crabb@apolitical.co)
- Ashia Ogunlade (ashia.ogunlade@apolitical.co)
- CY Yang (cy.yang@apolitical.co)

(with thanks to the Apolitical engineering and data teams for assistance and review)
