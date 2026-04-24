# Layout Rules

## Overall Style

The pages should feel like a subtle background structure for calligraphy and decoration, not like a traditional boxed planner.

## Inside Page Structure

- 2 columns per page
- 3 months per column
- 6 months total per page
- Dates flow seamlessly down each column across month boundaries

## Column Rules

- Weekday names appear once at the top of each column
- Month starts are identified by small inline month labels
- Non-month dates are omitted rather than repeated
- Vertical grid lines are allowed
- Horizontal guides should remain subtle
- Avoid heavy borders or boxed month sections

## Annotation Rules

- Date annotations are driven by `dating_log_connie.csv`
- Categories are styled using `CATEGORY_STYLES` in `src/annotations.py`
- Date cells display compact category markers
- Legend page is generated from the marker/label dictionary

## Cover Page Structure

- Top area remains blank for handwritten message
- Date boxes sit lower on the page
- Date boxes use 20/20/20/20/20 horizontal proportions
- Small heart appears beneath the date boxes
- Cover should remain open and minimal

## Booklet Layout

The final print-order PDF is imposed for two-up duplex printing.  
Page order is intentionally not chronological; it is arranged for physical booklet assembly.